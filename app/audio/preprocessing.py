
import wave
import numpy
import cmath
import numpy.fft as fft
import pickle
from scipy.signal import butter, lfilter, freqz, fftconvolve, resample_poly

def nextPowerOf2(n):
    power = 1
    while power < n:
        power *= 2
    return power

def InitialiseAudio(filename, pointerInAudio):

    # Read wav file
    sound = wave.open(filename, 'rb')

    # Audio metadata
    CHANNELS = sound.getnchannels()
    SAMPLERATE = sound.getframerate()
    FRAMES = sound.getnframes()
    DURATION = FRAMES / SAMPLERATE
    CHUNK = 2048

    # Store chunks
    audioData = []

    for i in range(0,int((SAMPLERATE / CHUNK) * DURATION)):
        audioData.append(sound.readframes(CHUNK))
            
    # Merge bytes together
    concatData = b''.join(audioData[pointerInAudio:])

    # Convert bytes → integers
    audioArray = numpy.frombuffer(concatData,dtype='<i2').reshape(-1, CHANNELS)
        
    
    return (audioArray, SAMPLERATE, DURATION, int((SAMPLERATE / CHUNK) * DURATION))
     
def StereoToMono(steroaudio):
    mono  = steroaudio.sum(axis = 1)/2
    return mono

def Zeropad(audio):
    zeros = numpy.zeros((nextPowerOf2(len(audio)) - len(audio),),dtype=numpy.int8)
    return list(audio) + list(zeros)

#Nyquist-shannon theorm
############################################
def LowPassFilter(cutoff, transitionBand, Fs):

    cutoff = cutoff / Fs

    N = int(numpy.ceil((4 / transitionBand)))

    if not N % 2:
        N += 1

    n = numpy.arange(N)

    lpf = numpy.sinc(
        2 * cutoff * (n - (N - 1) / 2.)
    )

    lpf *= numpy.blackman(N)# Store the average

    lpf = lpf / numpy.sum(lpf)

    return lpf
###############################################

def FilterFrequencies(audio, SAMPLERATE):
    lpf = LowPassFilter(5000,0.0001,SAMPLERATE)
    return fftconvolve(audio, lpf)

def downsample(averagingChunk, data):
    downsampledData = []

   
    for i in range(0, len(data), averagingChunk):      
        chunk = data[i:i + averagingChunk]
        average = sum(chunk) / len(chunk)
        downsampledData.append(average)

    return downsampledData


#Hamming window for smoothing the FFT chunks
def HammingWindow(N):
    n = numpy.arange(0,N,1)

    y = (0.54 - 0.46*numpy.cos(2*cmath.pi * n)/(N-1))
    return y

def GenerateArrayaOfWindowedData(windowSize,windowFunction, windowOverlap,downsample ):
    windowedData = []
    
    step = int(windowSize * (1-windowOverlap/100))

    for index in range(0,len(downsample) - windowSize,step):
        chunk = downsample[index:index+windowSize]
        windowedChunk = (chunk*windowFunction)
        windowedData.append(windowedChunk)
        
    return windowedData

