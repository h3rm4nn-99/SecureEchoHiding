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
args = parser.parse_args()

if not args.filepath_encoded is None:
    filepath_encoded = args.filepath_encoded
else:
    filepath_encoded = './output/echoed_song.wav'
    
filepath = args.filepath
current_number = int(args.seed)
a_key = args.a
message_length = int(args.message_length)

samples_per_frame = 1024

original_track = AudioSegment.from_wav(filepath)
original_track = original_track.split_to_mono()[0]
encoded_track = AudioSegment.from_wav(filepath_encoded)
encoded_track = encoded_track.split_to_mono()[0]

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
i = 0
while count < message_length:
    start_index = i * samples_per_frame
    end_index = (i + 1) * samples_per_frame
    i += 1

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

binary_int = int(binary_message, 2)
byte_number = binary_int.bit_length() + 7 // 8
binary_array = binary_int.to_bytes(byte_number, "big")
ascii_message = binary_array.decode()

print("Messaggio binario: " + binary_message)
print("Messaggio decodificato: " + ascii_message)