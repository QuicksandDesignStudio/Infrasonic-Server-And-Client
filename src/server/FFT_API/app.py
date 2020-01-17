from __future__ import print_function
from os import listdir
from os.path import isfile, join

from flask import Flask
from flask import request
from flask_cors import CORS

import sys
import struct
import math
import wave
import json

import scipy
import scipy.io.wavfile as wavfile
import scipy.fftpack

import numpy as np


app = Flask(__name__)
CORS(app)

wavePath = "waves"


@app.route('/fft/api/v1.0/make_wave', methods=['POST'])
def make_wave():
    payload = json.loads(request.get_data().decode('utf8').replace("'", '"'))
    fileName = payload["file_name"]
    samplingRate = payload["sampling_rate"]
    samples = payload["samples"].split(",")

    wavef = wave.open(fileName, 'w')
    wavef.setnchannels(1)  # mono
    wavef.setsampwidth(2)
    wavef.setframerate(int(samplingRate))

    for i in samples:
        intData = int(i)
        data = struct.pack('<h', intData)
        wavef.writeframesraw(data)

    wavef.close()
    return "File Saved!"


@app.route('/fft/api/v1.0/get_wave', methods=['GET'])
def get_wave():
    allSamples = [f for f in listdir(
        wavePath) if isfile(join(wavePath, f))]
    return json.dumps(allSamples)


@app.route('/fft/api/v1.0/do_fft', methods=['POST'])
def do_fft():
    print("Doing FFT with a wave")
    fileName = "waves/" + request.get_data().decode('utf-8')
    fs_rate, signal = wavfile.read(fileName)
    print(signal)
    print("Frequency sampling", fs_rate)

    l_audio = len(signal.shape)
    print("Channels", l_audio)
    if l_audio == 2:
        signal = signal.sum(axis=1) / 2

    N = signal.shape[0]
    print("Complete Samplings N", N)
    secs = N / float(fs_rate)
    print("secs", secs)
    Ts = 1.0/fs_rate
    print("Timestep between samples Ts", Ts)

    # time vector as scipy arange field / numpy.ndarray
    t = scipy.arange(0, secs, Ts)

    FFT = abs(scipy.fft(signal))
    FFT_side = FFT[range(N//2)]  # one side FFT range

    freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
    freqs_side = freqs[range(N//2)]  # one side frequency range

    returnLoad = {'timeVector': t.tolist(), 'signal': signal.tolist(), 'fullPhaseFrequencies': freqs.tolist(),
                  'fullPhaseFFT': FFT.tolist(), 'positiveFrequencies': freqs_side.tolist(), 'positiveFFT': abs(FFT_side).tolist()}

    return json.dumps(returnLoad)


@app.route('/fft/api/v1.0/do_fft_from_sample', methods=['POST'])
def do_fft_from_sample():
    print("Doing FFT with a sample")
    payload = json.loads(request.get_data().decode('utf8').replace("'", '"'))
    fs_rate = int(payload["sampling_rate"])

    # the incoming samples need to be cast to string
    signalRaw = payload["samples"].split(",")
    print(int(" 300"))
    signal = np.array(list(map(int, signalRaw)))

    print("Frequency sampling", fs_rate)

    l_audio = len(signal.shape)
    print("Channels", l_audio)
    if l_audio == 2:
        signal = signal.sum(axis=1) / 2

    N = signal.shape[0]
    print("Complete Samplings N", N)
    secs = N / float(fs_rate)
    print("secs", secs)
    Ts = 1.0/fs_rate
    print("Timestep between samples Ts", Ts)

    # time vector as scipy arange field / numpy.ndarray
    t = scipy.arange(0, secs, Ts)

    FFT = abs(scipy.fft(signal))
    FFT_side = FFT[range(N//2)]  # one side FFT range

    freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
    freqs_side = freqs[range(N//2)]  # one side frequency range

    returnLoad = {'timeVector': t.tolist(), 'signal': signal.tolist(), 'fullPhaseFrequencies': freqs.tolist(),
                  'fullPhaseFFT': FFT.tolist(), 'positiveFrequencies': freqs_side.tolist(), 'positiveFFT': abs(FFT_side).tolist()}

    return json.dumps(returnLoad)


if __name__ == '__main__':
    app.run(debug=True)
