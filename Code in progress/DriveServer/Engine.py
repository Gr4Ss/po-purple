from BrickPi import *
from utility import *

BrickPiSetup()
PORTS = {'A':PORT_A,'B':PORT_B,'C':PORT_C,'D':PORT_D}
# Class concer_ning the LEGO-MINDSTORM Engine
# It possible to let the motor run (back and forth) at a given power rate.
class Engine:
    global PORTS,PORT_A
    def __init__(self,port):
        ## A motor is connected to a given port ('A','B','C','D')
        self.__port = PORTS.get(port,PORT_A)
        ## BrickPi command to enable the motor
        BrickPi.MotorEnable[self.__port] = 1
        ## speed = 0 is not running
        ## speed < 0 is running backward
        ## speed > 0 is running forward
        self.__speed = 0
        ## Set the speed of the motor to 0
        BrickPiUpdateValues()
        ## Ask the current angle of the wheel
        start_angle = BrickPi.Encoder[self.__port]
        self.__start_angle = start_angle
        self.__global_angle = start_angle
    ## Returning the running speed of this Motor
    ## speed = 0 is not running
    ## speed < 0 is running backward
    ## speed > 0 is running forward
    def get_speed(self):
        return self.__speed
    ## Method to set the speed of this motor
    ## If the given is a float it will be round down to an int
    ## If the absolute value of the speed bigger is then 255 the speed will be set to -/+ 255
    def set_speed(self,speed):
        speed = speed *(-1)
        if abs(speed) > 255:
            speed = sign(speed) * 255
        if abs(speed)< 50:
            speed = 0
        BrickPi.MotorSpeed[self.__port] = int(speed)
        self.__speed = int(speed)

    ## The motor is pulsed with the current speed
    ##def pulse(self):
    ##    BrickPi.MotorSpeed[self.__port] = self.__speed
    # A method returning the number of rotations (expressed in number of rotations) of the motor since the last time
    # reset_count() is executed
    def get_count(self):
        angle = BrickPi.Encoder[self.__port]
        return (angle-self.__start_angle)/720.
    ## A method to reset the counter
    ## @post self.__start_angle = the current encoder of the motor.
    def reset_count(self):
        angle = BrickPi.Encoder[self.__port]
        self.__start_angle = angle
    ## Return the total number of rotations of this motor since the motor is inited.
    def get_global_count(self):
        angle = BrickPi.Encoder[self.__port]
        return (angle-self.__global_angle)/720.
