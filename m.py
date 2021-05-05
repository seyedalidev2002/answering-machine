#!/usr/bin/env python 
from time import sleep
#sleep(10)
import Wifi
import subprocess as Sub
import serial
import multiprocessing 
#import UDP as udp
import tone
import os
import sys
import mainAudio
import threading
if not os.getegid()==0:
        sys.exit("root needed")


#GPIO IMPORT
from pyA20.gpio import gpio
from pyA20.gpio import port

my_relay=port.PA12
ringTrigger = port.PA6
gpio.init()

gpio.setcfg(ringTrigger , gpio.INPUT)
gpio.pullup(ringTrigger , gpio.PULLUP)
gpio.setcfg(my_relay , gpio.OUTPUT)
gpio.output(my_relay , 1)

import time
#Ser init:
Sub.call("mkdir /sys/kernel/config/device-tree/overlays/uart1" , shell=True)
Sub.call("cat /boot/dtb/overlay/sun8i-h3-uart1.dtbo > /sys/kernel/config/device-tree/overlays/uart1/dtbo" , shell=True)
ser = serial.Serial(port = "/dev/ttyS1", baudrate=1200)
ser.close()
ser.open()


#udp.startListening()

def Record():
	mainAudio.record()
def Stream(IP):
	mainAudio.SM(IP)
def rec_mes():
     print("recording massage")
     gpio.output(my_relay , 0)#open relay
    # recorder.main()
     #strat recording 
    # p=multiprocessing.Process(target=Record)
    # p.start()
    # p.join()
     Record()
     gpio.output(my_relay , 1)#close relay
     print("The massage has been taken")
	
def runbot():
	Sub.call("sudo python3 /home/ali/code/MP/Bot.py" , shell=True)
def botSendVoice():
	botSend("sd")
def botSend(mytext ):
	file=open('/home/ali/code/MP/files/balecom.txt' , 'w')
	file.write("mes")
	file.close()
def ringDec():
	ringDelay=0
	ringCounter=0
	flag=0
	global ringTrigger
	while(True):
		if  (not gpio.input(ringTrigger)):
#			udp.sendToAll("RING")
			ringCounter +=1
			flag=1
			print("rang")
			while (not gpio.input(ringTrigger)):
				ringDelay=time.time()
			if(ringCounter==3):
			#	"""" turn trelay on """"
				print("A New Massage  !!!!!!!!!!!")
				rec_mes()
				ringDelay=0
				ringCounter=0
				flag=0
				botSendVoice()
			
		if (time.time() - ringDelay >5 and flag==1):
			ringCounter=0
			flag=0
			print("RING ERROR")
botThread= threading.Thread(target = runbot)
botThread.start()
ringThread = threading.Thread(target=ringDec)
ringThread.start()
# while (True):
	# gpioScan(bot)
botThread.join()
ringThread.join()



