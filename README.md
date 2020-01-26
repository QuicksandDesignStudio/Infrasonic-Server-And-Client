# Infrsonic Server And Client

This Repo has three components

**1. Flask Server - With the Following API Hooks**  
_For instructions on how to use these methods please look at the documented code in app.py_

    1. /fft/api/v1.0/make_wave
    POST - Make a wave (.wav) from raw sound sensor (mic) samples

    2. /fft/api/v1.0/get_wave
    GET - Get names of all the waves on the server

    3. /fft/api/v1.0/do*fft
    POST - Do an FFT analysis with a wave already on the server.
    *For details on the returned FFT object, please look at hte documented code in app.py\*

    4. /fft/api/v1.0/do_fft_from_sample
    POST - Do an FFT analysis with raw sample data sent to the server as post

**2. Client API - With the following Hooks**
_For instructions on how to use these methods please look at the documented code in getFFT.py. The simple HTTP requests and some drawing methods in getFFT.py are for illustration purposes. Feel free to rewrite these in any environment that may be relevant. It should be very easy to port._

    1. getwaves
    _Get all the waves stored on the server - interfaces with the second API hook above_

    2. getFFT
    _Get FFT of a wave file already stored on the server - interfaces with the third hook above_

    3. getFFTsample
    _Get FFT of raw sounds samples - interfaces with the fourth book above_

    4. makewave
    _Make a wave (.wav) from raw sound samples - interfaces with the first hook above_

    _The hooks below are a) some helper hooks for local file handling and b) interfacing with the ESP32 server on the hardware side. For details on the hardware code (Arduino, C) please visit https://github.com/QuicksandDesignStudio/Infrasonic_hardware_

    5. getsamples
    _Get all sampels stored in a ESP32 server_

    6. listlocalsamples
    _List all the samples that are stored locally_

    7. listremotesamples
    _List all the samples on the ESP32 server_

    8. deletesample
    _Delete a specific sample from the ESP32 server_

    9. deleteallsamples
    _Delete all samples from the ESP32 server_
