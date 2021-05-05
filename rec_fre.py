import pyaudio
import wave
import numpy as np
import math
import time as Time
from matplotlib.mlab import find


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

#audio = pyaudio.PyAudio()

# start Recording
#stream = audio.open(format=FORMAT, channels=CHANNELS,
#                    rate=RATE, input=True,
  #                  frames_per_buffer=CHUNK)

def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0

def main():
    print "recording..."
    frames = []
    counter=0
    time=0
    while True:
        data = stream.read(CHUNK)
        Frequency = Pitch(data)
        print "%f Frequency" % Frequency
        if Frequency==430:
            time=Time.time()
            counter+=1
        if Time.time()-time>4:
            counter=0
        if counter >25:
            print("end")
            counter=0
            break
        frames.append(data)
    print "finished recording"

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


