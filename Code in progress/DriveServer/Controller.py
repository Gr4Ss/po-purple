import threading
import time
import math
from Engine import *
import Light
from Sensor import *
from IO_thread import *
import ControllerCommands


## 1 -> ON
## 0 -> OFF
DEBUG = True

class Controller:
    def __init__(self):
        # Storing the engines of this car
        self.__leftengine = Engine('A')
        self.__rightengine = Engine('B')
        self.__leftled = Light.Light('D')
        self.__rightled = Light.Light('C')
        self.__distance_sensor = DistanceSensor(17,4)
        # Storing the distance between the centers of the cars
        # TODO measure width and gearratio
        self.__widthcar = 20.
        self.__gearratio = 1./3.
        # Storing the perimeter of the wheels (2*pi*r)
        self.__perimeter = 2*math.pi* 2.579
        print 'initing Controller'
        ControllerCommands.init(self.__leftengine,self.__rightengine,self.__distance_sensor,self.__perimeter,self.__gearratio,self.__widthcar,self.__leftled,self.__rightled)
        print 'Controller inited'
        # Storing a reference to a brickpi thread
        self.__io = IO_Thread([self.__leftengine,self.__rightengine],[self.__distance_sensor],[self.__leftled,self.__rightled])
        self.__command_going = False
        self.__command_thread = None
        self.__parcours = None
    # Start a commands
    # If there is already a command going, stop that first
    # Start thread
    # @post self.__command_going = True
    # @post self.__command_thread = new thread
    def start_command(self,command,arguments = None):
        if ControllerCommands.Going:
            self.stop_command()
        self.__io.on()
        ControllerCommands.Going = True
        if arguments != None:
            thread = threading.Thread(target= command,args=arguments)
        else:
            thread = threading.Thread(target= command)
        self.__command_thread = thread
        self.__command_thread.setDaemon('True')
        self.__command_thread.start()
    # A method to stop the going command
    # if there is a command going stop it
    # @post self.__command_going = False
    # @post self.__command_thread = None
    def stop_command(self):
        if ControllerCommands.Going:
            ControllerCommands.Going = False
            self.__command_thread.join()
            self.__io.off()
            self.__command_thread = None
    # Turn the thread back off
    def kill_threads(self):
        self.__io.off()
