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
current_number = args.seed
a_key = args.a
message_length = args.message_length

samples_per_frame = 1024

original_track = AudioSegment.from_wav(filepath)
encoded_track = AudioSegment.from_wav(filepath_encoded)

original_samples = original_track.get_array_of_samples()
encoded_samples = encoded_track.get_array_of_samples()

print("Lunghezza traccia originale " + str(len(original_samples)))
print("Lunghezza traccia modificata " + str(len(encoded_samples)))

count = 0
leng = 0
for i in range(0, len(original_samples)):
    leng += 1
    if original_samples[i] != encoded_samples[i]:
        print("hit")
        count += 1

print(leng)
print(count)

R_sequence = bitarray(message_length)

current_number = 0
for i in range(0, message_length):
    current_number = (a_key * current_number + 2*a_key) % message_length

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False

count = 0
binary_message = ""

