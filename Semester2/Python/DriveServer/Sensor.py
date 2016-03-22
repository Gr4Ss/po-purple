# import libary for controlling the brickpi ports
from BrickPi import *
# Setup the brickpi after loading the module
BrickPiSetup()
# time module for timing
import time
# import libary for controlling the GPI0 pin
import RPi.GPIO as GPIO


class Sensor:
    def __init__(self,nb_values):
        # self.__value a FIFO, containing the last nb_values
        self.__values = []
        # self.__nb_values indicating how many values must be hold
        self.__nb_values = nb_values
	
    # A method that calculate a new sensor and add it afterwards to the self.values
    def update_value(self):
        pass
    # A method to add a given value to the self.__value FIFO
    # if len(self.__value) < self.__nb_values then the value is just added to self.__value
    # Else the len(self.__value) - self.__nb_values + 1 first values will be deleted.
    def add_value(self,value):
        while (len(self.__values) >= self.__nb_values):
	     self.__values.pop(0)
	self.__values.append(value)
	
    # Return the median of the not None values in self.__value	
    def get_value(self):
	try:
	    copy = sorted(self.__value)
	    while copy[0] == None:
		copy.pop(0)
	    return copy[len(copy)/2]
	except:
	    return None       

##
## A class to get the value of the distance sensor.
## Code conform Hands-on tutorial raspberry pi
## 
class DistanceSensor(Sensor):
    # self.__echo_gpio and self.__trig_gpio contain the numbers of the pin needed
    # for triggering the sensor and one to determine how long the echo is high
    def __init__(self,echo_gpio,trig_gpio):
	Sensor.__init__(self,5)
        self.__echo_gpio = echo_gpio
        self.__trig_gpio = trig_gpio
        # Some work to configure the GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(echo_gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(trig_gpio, GPIO.OUT)
        GPIO.output(trig_gpio,False)
    # A new value is added to Sensor.__value
    def update_value(self):
        trig_duration = 0.0001
        inttimeout = 2100
        v_snd = 340.29
        # Trigger an output signal
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
	
