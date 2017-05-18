import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
import sys as _sys
try:
    import threading as _threading
    from threading import Thread
except ImportError:
    del _sys.modules[__name__]
    raise
import PID_follower 
from DirectionControl import *
from ArduinoInput import *
from ThrottleControl import *
from UltrasonicSensors import *
from Mapping import *
from PID_follower import correction

sensor = 0
delta = 0
speedSet = 0
stepCounter = 0
Sum = 0
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    setTurning(0)

setup()
time.sleep(4)
setThrottle(8.2)
time.sleep(0.1)
t=time.time()
LastMPG=time.time()
lp=0
lthrot=0
while time.time()<t+100: 
	time.sleep(0.0001)
	if (EncoderMPG()==1) | (time.time()-LastMPG>0.2):
        	CurrMPG=time.time()
		stepCounter += 1
		Sum=Sum+CurrMPG-LastMPG
		if stepCounter==1:
      			if Sum/10<0.015:
			#if CurrMPG-LastMPG<0.0096:
           			speedSet-=0.02
				if speedSet<-0.1:
					speedSet=-0.1
        		else:
				if Sum/10>0.2:
				#if CurrMPG-LastMPG>0.2:
					speedSet=0.1
				else:
					if  speedSet<0.2:
            					speedSet+=0.01
					else:
						speedSet=0.2
			print "MPG: ",Sum/10, "SpeedSet: ",speedSet
			stepCounter=0
			Sum=0
		LastMPG=CurrMPG
        sensorBuffer=getTriggeredSensor()
	if sensorBuffer!=0:
        	sensor=sensorBuffer
	ComputedCorrection=correction(sensor)
	if lp!=sensorBuffer:
		#print sensorBuffer," Computed correction: ",ComputedCorrection
		lp=sensorBuffer
	setTurning(ComputedCorrection)
	throt=7.9+speedSet
	if throt != lthrot:
		setThrottle(throt)
		print "Throotle ",throt
		lthrot=throt
print "Stop"

GPIO.cleanup()
