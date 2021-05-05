import sys
import os
if not os.getegid()==0:
	sys.exit('The program needs root access ')

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
D0=port.PA12
D1=port.PA1
D2=port.PA2
D3=port.PA3
ToneEnable = port.PA15
gpio.init()

gpio.setcfg(D0 , gpio.OUTPUT)
gpio.setcfg(D1 , gpio.OUTPUT)
gpio.setcfg(D2 , gpio.OUTPUT)
gpio.setcfg(D3 , gpio.OUTPUT)
gpio.setcfg(ToneEnable , gpio.OUTPUT)
gpio.output(ToneEnable , 0)

def gpioset(d3 , d2 , d1, d0):
	print (str(d3)+str(d2)+str(d1)+str(d0))
	gpio.output(D0 , d0)
	gpio.output(D1 , d1)
	gpio.output(D2 , d2)
	gpio.output(D3 , d3)
def numTogpio(num):
	if num==0:
		gpioset(1 ,0 ,1 ,0)
	elif num==1:
		gpioset(0,0,0,1)
	elif num==2:
		gpioset(0,0,1,0)
	elif num==3:
		gpioset(0,0,1,1)
	elif num==4:
		gpioset(0,1,0,0)
	elif num==5:
		gpioset(0,1,0,1)
	elif num==6:
		gpioset(0,1,1,0)
	elif num==7:
		gpioset(0,1,1,1)
	elif num==8:
		gpioset(1,0,0,0)
	elif num==9:
		gpioset(1,0,0,1)

	
def main(number):
	i=0
	for i in range(0 , len(number)) :
		print("calling...")
		numTogpio(int(number[i]))
		gpio.output(ToneEnable , 1)
		sleep(0.1)
		gpio.output(ToneEnable , 0)


if __name__=="__main__":
	main(raw_input("enter the number  =>"))
