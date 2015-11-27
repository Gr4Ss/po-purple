import threading
import time
import math
from utility import *
from Engine import *
from BrickPi_thread import *
from GPIO_thread import *
from Sensor import *
import PID

## The minimum speed to move
MINIMUM_SPEED = 110
## Variable indicating how good batteries are working
## 1. -> full speed
## |
## 0.1 -> Nearly Empty
BATTERY = 1.
## 1 -> ON
## 0 -> OFF
DEBUG = 1

class Controller:
    def __init__(self):
        # Storing the engines of this car
        self.__leftengine = Engine('A')
        self.__rightengine = Engine('B')
        self.__topengine = Engine('C')
        self.__engines = [self.__leftengine,self.__rightengine,self.__topengine]
        # Storing the distance between the centers of the cars
        self.__widthcar = 2.6 + 11.1 - .2
        # Storing the Lego MINDSTORM distance sensor
        self.__distanceLego = MindstormSensor('4','ULTRASONIC_CONT')
        # Storing the GPIO distance sensor
        self.__distancePi = DistanceSensor(17,4)
        # Storing the current gearration
        self.__gearratio = 1./1.
        # Storing the perimeter of the wheels (2*pi*r)
        self.__perimeter = 2*math.pi*2.758
        # Storing a reference to a brickpi thread
        self.__brickpi = BrickPi_Thread(self.__engines,[self.__distanceLego])
        # Storing a reference to a gpio thread
        self.__gpio = GPIO_Thread([self.__distancePi])
        self.__brickpi.on()
        self.__gpio.on()
        self.__command_going = False
        self.__command_thread = None
    def get_car_width(self):
        return self.__widthcar
    def set_speed_engines(self,speed):
        if len(speed) != len(self.__engines):
            raise Exception
        engines = self.__engines
        for i in range(engies):
            engines[i].set_speed(speed[i])
    def flush_engines(self):
        for engine in self.__engines:
            engine.reset_count()
    def get_engine_distance(self):
        result = []
        for engine in self.__engines:
            result.append(engine.get_count()*self.__perimeter*self.__gearratio)
        return result
    ## Turn the thread back off
    def kill_threads(self):
        self.__brickpi.off()
        self.__gpio.off()

    def start_command(self,command,arguments):
        if self.__command_going:
            self.stop_commmand()
        self.__command_going = True
        if arguments != None:
            exec('thread = threading.Thread(target=self.' + command +',args='+ str(arguments) +')')
        else:
            exec('thread = threading.Thread(target=self.' + command +')')
        self.__command_thread = thread
        self.__command_thread.setDaemon('True')
        self.__command_thread.start()

    def stop_commmand(self):
        if self.__command_going:
            self.__command_going = False
            self.__command_thread.join()
            self.__command_thread = None

    ## Return the values of the sensor in a dictionary with keys
    ## Distancesensor1 -> GPIO distance sensor
    ## Distancesensor2 -> Lego MINDSTORM distance sensor
    ## Coming soon : Top angle -> The angle of the top motor
    ## Note: Not yet tested
    def get_sensor_data(self):
        result = dict()
        result['Distancesensor1'] = self.__distancePi.get_value()
        result['Distancesensor2'] = self.__distanceLego.get_value()
        ## result['Top angle'] = (self.__topengine.get_count()%1) *2*math.pi
        return result

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
            self.__rightengine.set_speed(240 + speeddif)
            time.sleep(0.05)

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
            time.sleep(0.05)

    def stop(self):
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)

    def ride_distance(self,distance):
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        pid1 = PID.PID(5.,1/20.,1/50.,.5)
        pid2 = PID.PID(20.,1/2.,1/5.,.5)
        speed = MINIMUM_SPEED
        if DEBUG:
            print speed
        self.__leftengine.set_speed(speed)
        self.__rightengine.set_speed(speed)
        while speed !=0 and self.__command_going:
            distance1 = self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distance2 = self.__rightengine.get_count()*self.__perimeter*self.__gearratio
            if DEBUG:
                print 'Distance:', distance1, distance2
            speed = pid1.new_value(distance-distance1,0.01)
            speed_diff = pid2.new_value(distance1-distance2,0.01)
            if DEBUG:
                print 'Speed + Speed diff: ', speed, speed_diff
            lspeed,rspeed = self.correct_speed(speed,speed_diff)
            if DEBUG:
                print 'Corrected speed:', lspeed,rspeed
            self.__leftengine.set_speed(lspeed)
            self.__rightengine.set_speed(rspeed)
            time.sleep(0.01)
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)


    def correct_speed(self,speed,speed_diff):
        # If the speed or speed + diff is bigger then 255 a correction must happen
        if speed > 255 or speed+speed_diff > 255:
            # if speed_diff bigger is bigger then 0 the left engine must slow down
            if speed_diff > 0:
                return [255-abs(speed_diff),255]
            # if speed_diff < 0 the right engine must slow down
            else:
                return [255,255 - abs(speed_diff)]
        # If the speed or speed+ speed_diff is less than 255
        elif speed < -255 or speed + speed_diff < -255:
            # If speed_diff bigger then 0 right engine must slow down
            if speed_diff > 0:
                return [-255,-255+abs(speed_diff)]
            # If speed diff smaller then 0 the left engine must slow down
            else:
                return [-255+abs(speed_diff),-255]
        # If the absolute value is less then the MINIMUM_SPEED its turned up
        elif abs(speed) < MINIMUM_SPEED:
            signed = sign(speed)
            return [signed*MINIMUM_SPEED,signed*MINIMUM_SPEED+speed_diff]
        return [speed,speed+speed_diff]


    ## A method to rotate
    def rotate(self,degree):
        ## reset the counters of the engiense
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        ## Determine which is the inner most wheel
        if degree > 0:
            inner_engine = self.__rightengine
            outer_engine = self.__leftengine
        else:
            inner_engine = self.__leftengine
            outer_engine = self.__rightengine
        # Calculate the distance to be driven
        distance = self.__widthcar/2. * abs(degree)
        pid1 = PID.PID(10.,1./2.,10/2.,.6)
        pid2 = PID.PID(10.,1./2.,10/2.,.6)
        speed1 = pid1.new_value(distance,0.1)
        speed2 = pid2.new_value(-distance,0.1)
        if DEBUG:
            print 'Speed: ', speed1, speed2
        outer_engine.set_speed(speed1)
        inner_engine.set_speed(speed2)
        while (not (speed1 == 0 and speed2 == 0)) and self.__command_going:
            distance1 = outer_engine.get_count()*self.__perimeter*self.__gearratio
            distance2 = inner_engine.get_count()*self.__perimeter*self.__gearratio
            if DEBUG:
                print 'Distance', distance1, distance2
            speed1 = pid1.new_value(distance - distance1,0.1)
            speed2 = pid2.new_value(-distance - distance2,0.1)
            if DEBUG:
                print 'Speed: ', speed1, speed2
            outer_engine.set_speed(speed1)
            inner_engine.set_speed(speed2)
            time.sleep(0.1)
    def rotate2(self,degree):
        pass
    def ride_polygon(self,sides,distance):
        try:
            sides = float(sides)
        except:
            raise Error()
        ## Hidden I love you sign
        if sides <3:
            raise Error()

        angle = math.pi - (math.pi * (sides-2)/sides) + 0.2
        if DEBUG:
            print 'Angle: ', angle
        while sides > 0:
            self.ride_distance(distance)
	        time.sleep(0.1)
            self.rotate(angle)
	        time.sleep(0.1)
            sides -= 1
            if DEBUG:
                print 'Sides: ', sides


    def correct_speed2(self,inspeed,outspeed):
        # Only usefull when outspeed bigger then inspeed
        if abs(outspeed) > abs(inspeed):
            routspeed = sign(outspeed) * min(255,abs(outspeed))
            routspeed = sign(outspeed) * max(MINIMUM_SPEED*1.1,abs(outspeed))
            rinspeed = sign(outspeed) * abs(max(abs(inspeed),5)/outspeed) * routspeed
	        return rinspeed,routspeed
        return inspeed,outspeed

    def ride_circ(self,radius):
        if abs(radius) <20:
            raise Exception
        pid1 = PID.PID(10.,1/20.,1/50.,1.)
        pid2 = PID.PID(10.,1/20.,1/50.,1.)
        if radius>0:
            inner_engine = self.__rightengine
            outer_engine = self.__leftengine
        else:
            inner_engine = self.__leftengine
            outer_engine = self.__rightengine
        inner_engine.reset_count()
        outer_engine.reset_count()
        angle_per_loop = 1.5/(float(radius))
        angle = angle_per_loop
        speed1 = pid1.new_value(angle*(2*math.pi*abs(radius))-0,0.1)
        speed2 = pid2.new_value(angle*(2*math.pi*(abs(radius)+ 0))-0,0.1)
        inner_engine.set_speed(speed1)
        outer_engine.set_speed(speed2)
        while (not (speed1==0 and speed2==0)) and self.__command_going:
            distance1 = inner_engine.get_count()*self.__perimeter*self.__gearratio
            distance2 = outer_engine.get_count()*self.__perimeter*self.__gearratio
            if DEBUG:
                print 'Distance: ', distance1, distance2
            speed1 = pid1.new_value(angle*abs(radius)-distance1,0.1)
            speed2 = pid2.new_value(angle*(abs(radius)+ self.__widthcar)-distance2,0.1)
            if DEBUG:
                print 'Speed: ',speed1,speed2
            ## Wat volgt is misschien nuttig
            ispeed, ospeed = self.correct_speed2(speed1,speed2)
            if DEBUG:
                print 'Corrected speed: ', ispeed, ospeed
            inner_engine.set_speed(ispeed)
            outer_engine.set_speed(ospeed)
            if angle <= 2*math.pi + 0.3:
                angle += angle_per_loop
            time.sleep(0.1)
        inner_engine.set_speed(0)
        outer_engine.set_speed(0)
    def drive(self,y,x):
        pass
    def rotate_left(self):
        pass
    def rotate_right(self):
        pass
