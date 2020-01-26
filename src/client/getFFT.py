from os import listdir
from os.path import isfile, join
import requests
import json
import sys
import numpy as np
import time
from matplotlib import pyplot as plt

samplePath = "samples"
analogSampleRate = '1950'
API_ENDPOINT_MAKEWAV = "http://localhost:5000/fft/api/v1.0/make_wave"
API_ENDPOINT_GETWAV = "http://localhost:5000/fft/api/v1.0/get_wave"
API_ENDPOINT_DOFFT = "http://localhost:5000/fft/api/v1.0/do_fft"
API_ENDPOINT_DOFFTSAMPLE = "http://localhost:5000/fft/api/v1.0/do_fft_from_sample"
API_ENDPOINT_ESP = "http://192.168.4.1/"
API_ENDPOINT_ESP_GETALLSAMPLES = API_ENDPOINT_ESP + "list"
API_ENDPOINT_ESP_DELETESAMPLE = API_ENDPOINT_ESP + "delete"


def main():
    argument = True

    # check if there was a user input
    try:
        sys.argv[1]
    except:
        argument = False

    if(argument == False):
        print("This script requires a user input \nTry getwaves, getFFT, getFFTsample or makewave")
    else:
        if(sys.argv[1] == "getwaves"):
            r = requests.get(url=API_ENDPOINT_GETWAV)
            allWaves = json.loads(r.text)
            print(allWaves)
            # print(allWaves[0])

        elif(sys.argv[1] == "getFFT"):
            payload = sys.argv[2]
            r = requests.post(url=API_ENDPOINT_DOFFT, data=payload)
            returnLoad = json.loads(r.text)
            plotfft(returnLoad)

        elif(sys.argv[1] == "getFFTsample"):
            f = open("samples/"+sys.argv[2])
            payload = {'sampling_rate': analogSampleRate, 'samples': f.read()}
            r = requests.post(url=API_ENDPOINT_DOFFTSAMPLE,
                              data=json.dumps(payload))
            returnLoad = json.loads(r.text)
            plotfft(returnLoad)

        elif(sys.argv[1] == "makewave"):
            f = open("samples/"+sys.argv[2])
            payload = {'file_name': sys.argv[3],
                       'sampling_rate': analogSampleRate, 'samples': f.read()}
            r = requests.post(url=API_ENDPOINT_MAKEWAV,
                              data=json.dumps(payload))
            print(r.text)

        elif(sys.argv[1] == "getsamples"):
            r = requests.get(url=API_ENDPOINT_ESP_GETALLSAMPLES)
            allsamples = json.loads(r.text)
            saveallsamples(allsamples)

        elif(sys.argv[1] == "listlocalsamples"):
            allSamples = [f for f in listdir(
                samplePath) if isfile(join(samplePath, f))]
            for i in allSamples:
                if(i != ".DS_Store"):
                    print(i)

        elif(sys.argv[1] == "listremotesamples"):
            r = requests.get(url=API_ENDPOINT_ESP_GETALLSAMPLES)
            allsamples = json.loads(r.text)
            for entry in allsamples:
                print(entry["name"])

        elif(sys.argv[1] == "deletesample"):
            r = requests.get(
                url=API_ENDPOINT_ESP_DELETESAMPLE+"?path=/"+sys.argv[2])
            print(r.text)
        elif(sys.argv[1] == "deleteallsamples"):
            r = requests.get(url=API_ENDPOINT_ESP_GETALLSAMPLES)
            allsamples = json.loads(r.text)
            deleteallsamples(allsamples)


def plotfft(fftdata):
    timeVector = np.array(fftdata["timeVector"])
    signal = np.array(fftdata["signal"])
    fullPhaseFrequencies = np.array(fftdata["fullPhaseFrequencies"])
    fullPhaseFFT = np.array(fftdata["fullPhaseFFT"])
    positiveFrequencies = np.array(fftdata["positiveFrequencies"])
    positiveFFT = np.array(fftdata["positiveFFT"])

    # remove random spike
    positiveFFT[0] = 0
    fullPhaseFFT[0] = 0

    # plotting the signal
    plt.subplot(311)
    p1 = plt.plot(timeVector, signal, "g")
    try:
        sys.argv[2]
        plt.title(sys.argv[2])
    except:
        plt.xlabel('Time')

    plt.ylabel('Amplitude')

    # plotting the complete fft spectrum
    plt.subplot(312)
    p2 = plt.plot(fullPhaseFrequencies, fullPhaseFFT, "r")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count dbl-sided')

    # plotting the positive fft spectrum
    plt.subplot(313)
    p3 = plt.plot(positiveFrequencies, positiveFFT, "b")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')

    plt.show()


def saveallsamples(allsamples):
    for entry in allsamples:
        r = requests.get(url=API_ENDPOINT_ESP+entry["name"])
        returnLoad = r.text
        sample = returnLoad[:-1]
        fileName = "samples/" + entry["name"] + ".txt"
        sampleBroken = sample.split(",")
        sampleBroken = [int(numeric_string)
                        for numeric_string in sampleBroken]
        filteredSample = ""
        for i in sampleBroken:
            if(i < 1900 and i > 1200):
                filteredSample += str(i) + ","
            else:
                filteredSample += str(int(Average(sampleBroken))) + ","
        filteredSample = filteredSample[:-1]
        with open(fileName, 'w') as f:
            print(fileName)
            f.write(filteredSample)
        """
        returnload = json.loads(r.text)
        sample = returnload["data"]
        fileName = "samples/" + entry["name"] + ".txt"
        print(fileName)
        with open(fileName, 'w') as f:
            counter = 0
            for item in sample:
                if(counter == len(sample) - 1):
                    f.write(str(item))
                else:
                    f.write(str(item)+",")
                counter += 1
        """


def deleteallsamples(allsamples):
    for entry in allsamples:
        r = requests.get(url=API_ENDPOINT_ESP_DELETESAMPLE +
                         "?path=/"+entry["name"])
        print(r.text)


def Average(lst):
    return sum(lst) / len(lst)


if __name__ == "__main__":
    main()
