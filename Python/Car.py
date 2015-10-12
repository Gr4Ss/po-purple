from Hardware import *
import threading
import math
from BrickPi import *
import time
from PID import *
sensor_type = {'touch':'TOUCH','uv_sensor':'ULTRASONIC_CONT'}
class Car:
    def __init__(self,radius,gear_ratio):
        self.__motor1 = Motor('A')
        self.__motor2 = Motor('D')
	self.__perimeter = 2*math.pi*radius
	self.__gear_ratio = gear_ratio
        self.__distance_sensor = DistanceSensor(17,4)
	self.__touch_sensor = MindstormSensor(1,'TOUCH')
	self.__distance_sensor2 = MindstormSensor(3,'ULTRASONIC_CONT')
    def ride_forward(self,run_time):
        start = time.time()
	self.__motor1.on(255)
	self.__motor2.on(255)
        while (time.time() - start <= run_time):
            time.sleep(0.1)
	self.__motor1.off()
	self.__motor2.off()
    def ride_backward(self,run_time):
        start = time.time()
        self.__motor1.on(-255)
        self.__motor2.on(-255)
        while (time.time() - start <= run_time):
            time.sleep(0.1)
	self.__motor1.off()
	self.__motor2.off()
    def stop(self):
        t1 = self.__motor1.off()
        t2 = self.__motor2.off()
    def rotate(self,run_time):
	start = time.time()
	self.__motor1.on(150)
	self.__motor2.on(-150)
	while(time.time() - start <=run_time):
		time.sleep(0.1)
	self.__motor1.off()
	self.__motor2.off()
    def ride_distance(self,distance):
	self.__motor1.reset_count()
	self.__motor2.reset_count()
	pid1 = PID(1,1./10000.,1./50000.,0.01)
	pid2 = PID(2,1/5000.,1./2500,0.01)
	speed = pid1.new_value(distance,0.01)
	self.__motor1.on(speed)
	self.__motor2.on(speed)
	while (speed != 0):
	    distance1 = self.__motor1.get_count()*self.__perimeter*self__gear_ratio
	    distance2 = self.__motor2.get_count()*self.__perimeter*self__gear_ratio
	    speed = pid1.new_value(distance - distance1,0.01)
	    speed_diff = pid2.new_value(distance1-distance2,0.01)
	    self.__motor1.update_speed(speed)
	    self.__motor2.update_speed(speed + speed_diff)
	self.__motor1.off()
	self.__motor2.off()
    def loop(self):
        while 1:
            self.ride_forward(2)
	    time.sleep(1)
	    self.rotate(1)
	    time.sleep(1)
            self.ride_backward(2)
	    time.sleep(1)
    def test_distance(self):
	self.__distance_sensor.on()
	while 1:
	    time.sleep(1)
	    print self.__distance_sensor.get_value()
    def test_touch(self):
	self.__touch_sensor.on()
	while 1:
	    time.sleep(0.5)
	    print self.__touch_sensor.get_value()

    

