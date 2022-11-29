from pydub import AudioSegment
import utility
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', type=str, required=True)
args = parser.parse_args()

filepath = args.filepath

samples_per_slice = 5000

original_track = AudioSegment.from_mp3(filepath)
original_track_mono = original_track.split_to_mono()
left_channel_track = original_track_mono[0]
left_channel_samples = left_channel_track.get_array_of_samples()

number_of_frames = original_track.frame_count()
available_bits= number_of_frames / samples_per_slice

count = 0
counter_to_8 = 0

for i in range (0, available_bits):
    e_values = extract_e(count, i, left_channel_samples)

    Emin = e_values[0][0]
    Emid = e_values[1][0]
    Emax = e_values[2][0]

    A = Emax - Emin
    B = Emid - Emin

    if A >= B:
        print("1", end="")
    if B > A:
        print("0", end="")

    count += samples_per_slice

    if counter_to_8 == 7:
        print("")
        counter_to_8 = 0
    else:
        counter_to_8 += 1


