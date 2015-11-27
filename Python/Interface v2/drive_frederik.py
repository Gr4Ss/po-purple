import threading
import time
import math
from utility import *
import Controller
import PID
controller = Controller.Controller()
MINIMUM_SPEED = 110
class Driver:
    global MINIMUM_SPEED
    def __init__(self):
        # Storing the engines of this car
        self.__widthcar = controller.get_car_width()
        self.__values = []
        self.__distance = (0,0)
        self.__leftpid = PID.PID2(20,1/20.,1/10.,0.7,0)
        self.__rightpid = PID.PID2(20,1/20.,1/10.,0.7,0)
        self.__driving = True
    def flush(self):
        self.__values = []
        self.__distance = (0,0)
        controller.flush_engines()
    def add_new_values(self,values):
        for value in values:
            self.__values.append(value)
    def drive(self):
        lspeed = MINIMUM_SPEED
        rspeed = MINIMUM_SPEED
        topspeed = random.randint(-255,255)
        controller.set_speed_engines([lspeed,rspeed,topspeed])
        self.__distance[0] += self.__values[0][0]
        self.__distance[1] += self.__values[0][1]
        while self.__driving:
            ldistance,rdistance = controller.get_engine_distance()
            lspeed = self.__leftpid.new_value(self.__distance[0]-ldistance)
            rspeed = self.__rightpid.new_value(self.__distance[1]-rdistance)
            lspeed,rspeed = self.correct_speed(lspeed,rspeed)
            topspeed += random.randint(-25,25)
            controller.set_speed_engines([lspeed,rspeed,topspeed])
            if (abs(ldistance) > abs(self.__distance[0]) -1. and abs(rdistance) > abs(self.__distance[1]) -1.):
                try:
                    self.__values.pop(0)
                    self.__distance[0] += self.__values[0][0]
                    self.__distance[1] += self.__values[0][1]
                except:
                    pass
            time.sleep(0.05)
