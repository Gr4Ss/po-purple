import Engine
import PID
import time

from utility import *
DEBUG = True
DEBUG2 = False
class Control:
    global DEBUG,DEBUG2
    def __init__(self,el,er):
        self.__previous_cms_left  = 0
        self.__previous_cms_right = 0
        self.__engine_left = el
        self.__engine_right = er
        self.__minimum_speed_left = 60
        self.__minimum_speed_right = 60
        self.__port_cms_left = 0.1
        self.__port_cms_right = 0.1
        self.__previous_discrete_left = 0
        self.__previous_discrete_right = 0
        self.__previous_time = time.time()
        self.__engine_left.reset_count()
        self.__engine_right.get_count()
        self.__pidleft = PID.PID(1.,0.5,0.6,.1)
        self.__pidright = PID.PID(1.,0.5,0.6,.1)
    def reset(self):
        self.__engine_left.reset_count()
        self.__engine_right.get_count()
        self.__previous_time = time.time()
    def drive(self,left,right,dt):
        current_time = time.time()
        time_to_previous,self.__previous_time = current_time  - self.__previous_time,current_time
        real_speed_left = (self.__engine_left.get_count()*self.__engine_left.get_perimeter())/ time_to_previous
        real_speed_right = (self.__engine_right.get_count()*self.__engine_right.get_perimeter())/time_to_previous
        error_left = self.__previous_cms_left - real_speed_left
        error_right = self.__previous_cms_right - real_speed_right
        if DEBUG:
            print 'Error speed (in cm/s): ', error_left,error_right
        self.check_movement(real_speed_left,real_speed_right)
        self.check_speed(real_speed_left,real_speed_right)
        self.__engine_left.reset_count()
        self.__engine_right.reset_count()
        value_left = self.__pidleft.value(error_left,time_to_previous)
        value_right = self.__pidright.value(error_right,time_to_previous)
        speedL, speedR = self.rescale_speed_ms(left/dt+value_left,right/dt+value_right)
        self.__previous_cms_left,self.__previous_cms_right = speedL, speedR
        if DEBUG:
            print 'Output PID: ', value_left,value_right
            print 'Desired speed in m/s: ', left/dt+value_left,right/dt+value_right
            print 'Corrected to: ', speedL,speedR
        dspeedL,dspeedR = self.to_discrete(self.__left/dt+value_left,self.__right/dt+value_right)
        if DEBUG:
            print 'Speed on port: ',dspeedL,dspeedR
        self.__engine_left.set_speed(dspeedL)
        self.__engine_right.set_speed(dspeedR)
    def to_discrete(self,speed_ms_left,speed_ms_right):
        discrete_left =  sign(speed_ms_left)*(abs(speed_ms_left)/self.__port_ms_left + self.__minimum_speed_left)
        discrete_right = sign(speed_ms_right)*(abs(speed_ms_right)/self.__port_ms_right + self.__minimum_speed_right)
        return sign(speed_ms_left)*max(abs(discrete_left),self.__minimum_speed_left), sign(speed_ms_right) * max(abs(discrete_right),self.__minimum_speed_right)
    def check_speed(self,speed_left,speed_right):
        if self.__previous_discrete_left > self.__minimum_speed_left+10:
            self.__port_ms_left = self.__port_ms_left*0.95 + 0.05* (speed_left)/(self.__previous_discrete_left-self.__minimum_speed_left)
            if DEBUG2:
                print 'Ratio port/ms left changed to: ', self.__port_ms_left
        if self.__previous_discrete_right > self.__minimum_speed_right + 10:
            self.__port_ms_right = self.__port_ms_right*0.95 + 0.05* (speed_right)/(self.__previous_discrete_right-self.__minimum_speed_right)
            if DEBUG2:
                print 'Ratio port/ms right changed to: ', self.__port_ms_right

    def max_speed_ms(self):
        return min(self.__port_ms_left*(255-self.__minimum_speed_left),self.__port_ms_right*(255-self.__minimum_speed_right))
    def rescale_speed_ms(self,left,right):
        max_speed = self.max_speed_ms()
        if abs(left) >= abs(right) and abs(left)>max_speed:
            return sign(left)*max_speed, sign(right)*abs(right)/abs(left)*max_speed
        if abs(right) >= abs(left) and abs(right)>max_speed:
            return sign(left)*abs(left)/abs(right)*max_speed,sign(right)*max_speed
        else:
            return left,right

    def check_movement(self,left,right):
        if left < 0.001 and self.__previous_discrete_left != 0:
            self.__minimum_speed_left = self.__previous_discrete_left
            if DEBUG:
                print 'LEFT MINIMUM SPEED CHANGED: ',self.__minimum_speed_left
        if right < 0.001 and self.__previous_discrete_right != 0:
            self.__minimum_speed_right = self.__previous_discrete_right
            if DEBUG:
                print 'RIGHT MINIMUM SPEED CHANGED: ',self.__minimum_speed_right
