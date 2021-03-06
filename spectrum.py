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



    windowsize = 1024
    lackingFrames = nframes%windowsize
    data = np.append(data,[0]*lackingFrames)
    window = hann(windowsize)
    data = data/(2**(sampwidth*8))
    audio = data
    for i in range(0,nframes//windowsize):
        # apply a Hanning window
        audio[(i*windowsize):((i+1)*windowsize)] = audio[(i*windowsize):((i+1)*windowsize)]*window
    # fft
    mags = abs(rfft(audio))
    # convert to dB
    mags = 20*scipy.log10(mags)
    # normalise to 0 dB max
    mags -= max(mags)
    # plot
    plt.plot(mags)
    # label the axes
    plt.ylabel("Magnitude (dB)")
    plt.xlabel("Frequency Bin")
    # set the title
    plt.title("Spectrum")
    if graphpath is not None:
        plt.savefig("Spectrum.png")
    else:
        plt.show()

if __name__ == "__main__":
    plotFreqSpec("./static/music/temp.wav")