from os import listdir
from os.path import isfile, join
import requests
import json

samplePath = "samples"
API_ENDPOINT = "http://localhost:5000/fft/api/v1.0/make_wave"


def main():
    f = open("samples/sample.txt")
    payload = {'file_name': 'gube.wav',
               'sampling_rate': '1100', 'samples': f.read()}
    r = requests.post(url=API_ENDPOINT, data=json.dumps(payload))

    print(r.text)

    """
    allSamples = [f for f in listdir(
        samplePath) if isfile(join(samplePath, f))]

    payload = {'file_name': 'gube.wav',
               'sampling_rate': '1100', 'samples': '247,248'}
    r = requests.post(url=API_ENDPOINT, data=json.dumps(payload))

    print(r.text)
    """


if __name__ == "__main__":
    main()
