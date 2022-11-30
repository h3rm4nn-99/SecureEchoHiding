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
args = parser.parse_args()

filepath = args.filepath
filepath_encoded = args.filepath_encoded
current_number = args.seed
a_key = args.a

samples_per_frame = 5000

original_track = AudioSegment.from_wav(filepath)
encoded_track = AudioSegment.from_wav(filepath_encoded)

original_samples = original_track.get_array_of_samples()
encoded_samples = encoded_track.get_array_of_samples()

count = 0
leng = 0
initialIndex = 999
finalIndex = 0
for i in range(0, len(original_samples), samples_per_frame):
    if leng < 32:
        if original_samples[i] != encoded_samples[i]:
            if initialIndex == 999:
                initialIndex = i
            finalIndex = i
            #print("originale " + str(i) + " value: " + str(original_samples[i]))
            #print("modificato " + str(i) + " value: " + str(encoded_samples[i]))
            count += 1
            leng += 1

R_sequence = bitarray(leng)
for i in range(0, leng):
    current_number = (a_key * current_number + 2*a_key) % leng

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False

print(str(R_sequence))

count = 0
binary_message = ""
for i in range(initialIndex, finalIndex, samples_per_frame):
    if count <= leng:
            if R_sequence[count]:
                binary_message += "1"
            else:
                binary_message += "0"
    count += 1

print(binary_message)
