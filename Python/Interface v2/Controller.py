import threading
import time
from utility import *
from Engine import *
from BrickPi_thread import *
from PID import *

class Controller:
    def __init__(self):
        self.__command_going = False
        self.__command_thread = None
        self.__leftengine = Engine('A')
        self.__rightengine = Engine('B')
        self.__brickpi = BrickPi_Thread([self.__leftengine,self.__rightengine],[])
        self.__gearratio = 1./1.
        self.__perimeter = 2*math.pi*2.758
        self.__brickpi.on()
    def start_command(self,command,arguments):
        if self.__command_going:
            self.stop_commmand()
        self.__command_going = True
        exec('thread = threading.Thread(target=self.' + command +',args='+ argument +')')
        self.__command_thread = thread
        self.__command_thread.setDaemon('True')
        self.__command_thread.start()
    def stop_commmand(self):
        if self.__command_going:
            self.__command_going = False
            self.__command_thread.join()
            self.__command_thread = None
    def forward(self):
        pid = PID(5.,1/20.,1/50.,1.)
        self.__leftengine.set_speed(240)
        self.__rightengine.set_speed(240)
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        while self.__command_going:
            distance1 = self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distance2 = self.__rightengine.get_count()*self.__perimeter*self.__gearratio
            speeddif = pid.new_value(distance1-distance2,0.1)
            self.__rightengine.set_speed(-240 - speeddif)
            time.sleep(0.1)
    def backward(self):
        pid = PID(5.,1/20.,1/50.,1.)
        self.__leftengine.set_speed(-240)
        self.__rightengine.set_speed(-240)
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        while self.__command_going:
            distance1 = self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distance2 = self.__rightengine.get_count()*self.__perimeter*self.__gearratio
            speeddif = pid.new_value(distance1-distance2,0.1)
            self.__rightengine.set_speed(-240 - speeddif)
            time.sleep(0.1)
    def stop(self):
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)
    def drive(self,y,x):
        pass
    def rotate_left(self):
        pass
    def rotate_right(self):
        pass
