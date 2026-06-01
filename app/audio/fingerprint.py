import pyaudio
import wave
import numpy
import cmath
import numpy.fft as fft
import pickle
from scipy.signal import butter, lfilter, freqz, fftconvolve, resample_poly
from app.audio.preprocessing import *
from app.audio.fft import *


def LocatePowerfulFrequencies(transformedData, frequencyBin):
    powerfulfreq = []
    for spectrum in transformedData:
        currentwindow = []
        for start in range(0, len(spectrum), frequencyBin):
            band = spectrum[start:start + frequencyBin]
            if len(band) == 0:
                continue
            peakValue = numpy.max(band)
            strongestpeak = numpy.argmax(band)
            strongestfreq = start + strongestpeak
            currentwindow.append((peakValue, strongestfreq))
        
        # Keep only top 3 peaks per window
        currentwindow.sort(reverse=True)
        top = [freq for _, freq in currentwindow[:3]]
        powerfulfreq.append(top)
    return powerfulfreq

def SeprateAndFlattenAudioData(powefulfreq):
    constellationmap = []

    for(time,window) in enumerate(powefulfreq):
        for frequency in window:
            constellationmap.append((time,frequency))

    return constellationmap

def GenerateConstellationMap(filename):
    #step 1 read audio
    audio, samplerate, duration, _ = (InitialiseAudio(filename,0))

    #step 2 streo->mono
    monoAudio = StereoToMono(audio)

    #step 3 zeropadding
    paddedAudio = Zeropad(monoAudio)

    #step 4 low pass filtering
    filteredAudio = FilterFrequencies(paddedAudio,samplerate)

    #step 5 downsample
    downsampleAudio  = downsample(4,filteredAudio)

    #step 6 hamming window
    WindowSize = 1024
    Hamming = HammingWindow(WindowSize)

    #step 7 generate FFT windows
    windowedData = GenerateArrayaOfWindowedData(WindowSize,Hamming,50,downsampleAudio)

    # STEP 8 — FFT Across Windows
    transformedData = (
        FourierAcrossWindows(
            windowedData
        )
    )

    # STEP 9 — Locate Strong Peaks
    powerfulFrequencies = (
        LocatePowerfulFrequencies(
            transformedData,
            120
        )
    )

    # STEP 10 — Flatten To Constellation Map
    constellationMap = (
        SeprateAndFlattenAudioData(
            powerfulFrequencies
        )
    )
    return constellationMap

# Reduce fan out and time window
def GenerateHashes(constellationMap, fanOut=3, timeDelta=50):
    hashes = []
    for i, (anchorTime, anchorFreq) in enumerate(constellationMap):
        count = 0
        for j in range(1, len(constellationMap) - i):
            if count >= fanOut:
                break
            targetTime, targetFreq = constellationMap[i + j]
            if targetTime - anchorTime > timeDelta:
                break
            if targetTime == anchorTime:
                continue
            deltaTime = targetTime - anchorTime
            hashes.append((f"{anchorFreq}|{targetFreq}|{deltaTime}", anchorTime))
            count += 1
    return hashes