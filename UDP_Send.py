import  socket
import pyaudio
import multiprocessing
port = 9090
chunk = 1920#half of 3840 the min buf size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
clientIP="192.168.1.4"
clientport=9091
runThread = None
streamState=False
def runMain(ip , port):
    print "starting thread"
    global runThread,streamState
    streamState=True
    runThread = multiprocessing.Process(target=run, args=(ip , port ,))
    runThread.start()
def stramStop():
    global streamState
    streamState=False
def run(ip  , port):
    print "openning pyaudio"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)
    print "pyaudio OK"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create the socket UDP
    server_socket.bind(('', port))  # listen on port 9090

    while True:
	
        server_socket.sendto(stream.read(chunk) ,(str( ip), 9091))
        if (streamState==False):
            print("Stream Ended")
            break

    stream.stop_stream()
    stream.close()
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    p.terminate()
if __name__=="__main__":
    runMain("192.168.1.2" , 6661)
    raw_input("Enter anything to quit")
    stramStop()
