# time module for timing
import time
# import libary for controlling the brickpi ports
from BrickPi import *
import math
PORTS = {'A':PORT_A,'B':PORT_B,'C':PORT_C,'D':PORT_D}
BrickPiSetup()
class Light:
    def __init__(self,port):
        self.port = PORTS.get(port,PORT_C)
        BrickPi.MotorEnable[self.port] = 1
        BrickPiUpdateValues()
        self.count = 0
        self.on = False
    def set_on(self):
        self.on = True
    def set_off(self):
        self.on = False
    def get_light(self):
        if self.count >= 5:
            if self.on:
                BrickPi.MotorSpeed[self.port] = 255
            else:
                BrickPi.MotorSpeed[self.port] = 0
            self.count = 0
        else:
            BrickPi.MotorSpeed[self.port] = 0
            self.count += 1
