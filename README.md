# Infrsonic Server And Client

This Repo has three components

**Flask Server - With the Following APIs**
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
