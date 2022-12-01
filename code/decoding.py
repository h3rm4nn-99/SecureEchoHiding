from pydub import AudioSegment
from bitarray import bitarray
import argparse
import utils as utils
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--filepath_encoded', type=str, required=True)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
parser.add_argument('--message_length', type=int, required=True)
args = parser.parse_args()

filepath = args.filepath
filepath_encoded = args.filepath_encoded
current_number = int(args.seed)
a_key = args.a
message_length = int(args.message_length)

samples_per_frame = 1024

original_track = AudioSegment.from_wav(filepath)
encoded_track = AudioSegment.from_wav(filepath_encoded)

original_samples = original_track.get_array_of_samples()
encoded_samples = encoded_track.get_array_of_samples()

print("Lunghezza traccia originale " + str(len(original_samples)))
print("Lunghezza traccia modificata " + str(len(encoded_samples)))

# count = 0
# leng = 0
# for i in range(0, len(original_samples)):
#     leng += 1
#     if original_samples[i] != encoded_samples[i]:
#         print("hit")
#         count += 1

# print(leng)
# print(count)

R_sequence = bitarray(message_length)

for i in range(0, message_length):
    current_number = (a_key * current_number + 2 * a_key) % message_length

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False

print("KEY DECODER " + str(R_sequence))

count = 0
cleartext_message = ''
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
            cleartext_message += '0'
        elif not R_sequence[count]:
            cleartext_message += '1'
    elif not different:
        if R_sequence[count]:
            cleartext_message += '1'
        elif not R_sequence[count]:
            cleartext_message += '0'
    count += 1

print("messaggio " + cleartext_message)