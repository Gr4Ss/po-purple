import Motor
from BrickPi_thread import *
from GPIO_thread import *
from Sensor import *
import math
import time
import PID

class Interface:
    def __init__(self):
        self.__leftengine = Motor.Motor('A')
        self.__rightengine = Motor.Motor('D')
        self.__topengine = Motor.Motor('C')
        self.__widthcar = 15
        self.__distanceLego = MindstormSensor('1','ULTRASONIC_CONT')
        self.__distancePi = DistanceSensor(17,4)
        self.__gearratio = 24./40.
        self.__perimeter = 2*math.pi*2.775
        self.__brickpi = BrickPi_Thread([self.__leftengine,self.__rightengine],[])
        self.__gpio = GPIO_Thread([self.__distancePi])
        self.__brickpi.on()

    def kill_thread(self):
        self.__brickpi.off()

    def set_engines_speed(self,speed):
        if len(self.__engines) != len(speed):
            raise Error()
        else:
            for i in range(len(self.__engines)):
                self.__engines[i].set_speed(speed[i])
    
    def ride_time(self,run_time,speed):
        start_time = time.time()
        self.__leftengine.set_speed(speed)
        self.__rightengine.set_speed(speed)
        while (time.time() - start_time < run_time):
            time.sleep(0.1)
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)
        
    def ride_distance(self,distance):
        constant = -1 if distance<0 else 1
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        pid1 = PID.PID(5.,1/20.,1/50.,1.)
        pid2 = PID.PID(1.,1/20.,1/50.,1.)
        speed = pid1.new_value(distance,0.01)
        self.__leftengine.set_speed(speed)
        self.__rightengine.set_speed(speed)
        while speed !=0:
            distance1 = constant*self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distance2 = constant*self.__rightengine.get_count()*self.__perimeter*self.__gearratio
            speed = pid1.new_value(distance-distance1,0.01)
            speed_diff = pid2.new_value(distance1-distance2,0.01)
            self.__leftengine.set_speed(speed)
            self.__rightengine.set_speed(speed + speed_diff)
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)
    def ride_circ(self,radius):
        if abs(radius) <20:
            raise Exception
        pid1 = PID.PID(10.,1/20.,1/50.,1.)
        pid2 = PID.PID(10.,1/20.,1/50.,1.)
        if radius>0:
            inner_engine = self.__right_engine
            outer_engine = self.__left_engine
        else:
            inner_engine = self.__left_engine
            outer_engine = self.__right_engine
        self.__inner_engine.reset_count()
        self.__outer_engine.reset_count()
        angle_per_loop = 5./float(radius)
        angle = 0.
        while angle < 2*pi:
            distance1 = self.__inner_engine.get_count()*self.__perimeter*self.__gearratio
            distance2 = self.__outer_engine.get_count()*self.__perimeter*self.__gearratio
            speed1 = pid1.new_value(angle*(2*math.pi*abs(radius)-distance1,0.1))
            speed2 = pid2.new_value(angle*(2*math.pi*(abs(radius)+ self.__widthcar))-distance2,0.1)
            inner_engine.set_speed(speed1)
            outer_engine.set_speed(speed2)
            angle += angle_per_loop
	    time.sleep(0.1)
        inner_engine.set_speed(0)
        outer_engine.set_speed(0)
        
