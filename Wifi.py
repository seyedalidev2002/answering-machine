import socket
import subprocess as sub
from time import sleep
def runCommand(command):
	file =open("/home/ali/code/MP/files/wifiStd.txt" ,'w')
	sub.call(command , shell =True , stdout=file)
	file.close()
	file2=open("/home/ali/code/MP/files/wifiStd.txt" , 'r')
	out= file2.read()
	file2.close()
	print "============================================="
	print out
	print "============================================="
	return out
def getSsidPass():
	s=socket.socket()
	s.bind(("" , 9993))
	s.listen(1)
	c , addr= s.accept()
	data=c.recv(1024)
	c.close()
	s.close()
	sub.call("nmcli c delete id Hotspot" , shell=True)
	f=open("/home/ali/code/MP/files/ssid_pass.txt" , 'w')
	f.write(data)
	f.close()
	file=open("/home/ali/code/MP/files/ssid_pass.txt" , 'r')
        ssid_pass=file.read().split('~')
        file.close()
	sleep(1)
        out2=runCommand("nmcli device wifi list")
   	connectTo(ssid_pass[0], ssid_pass[1])
def connectTo(ssid , password):
	#sub.call("nmcli device wifi con "+ssid+" password "+password , shell=true)
	#runCommand("nmcli device wifi con \""+ssid+"\" password \""+password+"\"")
	
	out=runCommand("nmcli device wifi con \""+ssid+"\" password \""+password+"\"")
	if "Error" in out :
		print "ERRRRRRRRRRRRRRRRRRRRRRR"
	else:
		print "CONNECTED!!"

def startHotSpot():
	out=runCommand("nmcli con show")
	if "Hotspot" in out : #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                print "Hotspot is already Created"
                getSsidPass()
		return
	runCommand ("nmcli dev wifi hotspot ssid TEST password tehran19")
	
	out=runCommand("nmcli con show")
        if "Hotspot" in out : #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                print "Hotspot is Created"
		getSsidPass()
        else:
		
                print "sth went wrong \nTrying agin..."
		sleep(1)
		startHotSpot()
def run():
	
	file=open("/home/ali/code/MP/files/ssid_pass.txt" , 'r')
        ssid_pass=file.read().split('~')
        file.close()
	print "ssid : "+ssid_pass[0]
	print "pass : "+ssid_pass[1]
	out= runCommand("nmcli con show --active")
	if ssid_pass[0] in out:
		print "we are connected"
	else:
		out2=runCommand("nmcli device wifi list")
		if ssid_pass[0] in out2 :
			connectTo(ssid_pass[0] , ssid_pass[1])
		else :
			startHotSpot()
run()
