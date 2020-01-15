from flask import Flask
from flask import request
from flask_cors import CORS
import sys
import struct
import math
import wave
import json


app = Flask(__name__)
CORS(app)


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


@app.route('/fft/api/v1.0/make_wave', methods=['POST'])
def do_fft():
    return "this method is pending"


if __name__ == '__main__':
    app.run(debug=True)
