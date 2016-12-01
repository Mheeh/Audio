#!/usr/bin/env python
#coding: utf-8
# using python 2.7 Anaconda Interpreter
# Authors: Ariel Antonowicz, Marcin Lipa, Dariusz Urbański

import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.signal as signal

def plotGraph(filename,graphpath=None):

    rate,data = wav.read(filename)
    file = wave.open(filename, 'rb')
    nchannels, sampwidth, framerate, nframes = file.getparams()[0:4]

    data = data.astype(np.float, copy=False)
    #normalization
    data = data / (2 ** (8 * sampwidth))

    if nchannels > 1:
        data2 = np.mean(a=data,axis=1)
        data = data2

    print "Channels: ",nchannels
    print "sampleWidth: ",sampwidth
    print "framerate: ",framerate
    print "nframes: ",nframes



    #freq = np.fft.fftfreq(nframes,d=1./framerate)
    #d = len(freq)/2
    xSize = 15
    ySize = 6

    plt.figure(figsize=(xSize, ySize))
    #test
    #s = 2048
    windowing = False

    windowsize = 512

    window = signal.get_window('hann',windowsize)
    if windowing:
        data = signal.convolve(data, window, mode='same') / sum(window)


    freqbin = np.linspace(-framerate/2,framerate/2,nframes)
    #freqbin[-1] = 0

    fft = np.fft.fft(data)
    sfft = np.fft.fftshift(fft)


    #fft = np.real(fft)*np.real(fft)+np.imag(fft)*np.imag(fft)
    #fft = 10*np.log10(fft)

    plt.plot(freqbin[len(freqbin)/2+1:],np.abs(sfft)[len(sfft)/2+1:])
    #plt.show()

    # values= np.fft.fft(data)
    # values = np.abs(values)**2



    #pxx, freqs, bins, _ = plt.specgram(data, NFFT=windowsize, Fs=rate, noverlap=0,
     #                                  cmap=plt.cm.binary, sides='onesided',
      #                                 window=signal.blackmanharris(windowsize),
       #                                scale_by_freq=True,
        #                               mode='magnitude')

    #pxx, freqs, bins, _ = signal.spectrogram()
    #plt.plot(freqs, 20 * np.log10(np.mean(pxx, axis=1)), 'g')

    #pxx = np.mean(pxx, axis=1)
    #pxx = np.log10(pxx)
    #pxx = 20*pxx
    #plt.plot(freqs[1:],pxx[1:])

    #plt.plot(freq[:d],abs(values[:d]))
    plt.title("Frequency Spectrum")
    plt.xlim(0,5500)
    #plt.ylim(0,max_y)
    plt.xlabel("Freq [Hz]")
    plt.show()

    print "Done"

    if graphpath is None:
        plt.show()
    else:
        plt.savefig(filename,graphpath)

plotGraph(filename="./static/music/jungle.wav")