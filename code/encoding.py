from pydub import AudioSegment
from bitarray import bitarray
import argparse
import sys
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

samples_per_frame = 1024

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

print("KEY ENCODER " + str(R_sequence))

echoed_song = AudioSegment.empty()
original_song = AudioSegment.from_wav(filepath)
original_song_R = original_song.split_to_mono()[1]
original_song = original_song.split_to_mono()[0]


loudness = -20
delay = 2

original_song_frame_number = int(len(original_song.get_array_of_samples()))
available_bits = original_song_frame_number / samples_per_frame

if (available_bits < frame_da_modificare):
    print("Non sono disponibili abbastanza frame per nascondere il messaggio")
    sys.exit(0)

count = 0
for i in range(0, frame_da_modificare):
    start_index = i * samples_per_frame
    end_index = (i+1) * samples_per_frame
    count += samples_per_frame
    
    frame_da_modificare = original_song.get_sample_slice(start_index, end_index)
    
    if R_sequence[i]:
        if not message_bitarray[i]:
            frame_da_modificare = frame_da_modificare.overlay(frame_da_modificare.apply_gain(loudness), position=delay)
    else:
        if message_bitarray[i]:
            frame_da_modificare = frame_da_modificare.overlay(frame_da_modificare.apply_gain(loudness), position=delay)
    
    frame_da_modificare_array = frame_da_modificare.get_array_of_samples()
    frame_da_modificare_length = len(frame_da_modificare.get_array_of_samples())
    
    if frame_da_modificare_length < samples_per_frame:
        to_append_samples = frame_da_modificare_array[len(frame_da_modificare_array) - (samples_per_frame - len(frame_da_modificare_array)):]
        to_append = AudioSegment(data=to_append_samples.tobytes(), sample_width = original_song.sample_width, frame_rate = original_song.frame_rate, channels=1)
        frame_da_modificare = frame_da_modificare + to_append

    echoed_song = echoed_song + frame_da_modificare
    

echoed_song = echoed_song + original_song.get_sample_slice(count, original_song_frame_number)

print("Lunghezza traccia originale " + str(len(original_song.get_array_of_samples())) + " samples, " + str(len(original_song)) + " ms")
print("Lunghezza traccia modificata " + str(len(echoed_song.get_array_of_samples())) + " samples, " + str(len(echoed_song)) + " ms")

print("Lunghezza messaggio: " + str(len(message_bitarray)))
print("Messaggio: " + str(message_bitarray))

echoed_song_export = AudioSegment.from_mono_audiosegments(echoed_song, original_song_R)

if not os.path.exists("output"):
    os.mkdir("output")
echoed_song_export.export('./output/echoed_song.wav', format='wav')