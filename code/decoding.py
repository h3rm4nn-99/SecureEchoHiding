from pydub import AudioSegment
from bitarray import bitarray
import utils as utils
import argparse
import binascii
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--filepath_encoded', type=str, required=False)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
parser.add_argument('--message_length', type=int, required=True)
parser.add_argument('--aes_key', type=str, required=True)
args = parser.parse_args()

if not args.filepath_encoded is None:
    filepath_encoded = args.filepath_encoded
else:
    filepath_encoded = './output/echoed_song.wav'
    
filepath = args.filepath
current_number = int(args.seed)
a_key = args.a
message_length = int(args.message_length)
aes_key = args.aes_key

if len(aes_key) > 16:
    aes_key = aes_key[0:16]
elif len(aes_key) < 16:
    print("La chiave proposta non risulta essere di 128 bit o più. Uscita")
    sys.exit(0)

samples_per_frame = 1024
frames_to_skip = 2

original_track = AudioSegment.from_wav(filepath)
original_track_nonce = original_track.split_to_mono()[1]
original_track = original_track.split_to_mono()[0]
encoded_track = AudioSegment.from_wav(filepath_encoded)
encoded_track_nonce = encoded_track.split_to_mono()[1]
encoded_track = encoded_track.split_to_mono()[0]

original_samples = original_track.get_array_of_samples()
encoded_samples = encoded_track.get_array_of_samples()

original_samples_nonce = original_track_nonce.get_array_of_samples()
encoded_samples_nonce = encoded_track_nonce.get_array_of_samples()

R_sequence = bitarray(message_length)
N_sequence = bitarray(64) # nonce is always 64 bits

for i in range(0, message_length):
    current_number = (a_key * current_number + 2 * a_key) % message_length

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False

current_number = int(args.seed)
for i in range(0, 64):
    current_number = (a_key * current_number + 2 * a_key) % message_length

    if current_number % 6 > 2:
        N_sequence[i] = True
    else:
        N_sequence[i] = False

print("KEY DECODER " + str(R_sequence))
print("Nonce decoder key " + str(N_sequence))

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

count = 0
binary_message_nonce = ''
start_index = 0
end_index = start_index + samples_per_frame
skip = 0
while count < 64:
    
    if skip:
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue

    current_portion_to_analyze_original_song_nonce = original_samples_nonce[start_index:end_index]
    current_portion_to_analyze_echoed_song_nonce = encoded_samples_nonce[start_index:end_index]

    different = False
    for j in range(0, len(current_portion_to_analyze_original_song_nonce)):
        if current_portion_to_analyze_original_song_nonce[j] != current_portion_to_analyze_echoed_song_nonce[j]:
            different = True
            break
    
    if different:
        if N_sequence[count]:
            binary_message_nonce += '0'
        elif not N_sequence[count]:
            binary_message_nonce += '1'
    elif not different:
        if N_sequence[count]:
            binary_message_nonce += '1'
        elif not N_sequence[count]:
            binary_message_nonce += '0'
    count += 1
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame

print(binary_message)
print()
print()
print(binary_message_nonce)

binary_int = int(binary_message, 2)
byte_number = binary_int.bit_length() + 7 // 8
binary_array = binary_int.to_bytes(byte_number, "big")
ascii_message = binary_array.decode()

print("Messaggio binario: " + binary_message)
print("Messaggio decodificato: " + ascii_message)