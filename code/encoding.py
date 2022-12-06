from pydub import AudioSegment
from bitarray import bitarray
from Crypto.Cipher import AES
import argparse
import sys
import os

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

if len(aes_key) > 16:
    aes_key = aes_key[0:16]
elif len(aes_key) < 16:
    print("La chiave proposta non risulta essere di 128 bit o più. Uscita")
    sys.exit(0)

aes_key = aes_key.encode()

cipher = AES.new(aes_key, AES.MODE_CTR)
ciphertext = cipher.encrypt(message.encode())
nonce = cipher.nonce

print("Len nonce" + str(len(nonce)))

samples_per_frame = 1024
frames_to_skip = 2

message_size = len(message)

message_bitarray = bitarray()
message_bitarray.frombytes(ciphertext)

nonce_bitarray = bitarray()
nonce_bitarray.frombytes(nonce)

frame_da_modificare = len(message_bitarray)
frame_da_modificare_nonce = len(nonce_bitarray)

R_sequence = bitarray(frame_da_modificare)
N_sequence = bitarray(frame_da_modificare_nonce)

for i in range(0, frame_da_modificare):
    current_number = (a_key * current_number + 2*a_key) % frame_da_modificare

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False

current_number = args.seed

for i in range(0, frame_da_modificare_nonce):
    current_number = (a_key * current_number + 2*a_key) % frame_da_modificare_nonce

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False


echoed_song = AudioSegment.empty()
nonce_song = AudioSegment.empty()
original_song = AudioSegment.from_wav(filepath)
original_song_R = original_song.split_to_mono()[1]
original_song = original_song.split_to_mono()[0]


loudness = -20
delay = 2

original_song_sample_number = int(len(original_song.get_array_of_samples()))
original_song_frames = original_song_sample_number / samples_per_frame

available_frames = original_song_frames // (frames_to_skip + 1)

if (available_frames < frame_da_modificare):
    print("La lunghezza del messaggio supera il numero di frame della traccia audio. Impossibile procedere. Frame disponibili: " + str(available_frames) + ". Bit da nascondere: " + str(frame_da_modificare))
    sys.exit(0)

if (available_frames < frame_da_modificare_nonce):
    print("La lunghezza del nonce supera il numero di frame della traccia audio. Impossibile procedere. Frame disponibili: " + str(available_frames) + ". Bit da nascondere: " + str(frame_da_modificare))
    sys.exit(0)

frames_edited = 0
skip = 0
start_index = 0
end_index = start_index + samples_per_frame
while frames_edited < frame_da_modificare:
    if skip:
        slice_da_modificare = original_song.get_sample_slice(start_index, end_index)
        echoed_song = echoed_song + slice_da_modificare
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue
        

    slice_da_modificare = original_song.get_sample_slice(start_index, end_index)
    
    if R_sequence[frames_edited]:
        if not message_bitarray[frames_edited]:
            slice_da_modificare = slice_da_modificare.overlay(slice_da_modificare.apply_gain(loudness), position=delay)
    else:
        if message_bitarray[frames_edited]:
            slice_da_modificare = slice_da_modificare.overlay(slice_da_modificare.apply_gain(loudness), position=delay)
    
    slice_da_modificare_array = slice_da_modificare.get_array_of_samples()
    slice_da_modificare_length = len(slice_da_modificare.get_array_of_samples())
    
    if slice_da_modificare_length < samples_per_frame:
        to_append_samples = slice_da_modificare_array[len(slice_da_modificare_array) - (samples_per_frame - len(slice_da_modificare_array)):]
        to_append = AudioSegment(data=to_append_samples.tobytes(), sample_width = original_song.sample_width, frame_rate = original_song.frame_rate, channels=1)
        slice_da_modificare = slice_da_modificare + to_append

    echoed_song = echoed_song + slice_da_modificare
    frames_edited += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame
    

echoed_song = echoed_song + original_song.get_sample_slice(end_index - samples_per_frame, original_song_sample_number)

print("Lunghezza traccia originale " + str(len(original_song.get_array_of_samples())) + " samples, " + str(len(original_song)) + " ms")
print("Lunghezza traccia modificata " + str(len(echoed_song.get_array_of_samples())) + " samples, " + str(len(echoed_song)) + " ms")

print("Lunghezza messaggio: " + str(len(message_bitarray)))
print("Messaggio: " + str(message_bitarray))

print("Embedding del nonce all'interno del canale destro della traccia")

frames_edited = 0
skip = 0
start_index = 0
end_index = start_index + samples_per_frame
while frames_edited < frame_da_modificare_nonce:
    if skip:
        slice_da_modificare = original_song_R.get_sample_slice(start_index, end_index)
        nonce_song = nonce_song + slice_da_modificare
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue
        

    slice_da_modificare = original_song_R.get_sample_slice(start_index, end_index)
    
    if N_sequence[frames_edited]:
        if not nonce_bitarray[frames_edited]:
            slice_da_modificare = slice_da_modificare.overlay(slice_da_modificare.apply_gain(loudness), position=delay)
    else:
        if nonce_bitarray[frames_edited]:
            slice_da_modificare = slice_da_modificare.overlay(slice_da_modificare.apply_gain(loudness), position=delay)
    
    slice_da_modificare_array = slice_da_modificare.get_array_of_samples()
    slice_da_modificare_length = len(slice_da_modificare.get_array_of_samples())
    
    if slice_da_modificare_length < samples_per_frame:
        to_append_samples = slice_da_modificare_array[len(slice_da_modificare_array) - (samples_per_frame - len(slice_da_modificare_array)):]
        to_append = AudioSegment(data=to_append_samples.tobytes(), sample_width = original_song_R.sample_width, frame_rate = original_song_R.frame_rate, channels=1)
        slice_da_modificare = slice_da_modificare + to_append

    nonce_song = nonce_song + slice_da_modificare
    frames_edited += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame
    

nonce_song = nonce_song + original_song.get_sample_slice(end_index - samples_per_frame, original_song_sample_number)

print("Lunghezza messaggio nonce: " + str(len(nonce_bitarray)))
print("Messaggio nonce: " + str(nonce_bitarray))

echoed_song_export = AudioSegment.from_mono_audiosegments(echoed_song, nonce_song)

if not os.path.exists("output"):
    os.mkdir("output")
echoed_song_export.export('./output/echoed_song.wav', format='wav')