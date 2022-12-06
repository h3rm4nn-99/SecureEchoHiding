from pydub import AudioSegment
from bitarray import bitarray
from Crypto.Cipher import AES
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
parser.add_argument('--aes_key_path', type=str, required= True)
parser.add_argument('--nonce_path', type=str, required= True)
args = parser.parse_args()

if not args.filepath_encoded is None:
    filepath_encoded = args.filepath_encoded
else:
    filepath_encoded = './output/echoed_song.wav'
    
filepath = args.filepath
current_number = int(args.seed)
a_key = args.a
message_length = int(args.message_length)
aes_key_path = args.aes_key_path
nonce_path = args.nonce_path

f = open(aes_key_path, 'rb')
aes_key = f.read()
f.close()

f = open(nonce_path, 'rb')
nonce = f.read()
f.close()

samples_per_frame = 1024
frames_to_skip = 1

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
start_index = 0
end_index = start_index + samples_per_frame
skip = 0
while count < message_length:
    
    if skip:
        skip = (skip + 1) % (frames_to_skip + 1)
        start_index = end_index
        end_index = end_index + samples_per_frame

        continue

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
    skip = (skip + 1) % (frames_to_skip + 1)
    start_index = end_index
    end_index = end_index + samples_per_frame

decipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
binary_message_in_bytes = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, 'big')

plaintext = decipher.decrypt(binary_message_in_bytes)

print("Messaggio binario: " + binary_message)
print("Messaggio decodificato: " + plaintext.decode('utf-8'))
