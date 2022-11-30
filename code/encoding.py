from pydub import AudioSegment
from bitarray import bitarray
import sys
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--message', type=str, required=True)
parser.add_argument('--filepath', type=str, required=True)
parser.add_argument('--seed', type=int, required=True)
parser.add_argument('--a', type=int, required=True)
args = parser.parse_args()

current_number = args.seed
a_key = int(args.a) 
filepath = args.filepath
message = args.message

samples_per_frame = 5000

message_size = len(message)

message_bitarray = bitarray()
message_bitarray.frombytes(message.encode('utf-8'))
frame_da_modificare = len(message_bitarray)
R_sequence = bitarray(frame_da_modificare)

for i in range(0, frame_da_modificare):
    current_number = (a_key * current_number + 2*a_key) % frame_da_modificare

    if current_number % 6 > 2:
        R_sequence[i] = True
    else:
        R_sequence[i] = False
print("ERRE " + str(len(R_sequence)))
print(str(R_sequence))

echoed_song = AudioSegment.empty()
original_song = AudioSegment.from_wav(filepath)

loudness = -10
delay = 1

original_song_frame_number = int(original_song.frame_count())
available_bits = original_song_frame_number / samples_per_frame

if (available_bits < frame_da_modificare):
    print("Non sono disponibili abbastanza frame per nascondere il messaggio")
    sys.exit(0)

count = 0
for i in range(0, frame_da_modificare):
    start_index = i * samples_per_frame
    end_index = (i+1) * samples_per_frame
    count += samples_per_frame

    porzione_eco = original_song.get_sample_slice(start_index, end_index)
    if i < frame_da_modificare:
        if R_sequence[i]:
            if message_bitarray[i]:
                echoed = porzione_eco.get_array_of_samples()
            else:
                echoed = porzione_eco.overlay(porzione_eco.apply_gain(loudness), position=delay)
                echoed = echoed.get_array_of_samples()
        else:
            if message_bitarray[i]:
                echoed = porzione_eco.overlay(porzione_eco.apply_gain(loudness), position=delay)
                echoed = echoed.get_array_of_samples()
            else:
                echoed = porzione_eco.get_array_of_samples()
        echoed_song = echoed_song + original_song._spawn(echoed)

echoed_song = echoed_song + original_song.get_sample_slice(count, original_song_frame_number)
echoed_song.export('echoed_song.wav', format='wav')
