import pyaudio
import socket
from multiprocessing import Process
frames = []
stream = None
udp = None
Ts = None
p=None
thState=False
def udpStream():
    print "started"
    global stream
    global udp
    global stream, Ts, thState , p
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    frames_per_buffer=CHUNK,
                    )
    thState = True

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("0.0.0.0", 8080))

    while True:
	
        print "REC"
	# soundData, addr = udp.recvfrom(CHUNK)
        soundData, addr = udp.recvfrom(44100)
        frames.append(soundData)
        stream.write(frames.pop(0))
        if (thState==False):
            print("Thread Ended")
            break

def closeStream():
    global thState , udp
    thState=False
    udp.shutdown(socket.SHUT_RDWR)
    udp.close()
    stream.close()
    p.terminate()



def runMain():
    print("Receiving audio started")
    global stream, Ts, thState , p
    
    thState = True
    Ts = Process(target=udpStream)
    Ts.start()

if __name__ == "__main__":
    runMain()
    raw_input("Enter Anything to quit")
    closeStream()
