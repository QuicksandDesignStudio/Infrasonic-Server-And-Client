# eventually we should not need to store a wav at all, we should be able to directly do FFT with the data
# this is only a temp step

import serial
import wave
import struct
import math
import sys
import time
import threading

sampleRate = 44100.0  # hertz
duration = 5     # seconds
frequency = 440.0    # hertz

wavef = wave.open('sound6.wav', 'w')
wavef.setnchannels(1)  # mono
wavef.setsampwidth(2)
wavef.setframerate(sampleRate)

ser = serial.Serial('/dev/tty.usbserial-1460')
ser.flushInput()


def mytimer():
    wavef.writeframes('')
    wavef.close()
    ser.close()


my_timer = threading.Timer(duration, mytimer)
my_timer.start()

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
        data = struct.pack('<h', decoded_bytes)
        wavef.writeframesraw(data)
    except:
        break
