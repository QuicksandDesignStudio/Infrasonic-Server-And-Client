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
import serial as sl
import wave
import sys

duration = 4
counter = 0
sample_rate = 1000

wavef = wave.open(sys.argv[0], 'w')
print(sys.argv[0])
wavef.setnchannels(1)  # mono
wavef.setsampwidth(2)
wavef.setframerate(sample_rate)

ser = sl.Serial('/dev/tty.usbserial-1410', 57600)

while(counter < (duration * sample_rate)):
    try:
        value = ser.readline()

        intData = int(value)
        # print(intData)
        data = struct.pack('<h', intData)
        wavef.writeframesraw(data)
        counter += 1
    except:
        pass

# wavef.writeframes('')
wavef.close()
