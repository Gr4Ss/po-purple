from Hardware import *
from threading import *
from BrickPi import *
import time

class Car:
    def __init__(self):
        self.__motor1 = Motor('A')
        self.__motor2 = Motor('D')
        self.__distance_sensor = DistanceSensor(17,4)
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
    def loop(self):
        while 1:
            self.ride_forward(2)
	    time.sleep(1)
	    self.rotate()
	    time.sleep(1)
            self.ride_backward(2)
	    time.sleep(1)
   def test_distance(self):
	self.__distance_sensor().on()
	while 1:
	    time.sleep(1)
	    print self.__distance_sensor().get_value()
    

