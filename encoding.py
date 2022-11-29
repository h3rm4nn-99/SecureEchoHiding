from pydub import AudioSegment
import bitarray
import sys
import fileinput
import argparse


## insert parsing here
#a_key #seed #msg #filepath 


def next_key_chunk(current_key_chunk,a_key):
    return (a_key * current_key_chunk + 2 * a_key)

def gen_r_sequence(sequence_length):
    R_sequence = bitarray(sequence_length)
    for i in range():
        next_key_chunk = next_key_chunk(current_key_chunk, a_key)
        if next_key_chunk % 6 > 2:
            R_sequence[i] = True
        elif next_key_chunk % 6 <=2:
            R_sequence[i] = False
    return R_sequence


samples_per_slice=5000 #tbd #controllare da header mp3 quando si va a leggere?


msg_bitarray = bitarray()
msg_bitarray.fromstring(msg)

msg_length = len(msg_bitarray)

current_key_chunk = seed 

r_sequence = gen_r_sequence(msg_length)

original_track = AudioSegment.from_file(filepath, format="mp3")
echoed_track = AudioSegment.empty()

echo_loudness = -10 #dB

echo_delay = 1 #50ms????????????????????????????????????????????????? WTH??????

n_frames = int(original_track.frame_count())

available_bits= n_frames/samples_per_slice  ##?????

if(available_bits < msg_length):
    print("Error?")
    sys.exit(0)

count = 0
for i in range (0,msg_length):
    