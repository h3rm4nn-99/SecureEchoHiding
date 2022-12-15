from pydub import AudioSegment
from bitarray import bitarray
from Crypto.Cipher import AES
import utils as utils
import argparse
import binascii
import sys
import os

# --- Parameters ---
# Frames to skip: 1

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--filepath_encoded', type=str, required=False)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
parser.add_argument('--message_length', type=int, required=True)
parser.add_argument('--aes_key_path', type=str, required=False)
args = parser.parse_args()

if not args.filepath_encoded is None:
    filepath_encoded = args.filepath_encoded
else:
    files = os.listdir("./output")
    last = 0
    for i in range(0, files.__len__()):
        if files[i].startswith("echoed_"):
            if os.path.getmtime("./output/" + files[i]) > os.path.getmtime("./output/" + files[last]):
                last = i
    filepath_encoded = "./output/" + files[last]
    print("Using " + filepath_encoded + " as encoded file")

if not args.aes_key_path is None:
    aes_key_path = args.aes_key_path
else:
    aes_key_path = './output/key.bin'
    
filepath = args.filepath
current_number = int(args.seed)
a_key = args.a
message_length = int(args.message_length)

f = open(aes_key_path, 'rb')
aes_key = f.read()
f.close()


samples_per_frame = 1024
frames_to_skip = 1

original_track = AudioSegment.from_wav(filepath)
original_track_channels = original_track.split_to_mono()
original_track = original_track_channels[0]
original_track_right = original_track_channels[1]

# Nonce
encoded_track = AudioSegment.from_wav(filepath_encoded)
encoded_track_channels = encoded_track.split_to_mono()
encoded_track = encoded_track_channels[0]
encoded_track_right = encoded_track_channels[1]

original_samples = original_track.get_array_of_samples()
encoded_samples = encoded_track.get_array_of_samples()

R_sequence = bitarray(message_length)

for i in range(0, message_length):
    current_number = (a_key * current_number + 2 * a_key) % message_length

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False

print("KEY DECODER " + str(R_sequence))

count = 0
binary_message = ''
start_index = 0
end_index = start_index + samples_per_frame
skip = 0
while count < message_length:
    
    if skip:
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue

    current_portion_to_analyze_original_song = original_samples[start_index:end_index]
    current_portion_to_analyze_echoed_song = encoded_samples[start_index:end_index]

    different = False
    for j in range(0, len(current_portion_to_analyze_original_song)):
        if current_portion_to_analyze_original_song[j] != current_portion_to_analyze_echoed_song[j]:
            different = True
            break
    
    if different:
        if R_sequence[count]:
            binary_message += '0'
        elif not R_sequence[count]:
            binary_message += '1'
    elif not different:
        if R_sequence[count]:
            binary_message += '1'
        elif not R_sequence[count]:
            binary_message += '0'
    count += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame

binary_message_in_bytes = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, 'big')

print("Estrazione testo cifrato completata. Estraggo ora il nonce per la decifratura")

original_samples_right = original_track_right.get_array_of_samples()
encoded_samples_right = encoded_track_right.get_array_of_samples()

N_sequence = bitarray(64) # we know that nonce is always 64 bit long so no problem here hardcoding that value

current_number = int(args.seed)
for i in range(0, 64):
    current_number = (a_key * current_number + 2 * a_key) % 64

    if current_number % 6 > 2:
        N_sequence[i] = True
    else:
        N_sequence[i] = False

count = 0
nonce_binary_string = ''
start_index = 0
end_index = start_index + samples_per_frame
skip = 0

while count < 64:
    if skip:
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue

    current_portion_to_analyze_original_song_right = original_samples_right[start_index:end_index]
    current_portion_to_analyze_echoed_song_right = encoded_samples_right[start_index:end_index]

    different = False
    for j in range(0, len(current_portion_to_analyze_original_song_right)):
        if (current_portion_to_analyze_original_song_right[j] != current_portion_to_analyze_echoed_song_right[j]):
            different = True
            break

    if different:
        if N_sequence[count]:
            nonce_binary_string += '0'
        elif not N_sequence[count]:
            nonce_binary_string += '1'
    elif not different:
        if N_sequence[count]:
            nonce_binary_string += '1'
        elif not N_sequence[count]:
            nonce_binary_string += '0'
    
    count += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame

nonce = int(nonce_binary_string, 2).to_bytes((len(nonce_binary_string) + 7) // 8, 'big')
    
decipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
plaintext = decipher.decrypt(binary_message_in_bytes)

print("Binary message: " + binary_message)
print("Decoded message: " + plaintext.decode())
