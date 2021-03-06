#!/usr/bin/env python
#coding: utf-8
""" This work is licensed under a Creative Commons Attribution 3.0 Unported License.
    Frank Zalkow, 2012-2013 """
"""Modified by: Ariel Antonowicz, Marcin Lipa, Dariusz Urbanski, 2016 """

import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
import wave
import numpy as np

""" short time fourier transform of audio signal """
def stft(sig, frameSize, overlapFac=0.99, window=np.hanning):
    #frameSize = 128
    win = window(frameSize)
    print frameSize
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(np.floor(frameSize/2.0)), sig)
    # cols for windowing
    cols = np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))

    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)

""" scale frequency axis logarithmically """
def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))

    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,scale[i]:], axis=1)
        else:
            newspec[:,i] = np.sum(spec[:,scale[i]:scale[i+1]], axis=1)

    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i+1]])]

    return newspec, freqs

""" plot spectrogram"""
def plotstft(audiopath, binsize=2**10, plotpath=None, colormap="jet"):
    samplerate, samples = wav.read(audiopath)

    file = wave.open(audiopath, 'rb')
    nchannels, sampwidth, framerate, nframes = file.getparams()[0:4]

    samples = samples.astype(np.float, copy=False)

    if nchannels > 1:
        samples2 = np.mean(a=samples, axis=1)
        samples = samples2

    #konwersja do mono.
    ##nie uzywana
    #samples2 = np.array(np.mean(samples,axis=1,dtype=samples.dtype),dtype=samples.dtype)
    #samples2 = np.array(np.sum(samples,axis=1),dtype=samples.dtype)

    # Rozdzielanie kanalow, tez nie uzywane
    #samples = np.array(samples.T[1],dtype=samples.dtype)


    s = stft(samples, binsize)

    print "Channels: ",nchannels
    print "sampleWidth: ",sampwidth
    print "framerate: ",framerate
    print "nframes: ",nframes

   # print samplerate
    print "Sample " + str(len(samples))
    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    xPx = 1175
    yPx = 676
    xSize = 15
    ySize = 7.5
    dpi = np.floor((xPx*yPx)/(xSize*ySize))

    plt.figure(figsize=(xSize, ySize))



    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])


    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    if plotpath is not None:
        plt.savefig(plotpath)
    else:
        plt.show()

    plt.clf()

if __name__ == "__main__":
   plotstft("./static/music/drum.wav")
