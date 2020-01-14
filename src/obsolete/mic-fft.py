import pyaudio
import struct
import math
import numpy as np
import scipy
import scipy.fftpack
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.animation as animation
import time
from scipy.io.wavfile import write

THRESHOLD = 0  # dB
RATE = 44100
INPUT_BLOCK_TIME = 1  # 30 ms
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)
INPUT_FRAMES_PER_BLOCK_BUFFER = int(RATE * INPUT_BLOCK_TIME)

audio = None

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def get_rms(block):
    return np.sqrt(np.mean(np.square(block)))


class AudioHandler(object):
    def __init__(self, rateTemp):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.threshold = THRESHOLD
        self.plot_counter = 0
        self.rate = rateTemp

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)
            print('Device %{}: %{}'.format(i, devinfo['name']))

            for keyword in ['mic', 'input']:
                if keyword in devinfo['name'].lower():
                    print(
                        'Found an input: device {} - {}'.format(i, devinfo['name']))
                    device_index = i
                    return device_index

        if device_index == None:
            print('No preferred input found; using default input device.')

        return device_index

    def open_mic_stream(self):
        device_index = self.find_input_device()

        stream = self.pa.open(format=self.pa.get_format_from_width(2, False),
                              channels=1,
                              rate=RATE,
                              input=True,
                              input_device_index=device_index)

        stream.start_stream()
        return stream

    def processBlock(self, snd_block):
        print(len(snd_block))
        fs_rate = self.rate
        l_audio = len(snd_block.shape)
        print(l_audio)
        print(print("Channels", l_audio))
        N = snd_block.shape[0]
        print("Complete Samplings N", N)
        secs = N / float(fs_rate)
        print("secs", secs)
        # sample interval in time
        Ts = 1.0/fs_rate
        print("Timestep between samples Ts", Ts)
        # time vector as scipy arange field / numpy.ndarray
        t = scipy.arange(0, secs, Ts)
        FFT = abs(scipy.fft(snd_block))
        FFT_side = FFT[range(N//2)]  # one side FFT range
        freqs = scipy.fftpack.fftfreq(snd_block.size, t[1]-t[0])
        fft_freqs = np.array(freqs)
        freqs_side = freqs[range(N//2)]  # one side frequency range
        fft_freqs_side = np.array(freqs_side)
        plt.subplot(311)
        p1 = plt.plot(t, snd_block, "g")  # plotting the signal
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.subplot(312)
        p2 = plt.plot(freqs, FFT, "r")  # plotting the complete fft spectrum
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Count dbl-sided')
        plt.subplot(313)
        # plotting the positive fft spectrum
        p3 = plt.plot(freqs_side, abs(FFT_side), "b")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Count single-sided')
        plt.show()

    def listen(self):
        try:
            print("start", self.stream.is_active(), self.stream.is_stopped())
            # raw_block = self.stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)

            total = 0
            t_snd_block = []
            while total < INPUT_FRAMES_PER_BLOCK:
                while self.stream.get_read_available() <= 0:
                    # print('waiting')
                    time.sleep(0.01)
                while self.stream.get_read_available() > 0 and total < INPUT_FRAMES_PER_BLOCK:
                    raw_block = self.stream.read(
                        self.stream.get_read_available(), exception_on_overflow=False)
                    count = len(raw_block) / 2
                    total = total + count
                    # print("done", total, count)
                    format = '%dh' % (count)
                    t_snd_block.append(np.fromstring(
                        raw_block, dtype=np.int16))
            snd_block = np.hstack(t_snd_block)
        except Exception as e:
            print('Error recording: {}'.format(e))
            return

        self.processBlock(snd_block)


def animate(i):
    audio.listen()


if __name__ == '__main__':
    audio = AudioHandler(RATE)
    for i in range(0, 1000):
        audio.listen()
