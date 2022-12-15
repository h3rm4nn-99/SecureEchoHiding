import scipy.io.wavfile as wavfile
import numpy as np
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
args = parser.parse_args()
file = args.file

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)


if (os.path.isfile(file)):
    data = wavfile.read(file)[1]
    singleChannel = data
    try:
        singleChannel = np.sum(data, axis=1)
    except:
        pass

    norm = singleChannel / (max(np.amax(singleChannel), -1 * np.amin(singleChannel)))
    print(signaltonoise(norm))