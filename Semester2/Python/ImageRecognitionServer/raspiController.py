import time
import math
import raspiSocket
from Engine import *
from BrickPi_thread import *

raspiSckt = raspiSocket.raspiSocket(6000)

class Controller:
    def __init__(self):
        # Storing the engines of this car
        self.__leftengine = Engine('A')
        self.__rightengine = Engine('B')
        self.__engines = [self.__leftengine,self.__rightengine]
        # Storing a reference to a brickpi thread
        self.__brickpi = BrickPi_Thread(self.__engines)
    def drive(self):
        while True:
            if raspiSckt.new_values():
                leftspeed,rightspeed = raspiSckt.get_values()
                self.__leftengine.set_speed(leftspeed)
                self.__rightengine.set_speed(rightspeed)
            time.sleep(0.005)
