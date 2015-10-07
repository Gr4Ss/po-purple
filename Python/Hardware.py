## Class concerning the motors of the robot.
from BrickPi import *
import threading
import time
import RPi.GPIO as GPIO
BrickPiSetup()
##
## Class concerning the LEGO-MINDSTORM Motor
## It possible to let the motor run (back and forth) at a given power rate.
## It's possible to rotate over a given angle.
## 
class Motor:
    def __init__(self,port):
        ## A motor is connected to a given port ('A','B','C','D')
        self.__port = port
        ## BrickPi command to enable the motor
        exec("BrickPi.MotorEnable[PORT_" + self.__port + "] = 1")
        ## Variable storring the actual moving status of this motor
        ## speed = 0 is not running
        ## speed < 0 is running backward
        ## speed > 0 is running forward
        self.__speed = 0
        self.__thread = None
    ## Returning the running speed of this Motor
    ## speed = 0 is not running
    ## speed < 0 is running backward
    ## speed > 0 is running forward
    def get_speed(self):
        return self.__speed
    
    ## Let's run a motor
    def run_motor(self):
	while (self.__speed !=0):
             exec("BrickPi.MotorSpeed[PORT_" + self.__port + "] =" + self.__speed)
             BrickPiUpdateValues()
    def on(self,value):
	self.__speed = value
	self.__thread = threading.Tread(target=run_motor)
	self.__thread.setDaemon('True')
	self.__thread.start()

 
    ## Stop running the motor.
    def off(self):
        self.__speed = 0
	self.__thread = None
    def update_speed(self,speed):
	self.__speed = speed
    ## TO DO: Example on
        ## https://github.com/DexterInd/BrickPi_Python/blob/master/Sensor_Examples/BrickPi.py
    def rotate_angle(self):
        pass

    
## 
## A superclass concerning sensors (both the GPIO and the LEGO-MINDSTORM)
##
class Sensor:
    def __init__(self):
        self.value = None
    def update_value(self):
        pass
##
## A class to get the value of the distance sensor.
## Code conform Hands-on tutorial raspberry pi
## 
class DistanceSensor:
    def __init__(self,echo_gpio,trig_gpio):
        self.__echo_gpio = echo_gpio
        self.__trig_gpio = trig_gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(echo_gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(trig_gpio, GPIO.OUT)
        GPIO.output(trig_gpio,False)
        self.__value = []
	self.__run = False
	self.__thread = None
        
    def add_value(self,value):
	while (len(self.__value) >=5):
	     self.__value = self.__value.pop(0)
	self.__value.append(value)

    def get_value(self):
	try:
  	    copy = sorted(self.__value)
	    return copy[2]
	except:
	    return None
    def on(self):
	self.__run = True
	self.__thread = treading.Thread(target=update_value)
	self.__thread.setDaemon(True)
	self.__thread.start()
    def off(self):
	self.__run = False
	self.__thread = None
    def update_value(self):
        trig_duration = 0.0001
        inttimeout = 2100
        v_snd = 340.29
	while self.__run:
	    GPIO.output(self.__trig_gpio,True)
       	    time.sleep(trig_duration)
	    GPIO.output(self.__trig_gpio,False)
       	    count_high = inttimeout
	    while ( GPIO.input(self.__echo_gpio) == 0 and count_high >0):
        	count_high -= 1
	    if count_high > 0:
                echo_start = time.time()
                count_low = inttimeout
                while ( GPIO.input(self.__echo_gpio) == 1 and count_low >0):
                    count_low -= 1
                echo_end = time.time()
                echo_duration = echo_end - echo_start
            if count_high>0 and count_low >0:
                distance = echo_duration * v_snd *100./2.
                self.add_value(distance)
	    else:
                self.add_value(None)
	    time.sleep(0.1)
            
class MindStormSensor:
    def __init__():
        pass
    def update_value():
        pass
