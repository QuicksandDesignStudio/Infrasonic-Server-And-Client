from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd


class serialPlot:
    def __init__(self, serialPort='/dev/ttyUSB0', serialBaud=38400, plotLength=100, dataNumBytes=2):
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.rawData = bytearray(dataNumBytes)
        self.data = collections.deque([0] * plotLength, maxlen=plotLength)
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        # self.csvData = []

        print('Trying to connect to: ' + str(serialPort) +
              ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(
                serialPort, serialBaud, timeout=4)
            print('Connected to ' + str(serialPort) +
                  ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) +
                  ' at ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self):
        currentTimer = time.perf_counter()
        # the first reading will be erroneous
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)
        self.previousTimer = currentTimer
        # use 'h' for a 2 byte integer
        value,  = struct.unpack('f', self.rawData)
        # we get the latest data point and append it to our array
        self.data.append(value)
        nvalues = np.array(self.data)
        return nvalues

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            # print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')
        # df = pd.DataFrame(self.csvData)
        # df.to_csv('/home/rikisenia/Desktop/data.csv')


def animate(i):
    global ax1
    global s
    global baudRate

    signal = s.getSerialData()
    print(signal)

    fs_rate = baudRate
    l_audio = len(signal.shape)
    print(print("Channels", l_audio))
    N = signal.shape[0]
    print("Complete Samplings N", N)
    secs = N / float(fs_rate)
    print("secs", secs)
    # sample interval in time
    Ts = 1.0/fs_rate
    print("Timestep between samples Ts", Ts)
    # time vector as scipy arange field / numpy.ndarray
    t = scipy.arange(0, secs, Ts)
    FFT = abs(scipy.fft(signal))
    FFT_side = FFT[range(N//2)]  # one side FFT range
    freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
    fft_freqs = np.array(freqs)
    freqs_side = freqs[range(N//2)]  # one side frequency range
    fft_freqs_side = np.array(freqs_side)

    ax1.clear()
    ax1.plot(freqs, FFT, "r")


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# portName = 'COM5'     # for windows users
portName = '/dev/tty.usbserial-1460'
baudRate = 38400
maxPlotLength = 100
dataNumBytes = 4        # number of bytes of 1 data point

# initializes all required variables
s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes)
# starts background thread
s.readSerialStart()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()


s.close()
