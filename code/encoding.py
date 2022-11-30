from pydub import AudioSegment
from bitarray import bitarray
import utils as utils
import sys
import fileinput
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--message', type=str, required=True)
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
args = parser.parse_args()

msg = args.message
filepath = args.filepath
seed = args.seed
a_key = args.a

echo_loudness = -10 #dB
echo_delay = 1 #50ms
samples_per_slice = 5000

message_bitarray = bitarray()
message_bitarray.frombytes(msg.encode('utf-8'))
message_length = len(message_bitarray)

r_sequence = utils.gen_r_sequence(message_length, seed, a_key)

original_track = AudioSegment.from_mp3(filepath)
echoed_track = AudioSegment.empty()

number_of_frames = int(original_track.frame_count())
available_bits= number_of_frames / samples_per_slice

if available_bits < message_length:
    print("Non ci sono abbastanza bit disponiili per nascondere un messaggio di lunghezza " + str(message_length))
    sys.exit(0)

count = 0
for i in range (0, message_length):
    current_slice_start = i * samples_per_slice
    current_slice_end = (i + 1) * samples_per_slice
    count += samples_per_slice

    slice_to_process = AudioSegment(original_track).get_sample_slice(current_slice_start, current_slice_end)

    processed_slice = None
    if r_sequence[i]:
        if message_bitarray[i]:
            processed_slice = slice_to_process.get_array_of_samples()
        else:
            processed_slice = slice_to_process.overlay(slice_to_process.apply_gain(echo_loudness), position=echo_delay)
            processed_slice = processed_slice.get_array_of_samples()
    else:
        if message_bitarray[i]:
            processed_slice = slice_to_process.overlay(slice_to_process.apply_gain(echo_loudness), position=echo_delay)
            processed_slice = processed_slice.get_array_of_samples()
        else:
            processed_slice = slice_to_process.get_array_of_samples()
    
    echoed_track = echoed_track + AudioSegment(original_track)._spawn(processed_slice)

# i samples residui vengono lasciati intatti e ricopiati nella traccia audio modificata

echoed_track = echoed_track + AudioSegment(original_track).get_sample_slice(count, number_of_frames)
echoed_track.export("./output/echoed_track.wav", format='wav')

sys.exit(0)