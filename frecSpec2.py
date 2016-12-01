from scipy.io.wavfile import read
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib import mlab
import wave
import numpy as np

def plotGraph(filename):
    rate, data = read(filename)

    file = wave.open(filename, 'rb')
    nchannels, sampwidth, framerate, nframes = file.getparams()[0:4]

    data = data.astype(np.float, copy=False)
    #normalization
    data = data / (2 ** (8 * sampwidth))

    if nchannels > 1:
        data2 = np.mean(a=data,axis=1)
        data = data2


    plt.subplot(311)
    plt.plot(range(len(data)), data)

    plt.subplot(312)
    plt.specgram(data, NFFT=128, noverlap=0)


    plt.subplot(313)
    #plt.magnitude_spectrum(data, Fs=rate, Fc=22, pad_to=None, sides='onesided',scale='dB')

    f = np.fft.fftfreq(nframes,1./framerate)
    z = np.abs(np.fft.fftshift(np.fft.fft(data)))
    plt.plot(f,z)

    plt.show()

if __name__ =='__main__':
    plotGraph('./static/music/jungle.wav')