#!/usr/bin/env python
#coding: utf-8
# using python 2.7 Anaconda Interpreter
# Authors: Ariel Antonowicz, Marcin Lipa, Dariusz Urbański

import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

def plotGraph(filename,graphpath=None):

    rate,data = wav.read(filename)
    file = wave.open(filename, 'rb')
    nchannels, sampwidth, framerate, nframes = file.getparams()[0:4]

    data = data.astype(np.float, copy=False)

    if nchannels > 1:
        data2 = np.mean(a=data,axis=1)
        data = data2

    print "Channels: ",nchannels
    print "sampleWidth: ",sampwidth
    print "framerate: ",framerate
    print "nframes: ",nframes

    #data = data.astype(np.float, copy=False)
    #data = data / 2 ** (8 * sampwidth)

    #values= np.fft.fft(data)
    #values = np.abs(values)**2

    freq = np.fft.fftfreq(nframes,d=1./framerate)
    d = len(freq)/2
    xSize = 15
    ySize = 6

    plt.figure(figsize=(xSize, ySize))
    #test
    s = 2048
    pxx, freqs, bins, _ = plt.specgram(data, NFFT=s, Fs=rate, noverlap=0,
                                       cmap=plt.cm.binary, sides='onesided',
                                       window=np.hamming(s),
                                       scale_by_freq=True,
                                       mode='magnitude')


    plt.plot(freqs, 20 * np.log10(np.mean(pxx, axis=1)), 'g')

    #plt.plot(freq[:d],abs(values[:d]))
    plt.title("Frequency Spectrum")
    #plt.xlim(0,max_x)
    #plt.ylim(0,max_y)
    plt.xlabel("Freq [Hz]")
    plt.show()

    print "Done"

    if graphpath is None:
        plt.show()
    else:
        plt.savefig(filename,graphpath)

plotGraph(filename="./static/music/temp.wav")