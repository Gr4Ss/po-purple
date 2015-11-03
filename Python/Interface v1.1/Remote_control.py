import threading
from Motor import *
from Sensor import *
from BrickPi_thread import *
from PID import *
from GPIO_thread import *
import time
import math

class Remote_control:
    def __init__(self):
        self.__input_going = False
        self.__input_thread = None
        self.__command_thread = None
        self.__command_going = False
        self.__leftengine = Motor('A')
        self.__rightengine = Motor('D')
	self.__distanceLego = MindstormSensor('1','ULTRASONIC_CONT')
        self.__brickpi = BrickPi_Thread([self.__leftengine,self.__rightengine],[self.__distanceLego])
        self.__gearratio = 1./1.
        self.__perimeter = 2*math.pi*2.758
        self.__commands = ['F','S','L','R','B','V','E']
    def going(self):
	return self.__input_going
    def is_legal_input(inpt):
        return inpt in self.__commands

    def input_handler(self):
        while self.__input_going:
            inp = raw_input('Enter next command: ')
            if not is_legal_input(inp):
                print 'Not a valid commad'
            if inp == 'F':
                if self.__command_going:
                    self.stop_command_thread()
                self.start_command_thread('forward')
            elif inp == 'B':
                if self.__command_going:
                    self.stop_command_thread()
                self.start_command_thread('backward')
            elif inp == 'S':
                if self.__command_going:
                    self.stop_command_thread()
                self.stop()
	    elif inp == 'V':
		if self.__command_going:
		    self.stop_command_thread()
		self.start_command_thread('values')
            elif inp == 'E':
                if self.__command_going:
		    self.stop_command_thread()
                self.off()
    def on(self):
            self.__brickpi.on()
            self.__input_going = True
	    self.__input_thread = threading.Thread(target=self.input_handler)
	    self.__input_thread.setDaemon('True')
	    self.__input_thread.start()

    def off(self):
		self.__brickpi.off()
		self.__input_going = False
		self.__input_thread.join()
		self.__input_thread = None

    def start_command_thread(self,name):
        if self.__thread == None:
            self.__comand_going = True
            exec('thread = threading.Thread(target=self.'+name+')')
            self.__command_thread = thread
            self.__command_thread.setDaemon('True')
            self.__command_thread.start()

    def stop_command_thread(self):
        if self.__command_thread != None:
            self.__command_going = False
            self.__command_thread.join()
            self.__command_thread = None
            
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

    def stop(self):
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)

    def values(self):
	print self.__distanceLego.getValue()

if __name__ == '__main__': 
	remote_control = Remote_control()
	remote_control.on()
	while remote_control.going():
		time.sleep(0.1)

