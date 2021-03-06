import  socket
import pyaudio
import threading
import multiprocessing
import wave
import numpy as np
import math
import time as Time
from matplotlib.mlab import find
import sys
sub1=None
S_port = 9090
chunk =1024  #half of 3840 the min buf size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE=6000
S_clientport=9091
S_streamState=False
frames = []
thState=False
F=False
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=chunk)
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create the socket UDP
#server_socket.bind(('', 9090))  # listen on port 9090
#server_socket.settimeout(5.0)
def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0
def closeStream():
    print("stop")
    global F,server_socket
    if not sub1.is_alive:
        print("OPPS")
    F = False


def S_run(ip):#start Stream
    print("SS")

    global p, stream, F, server_socket , frames
    F = True
    print "openning pyaudio"
    print "pyaudio OK"
    while F:
        print("SEND")
        server_socket.sendto(stream.read(chunk ,exception_on_overflow=False ), (str(ip), S_clientport))

        try:
            soundData, addr = server_socket.recvfrom(3840)
        except Exception as e :
            print(e)
            frames=[]
            break
        frames.append(soundData)
        stream.write(frames.pop(0))
        print("REC")
    print("Stream Ended")
    return
def SM(IP):
    global p, stream, server_socket , thState , sub1
    thState=True

    sub1=multiprocessing.Process(target=S_run ,args=(IP , ) )
    print("sub starting !")

    sub1.start()

def record():
    print "recording..."
    frames = []
    counter=0
    time=0
    while True:
        data = stream.read(chunk, exception_on_overflow=False)
        Frequency = Pitch(data)
        print "%f Frequency" % Frequency
        if  ((Frequency<431) and (Frequency>400)) :
            time=Time.time()
            counter+=1
	    print "Counter:" +str(counter)
        if Time.time()-time>4:
            counter=0
        if counter >25:
            print("end")
            counter=0
            break
        frames.append(data)
    print "finished recording"

    waveFile = wave.open("message.wav", 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
def control():
	while True:
		command=open("command.txt" , 'r+')
		c=command.read()
		if c=="R":
			print" Recording "
			record()
			command.write("-")
			
		if len(c)>4:
			command.write("-")
			print "STREAM	"
			SM(c)
			
		command.close()
                

#control()		
