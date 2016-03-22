import Engine
import PID
import time

from utility import *
class Control:
    def __init__(self):
        self.__engine_left = el
        self.__engine_right = er
        self.__minimum_speed = 100
        self.__previous_discrete_left = 0
        self.__previous_discrete_right = 0
        self.__engine_left.reset_count()
        self.__engine_right.get_count()
        self.__pidleft = PID.PID(50.,0.5,5.,.1)
        self.__pidright = PID.PID(50.,0.5,5.,.1)
    def drive(self,left,right):
        value_left = self.__pidleft.value(left,1.)
        value_right = self.__pidright.value(right,1.)
        speedL, speedR = self.rescale_speed(value_left,value_right)
        if DEBUG:
            print 'Output PID: ', value_left,value_right
            print 'Corrected to: ', speedL,speedR
        self.__engine_left.set_speed(speedL)
        self.__engine_right.set_speed(speedR)
    def rescale_speed(self,left,right):
        if left>=right:
            if left > self.__minimum_speed*1.1:
                nleft = sign(left) * min(230,abs(left))
                nright = sign(right) * max(self.__minimum_speed,abs(nleft*right/left))
                return nleft,nright
            else:
                return (0,0)
        else:
            if right> self.__minimum_speed*1.1:
                nright = sign(right) * min(230,abs(left))
                nleft = sign(left)* max(self.__minimum_speed,abs(nright*left/right))
                return nleft,nright
            else:
                return (0,0)
