
import time
import math
from PID import *
from Engine import *
from BrickPi_thread import *
import get_ratio_pi as ratio

## The minimum speed to move

## Variable indicating how good batteries are working
## 1. -> full speed
## |
## 0.1 -> Nearly Empty
BATTERY = 1.
## 1 -> ON
## 0 -> OFF
DEBUG = True

class Controller:
    def __init__(self):
        # Storing the engines of this car
        self.__leftengine = Engine('A')
        self.__rightengine = Engine('B')
        self.__engines = [self.__leftengine,self.__rightengine]
        # Storing a reference to a brickpi thread
        self.__brickpi = BrickPi_Thread(self.__engines)
    def drive(self):
        self.__brickpi.on()
        minimum_speed = 90.
        maximum_speed = 170.
        x_wheel_left = 0
        y_wheel_left = 287
        x_wheel_right = 480
        y_wheel_right = 287
        last_ratio = 1.0
        column_factor = 0.05 # <0.5
        row_factor = 0.05   # <0.5
        group_factor = 15
        correction = 1.0
        des = 0
        pd1 = PD(100.,50.,0.)
        pid2 = PID(1.,.0,.0,0.)
        try:
            while True:
                ratio = get_ratio('/dev/shm/mjpeg/cam.jpg',x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
                          last_ratio,
                          column_factor, row_factor,
                          correction)
                last_ratio = ratio

                if ratio<1:
                    global_speed = pd1.value(math.log(1./(1-math.sqrt(ratio)),0.1)
                    global_speed = min(max(minimum_speed,global_speed),maximum_speed)
                    new_ratio = 1 - pid2(1-ratio,0.1)
                    print global_speed
                    self.__leftengine.set_speed(global_speed)
                    self.__rightengine.set_speed(global_speed*new_ratio)
                elif ratio == 1:
                    self.__leftengine.set_speed(maximum_speed)
                    self.__rightengine.set_speed(maximum_speed)
                else:
                    ratio = 1./ratio
                    global_speed = pd1.value(math.log(1./(1-math.sqrt(ratio))),0.1)
                    global_speed = min(max(minimum_speed,global_speed),maximum_speed)
                    new_ratio = 1 - pid.pid2(1-ratio,0.1)
                    print global_speed
                    self.__leftengine.set_speed(global_speed*new_ratio)
                    self.__rightengine.set_speed(global_speed)
        except:
            self.__brickpi.off()
