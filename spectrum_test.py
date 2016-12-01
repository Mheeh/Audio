import wave
import numpy as np
import scipy
from scipy.io.wavfile import read
from scipy.signal import hann
from scipy.fftpack import rfft
import matplotlib.pyplot as plt


def plotFreqSpec(filename,graphpath=None):
    # read audio samples
    framerate,data = read(filename)

    file = wave.open(filename, 'rb')
    nchannels, sampwidth, framerate, nframes = file.getparams()[0:4]

    data = data.astype(np.float, copy=False)

    if nchannels > 1:
        data2 = np.mean(a=data, axis=1)
        data = data2


    windowsize = 512
    lackingFrames = nframes%windowsize

    if lackingFrames>0:
        data = np.append(data, np.tile(0, lackingFrames))

    window = hann(windowsize)
    data = data/(2**(sampwidth*8)) #data/sampwidth
    audio = data


    loopcount = nframes//windowsize


    for i in range(0,loopcount):
        # apply a Hanning window
        #audio[(i*windowsize):((i+1)*windowsize)] =
        fftdat = np.array(audio[(i*windowsize):((i+1)*windowsize)]*window)
        if i == 0:
            magstotal = rfft(fftdat)
        else:
            magstotal += rfft(fftdat)

        #magstotal  = abs(rfft(fftdat))
        # fft

    if(loopcount>0):
        magstotal = magstotal/loopcount

    mags = magstotal
    mags = abs(mags)
    # convert to dB
    mags = 20*scipy.log10(mags)
    # normalise to 0 dB max
    mags -= max(mags)


    x_freq = framerate/2./windowsize
    x_freq = x_freq*len(mags)
    x_freq = np.arange(0,x_freq, step =framerate/2./windowsize)

    xSize = 7
    ySize = 3

    plt.figure(figsize=(xSize, ySize))

    # plot
    #plt.plot(mags)
    plt.plot(x_freq,mags)
    # label the axes
    plt.ylabel("Magnitude (dB)")
    #plt.ylim((-90,0))
    plt.xlabel("Frequency Bin")
    # set the title
    plt.title("Spectrum")
    if graphpath is not None:
        plt.savefig(graphpath)
    else:
        plt.show()

if __name__ == "__main__":
    plotFreqSpec("./static/music/temp.wav")