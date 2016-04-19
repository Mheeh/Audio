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
    data = data.T
    time=[]
    for i in range(0,nframes):
        time.append(float(i)*(1./framerate))

    last = time[nframes-1]
    print "Channels: ",nchannels
    print "sampleWidth: ",sampwidth
    print "framerate: ",framerate
    print "nframes: ",nframes


    frames=[]
    for i in range(0,nchannels):
        frames.append(file.readframes(nframes=1))

    xSize = 15
    ySize = 6

    data = data.astype(np.float, copy=False)
    data = data / 2 ** (8 * sampwidth)
    data = data - (data.max() + data.min()) / 2

    plt.figure(figsize=(xSize, ySize*nchannels+10*(nchannels-1)))
    for i in range(0,nchannels):
        plt.subplot(211+i)
        plt.title('Channel '+str(i+1))
        plt.xlim(0,last)
        if nchannels > 1:
            plt.plot(time,data[i])
        else:
            plt.plot(time,data)
        plt.xlabel('Time [s]')

    print "Done"

    if graphpath is not None:
        plt.savefig(filename, graphpath)
    else:
        plt.show()

if __name__ == "__main__":
    plotGraph(filename="./static/music/temp.wav")