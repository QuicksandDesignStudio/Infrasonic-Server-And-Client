import serial
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('classic')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

xsm = 0
xs = []
ys = []

ser = serial.Serial('/dev/tty.usbserial-1440')
ser.flushInput()


def animate(i):
    global xsm
    try:
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
        ys.append(decoded_bytes)
        xs.append(xsm)
        xsm += 1
    except:
        print("error")
    ax1.clear()
    ax1.plot(xs, ys)


ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
