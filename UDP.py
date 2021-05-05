import socket as Socket
import threading
socket=None
IPs=[]
dataFlag=False
strData=""
addr=None
def init(port):
    global  socket
    socket = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)  # udp
    socket.bind(("", port))

    print("server is listening")

def sendToAll(m):
    global socket
    for addr in IPs :
        socket.sendto(m , addr)
def sendto ( m, ip , port):
    socket.sendto(m , (ip , port))
def listen():
    global socket , dataFlag  , strData
    while True:
	global addr
        data, addr = socket.recvfrom(1024)
        if (not addr in IPs):
            if str(data) == "join":
                IPs.append(addr)
                socket.sendto("Your device is  allowed !", IPs[len(IPs) - 1])
            else:
                socket.sendto("ERROR your device is not allowed !", addr)

        else:
            if dataFlag == False:
                strData = str(data)
                dataFlag = True


def stop():
    global socket
    socket.shutdown(Socket.SHUT_RDWR)
    socket.close()
def getData():
    global dataFlag , strData ,addr
    if dataFlag==True:
        dataFlag=False
        return strData , addr[0] , addr[1]
    else:
        return "-1" , "-1" , "-1"

def startListening():
    t1= threading.Thread(target=listen)
    t1.start()
