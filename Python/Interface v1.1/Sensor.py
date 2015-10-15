from BrickPi import *
import time
import RPi.GPIO as GPIO
BrickPiSetup()

class Sensor:
    def __init__(self,nb_values):
        self.__value = []
	self.__nb_values = nb_values
    def update_value(self):
        pass
    def add_value(self,value):
	while (len(self.__value) >= self.__nb_values):
	     self.__value.pop(0)
	self.__value.append(value)
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
    def __init__(self,echo_gpio,trig_gpio):
	Sensor.__init__(self,5)
        self.__echo_gpio = echo_gpio
        self.__trig_gpio = trig_gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(echo_gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(trig_gpio, GPIO.OUT)
        GPIO.output(trig_gpio,False)
    def update_value(self):
        trig_duration = 0.0001
        inttimeout = 2100
        v_snd = 340.29
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
        

class MindstormSensor(Sensor):
    def __init__(self,port,sensor_type):
	Sensor.__init__(self,3)
	self.__port = port
	exec('BrickPi.SensorType[PORT_'+str(self.__port)+'] = TYPE_SENSOR_'+ sensor_type)
	BrickPiSetupSensors()
    def update_value(self):
	exec('value = BrickPi.Sensor[PORT_'+ str(self.__port) +']')
	self.add_value(value)
	
