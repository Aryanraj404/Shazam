import pyaudio
import wave

def RecordAudio(outputFile,recordSeconds=5):

    FORMAT = pyaudio.paInt16
    CHANNELS = 1 #means mono 
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Recording...")

    frames = []
    print("Recording Started...")
    for i in range(0,int(RATE / CHUNK * recordSeconds)):

        data = stream.read(CHUNK,exception_on_overflow=False)

        frames.append(data)

    print("Recording Complete")
    print(len(frames))
    stream.stop_stream()
    stream.close()

    audio.terminate()

    waveFile = wave.open(outputFile,'wb')

    waveFile.setnchannels(CHANNELS)

    waveFile.setsampwidth(audio.get_sample_size(FORMAT))

    waveFile.setframerate(RATE)

    waveFile.writeframes( b''.join(frames))

    waveFile.close()
