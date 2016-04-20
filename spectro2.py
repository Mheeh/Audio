import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import wave

def plotGraph(filename,graphpath=None):
    rate, data = wav.read(filename)

    file = wave.open(filename, 'rb')
    nchannels, sampwidth, framerate, nframes = file.getparams()[0:4]

    data = data.astype(np.float, copy=False)

    if nchannels > 1:
        data2 = np.mean(a=data, axis=1)
        data = data2

    windowsize = 512
    window = signal.get_window('hamming',windowsize)
    f,t, Sxx = signal.spectrogram(data,rate,window=window,nperseg=windowsize,mode='magnitude')
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')


    if graphpath is None:
        plt.show()
    else:
        plt.savefig(filename,graphpath)

plotGraph(filename="./static/music/temp.wav")