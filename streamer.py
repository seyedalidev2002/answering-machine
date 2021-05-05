import  socket
import pyaudio
import threading
S_port = 9090
chunk = 1920#half of 3840 the min buf size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
S_clientport=9091
S_streamState=False
p=None
stream=None
server_socket=None
frames = []
thState=False

def S_run(ip  ):
    print("SS")

    global p ,stream,thState , server_socket
    thState=True
    print "openning pyaudio"
    print "pyaudio OK"
    while thState:
        print("SEND")
        server_socket.sendto(stream.read(chunk) ,(str( ip), 9091))

	soundData, addr = server_socket.recvfrom(44100)
        frames.append(soundData)
        stream.write(frames.pop(0))
        print("REC")

      

    stream.stop_stream()
    stream.close()
  #  server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    p.terminate()


def closeStream():
    global thState,server_socket
    thState = False
    
def R_run():
    global server_socket , frames
    print("RR")
    while True:
        soundData, addr = server_socket.recvfrom(44100)
        frames.append(soundData)
        stream.write(frames.pop(0))
        print("REC")
        if (thState == False):

            print("Thread Ended")
            break

def main():
    global p, stream, server_socket
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create the socket UDP
    server_socket.bind(('', 9090))  # listen on port 9090
    sub1=threading.Thread(target=S_run ,args=("192.168.1.11" , ) )
    sub2=threading.Thread(target=R_run)
    print("sub starting !")
    sub1.start()
    sub1.join()

if __name__=="__main__":
    main()
    raw_input("end>>")
