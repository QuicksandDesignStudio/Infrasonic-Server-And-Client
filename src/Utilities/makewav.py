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
sample_rate = 2000


wavef = wave.open(sys.argv[1], 'w')
wavef.setnchannels(1)  # mono
wavef.setsampwidth(2)
wavef.setframerate(sample_rate)

ser = sl.Serial('/dev/tty.SLAB_USBtoUART', 115200)

while(counter < (duration * sample_rate)):
    try:
        value = ser.readline()

        intData = int(value)
        data = struct.pack('<h', intData)
        wavef.writeframesraw(data)
        counter += 1
    except:
        pass

# wavef.writeframes('')
wavef.close()
