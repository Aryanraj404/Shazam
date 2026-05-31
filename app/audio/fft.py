import pyaudio
import wave
import numpy
import cmath
import numpy.fft as fft
import pickle
from scipy.signal import butter, lfilter, freqz, fftconvolve, resample_poly

def FastFourierTransform(x, N):

    if N == 1:
        return x

    else:

        evenIndexDFT = FastFourierTransform(x[::2],int(N/2))

        oddIndexDFT = FastFourierTransform(x[1::2],int(N/2))
            

        firstHalfFFT = []
        secondHalfFFT = []

        for k in range(0, int(N/2)):

            firstHalfFFT.append(evenIndexDFT[k] + cmath.exp((-2j*cmath.pi*k)/N) * oddIndexDFT[k])

            secondHalfFFT.append(evenIndexDFT[k] - cmath.exp((-2j*cmath.pi*k)/N) * oddIndexDFT[k])

    return firstHalfFFT + secondHalfFFT

def FourierAcrossWindows(windowedData):

    transformedData = []

    for window in windowedData:
        #fftData = FastFourierTransform(window,len(window))
        fftData = numpy.fft.fft(window)
        fftmagnitude = numpy.abs(fftData)

        transformedData.append(fftmagnitude)

    return transformedData
