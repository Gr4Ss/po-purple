
import time
import math

from Engine import *
from BrickPi_thread import *
import get_ratio_pi as ratio

## The minimum speed to move
MINIMUM_SPEED = 155
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
        x_wheel_left = 0
        y_wheel_left = 0
        x_wheel_right = 0
        y_wheel_right = 0
        last_ratio = 1.0
        column_factor = 0.05 # <0.5
        row_factor = 0.05   # <0.5
        group_factor = 15
        correction = 1.0

        des = 0
        try:
            while True:
                ratio = get_ratio('/dev/shm/mjpeg/cam.jpg',x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
                          last_ratio,
                          column_factor, row_factor,
                          correction)
                last_ratio = ratio
                if ratio<1:
                    self.__leftengine.set_speed(150.)
                    self.__rightengine.set_speed(150.*ratio)
                else:
                    self.__leftengine.set_speed(150.*1./ratio)
                    self.__rightengine.set_speed(150.)
        except:
            self.__brickpi.off()
