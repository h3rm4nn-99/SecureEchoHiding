from pydub import AudioSegment
from bitarray import bitarray
import fileinput
import argparse
import utils
import numpy
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--filepath_encoded', type=str, required=True)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
args = parser.parse_args()

filepath = args.filepath
filepath_encoded = args.filepath_encoded
seed = args.seed
a_key = args.a

samples_per_slice = 5000

original_track = AudioSegment.from_wav(filepath)
encoded_track = AudioSegment.from_wav(filepath_encoded)

original_samples = original_track.get_array_of_samples()
encoded_samples = encoded_track.get_array_of_samples()

message_length = len(original_samples) / samples_per_slice # lunghezza massima

r_sequence = utils.gen_r_sequence(message_length, seed, a_key)

message = ""
for i in range (0, len(original_samples), samples_per_slice):
    if original_samples[i] != encoded_samples[i]:
        if r_sequence[i]:
            message += "1"
        else:
            message += "0"

print("Messaggio decodificato: " + message)

