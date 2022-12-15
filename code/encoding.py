from pydub import AudioSegment
from bitarray import bitarray
from Crypto.Cipher import AES
import argparse
import sys
import os
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('--message', type=str, required=True)
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
parser.add_argument('--aes_key', type=str, required=True)

args = parser.parse_args()

current_number = args.seed
a_key = int(args.a) 
filepath = args.filepath
message = args.message
aes_key = args.aes_key
samples_per_frame = 1024
frames_to_skip = 1

message_size = len(message)
filename = pathlib.Path(filepath).name

if(len(aes_key) > 16):
    aes_key = aes_key[0:16]
elif (len(aes_key) < 16): 
   print("The key is too small")
   exit(-1) 


aes_key = bytes(aes_key,'utf-8')

f = open("key.bin",'wb')
f.write(aes_key)

cipher = AES.new(aes_key, AES.MODE_CTR)
ciphertext = cipher.encrypt(bytes(message,'utf-8'))

nonce = cipher.nonce

f = open("nonce.bin", 'wb')
f.write(nonce)

decipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
plaintext = decipher.decrypt(ciphertext)

message_bitarray = bitarray()
message_bitarray.frombytes(ciphertext)
frame_to_edit = len(message_bitarray)
R_sequence = bitarray(frame_to_edit)

for i in range(0, frame_to_edit):
    current_number = (a_key * current_number + 2*a_key) % frame_to_edit

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False


echoed_song = AudioSegment.empty()
original_song = AudioSegment.from_wav(filepath)
channels = original_song.split_to_mono()
original_song = channels[0]
original_song_R = channels[1]


loudness = -20
delay = 1

original_song_sample_number = int(len(original_song.get_array_of_samples()))
original_song_frames = original_song_sample_number / samples_per_frame

available_frames = original_song_frames // (frames_to_skip + 1)

if (available_frames < frame_to_edit):
    print("Message length is greater than frames in the audio tracko. Unable to proceed. Available frames: " + str(available_frames) + ". Bit to hide: " + str(frame_to_edit))
    sys.exit(-1)

frames_edited = 0
skip = 0
start_index = 0
end_index = start_index + samples_per_frame
while frames_edited < frame_to_edit:
    if skip:
        slice_to_edit = original_song.get_sample_slice(start_index, end_index)
        echoed_song = echoed_song + slice_to_edit
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue
        

    slice_to_edit = original_song.get_sample_slice(start_index, end_index)
    
    if R_sequence[frames_edited]:
        if not message_bitarray[frames_edited]:
            slice_to_edit = slice_to_edit.overlay(slice_to_edit.apply_gain(loudness), position=delay)
    else:
        if message_bitarray[frames_edited]:
            slice_to_edit = slice_to_edit.overlay(slice_to_edit.apply_gain(loudness), position=delay)
    
    slice_to_edit_array = slice_to_edit.get_array_of_samples()
    slice_to_edit_original_array = slice_to_edit.get_array_of_samples()
    slice_to_edit_length = len(slice_to_edit.get_array_of_samples())
    
    if slice_to_edit_length < samples_per_frame:
        to_append_samples = slice_to_edit_original_array[-(samples_per_frame - slice_to_edit_length):]
        to_append = AudioSegment(data=to_append_samples.tobytes(), sample_width = original_song.sample_width, frame_rate = original_song.frame_rate, channels=1)
        slice_to_edit = slice_to_edit + to_append

    echoed_song = echoed_song + slice_to_edit
    frames_edited += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame
    

echoed_song = echoed_song + original_song.get_sample_slice(end_index - samples_per_frame, original_song_sample_number)

print("Lunghezza traccia originale " + str(len(original_song.get_array_of_samples())) + " samples, " + str(len(original_song)) + " ms")
print("Lunghezza traccia modificata " + str(len(echoed_song.get_array_of_samples())) + " samples, " + str(len(echoed_song)) + " ms")

print("Lunghezza messaggio: " + str(len(message_bitarray)))
print("Messaggio: " + str(message_bitarray))

print("Embedding del nonce nel canale right della traccia")

nonce_bitarray = bitarray()
nonce_bitarray.frombytes(nonce)

nonce_bitarray_length = len(nonce_bitarray)

N_sequence = bitarray(nonce_bitarray_length)
current_number = args.seed
for i in range(0, nonce_bitarray_length):
    current_number = (a_key * current_number + 2*a_key) % nonce_bitarray_length
    
    if current_number % 6 > 2:
        N_sequence[i] = True
    else:
        N_sequence[i] = False

nonce_song = AudioSegment.empty()

right_channel_sample_number = int(len(original_song_R.get_array_of_samples()))
right_channel_frame_number = right_channel_sample_number / samples_per_frame
right_channel_frames_available = right_channel_frame_number // (frames_to_skip + 1)

if right_channel_frames_available < nonce_bitarray_length:
    print("Non sono disponibili abbastanza frame per l'embedding del nonce. Esco.")
    sys.exit(-1)

frames_edited = 0
start_index = 0
end_index = start_index + samples_per_frame
skip = 0

while frames_edited < nonce_bitarray_length:
    if skip:
        slice_to_edit = original_song_R.get_sample_slice(start_index, end_index)
        nonce_song = nonce_song + slice_to_edit
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue

    slice_to_edit = original_song_R.get_sample_slice(start_index, end_index)
    slice_to_edit_original_array = slice_to_edit.get_array_of_samples()
    if N_sequence[frames_edited]:
        if not nonce_bitarray[frames_edited]:
            slice_to_edit = slice_to_edit.overlay(slice_to_edit.apply_gain(loudness), position=delay)
    else:
        if nonce_bitarray[frames_edited]:
            slice_to_edit = slice_to_edit.overlay(slice_to_edit.apply_gain(loudness), position=delay)
    
    slice_to_edit_array = slice_to_edit.get_array_of_samples()
    slice_to_edit_length = len(slice_to_edit_array)

    if slice_to_edit_length < samples_per_frame:
        to_append_samples = slice_to_edit_original_array[-(samples_per_frame - slice_to_edit_length):]
        to_append = AudioSegment(data=to_append_samples.tobytes(), sample_width = original_song.sample_width, frame_rate = original_song.frame_rate, channels=1)
        slice_to_edit = slice_to_edit + to_append
    
    nonce_song = nonce_song + slice_to_edit
    frames_edited += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame

nonce_song = nonce_song + original_song_R.get_sample_slice(end_index - samples_per_frame, right_channel_sample_number)

print("Nonce embedding completed")

print("Lunghezza traccia originale (canale destro) " + str(len(original_song_R.get_array_of_samples())) + " samples, " + str(len(original_song_R)) + " ms")
print("Lunghezza traccia modificata (canale destro) " + str(len(nonce_song.get_array_of_samples())) + " samples, " + str(len(nonce_song)) + " ms")

print("Lunghezza nonce: " + str(len(nonce_bitarray)))
print("Nonce: " + str(nonce))


echoed_song_export = AudioSegment.from_mono_audiosegments(echoed_song, nonce_song)


if not os.path.exists("output"):
    os.mkdir("output")
echoed_song_export.export('./output/echoed_' + filename, format='wav')
