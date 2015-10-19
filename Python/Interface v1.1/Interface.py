import Motor
import BrickPiThread
import Sensor
import math
import time
import PID

class Interface:
    def __init__(self):
        self.__leftengine = Motor.Motor('A')
        self.__rightengine = Motor.Motor('B')
        self.__topengine = Motor.Motor('C')
        self.__engines = [Motor.Motor('A'),Motor.Motor('B')]
        self.__gearratio = 24./40.
        self.__perimeter = 2*math.pi*2.5
        self.__brickpi = BrickPiThread.BrickPiThread([self.__motorleft,self.__motorright],[])
        self.__brickpi.on()
        
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
        pid1 = PID.PID(5,1/20.,1/50.,0.01)
        pid2 = PID.PID(1,1/20.,1/50.,0.01)
        speed = pid1.new_value(distance,0.1)
        self.__leftengine.set_speed(speed)
        self.__rightengine.set_speed(speed)
        while speed !=0:
            distance1 = constant*self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distance2 = constant*self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            speed = pid1.new_value(distance-distance1,0.1)
            speed_diff = pid2.new_value(distance1-distance2,0.1)
            self.__leftengine.set_speed(speed)
            self.__rightengine.set_speed(speed + speed_diff)
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)
