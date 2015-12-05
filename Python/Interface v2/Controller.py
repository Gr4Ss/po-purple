import threading
import time
import math
from utility import *
from Engine import *
from BrickPi_thread import *
from GPIO_thread import *
from Sensor import *
import drive_Frederik as c1
import PID

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
        self.__topengine = Engine('C')
        self.__engines = [self.__leftengine,self.__rightengine,self.__topengine]
        # Storing the distance between the centers of the cars
        self.__widthcar = 2.6 + 11.1 - .2
        # Storing the Lego MINDSTORM distance sensor
        self.__distanceLego = MindstormSensor('4','ULTRASONIC_CONT')
        # Storing the GPIO distance sensor
        self.__distancePi = DistanceSensor(17,4)
        # Storing the current gearration
        self.__gearratio = 1.
        # Storing the perimeter of the wheels (2*pi*r)
        self.__perimeter = 2*math.pi* 2.579
        # Storing a reference to a brickpi thread
        self.__brickpi = BrickPi_Thread(self.__engines,[self.__distanceLego])
        # Storing a reference to a gpio thread
        self.__gpio = GPIO_Thread([self.__distancePi])
        self.__brickpi.on()
        self.__gpio.on()
        self.__command_going = False
        self.__command_thread = None
    # Start a commands
    # If there is already a command going, stop that first
    # Start thread
    # @post self.__command_going = True
    # @post self.__command_thread = new thread
    def start_command(self,command,arguments = None):
        if self.__command_going:
            self.stop_commmand()
        self.__command_going = True
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
    def stop_commmand(self):
        if self.__command_going:
            self.__command_going = False
            self.__command_thread.join()
            self.__command_thread = None
    # A method to set the speed of the engines
    # If the number of speeds don't equal the number of engines an error is raised
    def set_speed_engines(self,speed):
        if len(speed) != len(self.__engines):
            raise Exception
        engines = self.__engines
        for i in range(engies):
            engines[i].set_speed(speed[i])
    # A method to flush the counter values of the engines
    def flush_engines(self):
        for engine in self.__engines:
            engine.reset_count()
    # return the distance traveled by the engines
    def get_engine_distance(self):
        result = []
        for engine in self.__engines:
            result.append(engine.get_count()*self.__perimeter*self.__gearratio)
        return result
    # Turn the thread back off
    def kill_threads(self):
        self.__brickpi.off()
        self.__gpio.off()

    ## Return the values of the sensor in a dictionary with keys
    ## Distancesensor1 -> GPIO distance sensor
    ## Distancesensor2 -> Lego MINDSTORM distance sensor
    def get_sensor_data(self):
        result = dict()
        result['Distancesensor1'] = self.__distancePi.get_value()
        result['Distancesensor2'] = self.__distanceLego.get_value()
        result['SpeedLeft'] = self.__leftengine.get_speed()
        result['SpeedRight'] = self.__rightengine.get_speed()
        ## result['Top angle'] = (self.__topengine.get_count()%1) *2*math.pi
        return result
    # A method to drive forward
    def forward(self):
        pid = PID.PID(15.,1/2.,2.,.1)
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
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)
    # A mehtod to drive backward
    def backward(self):
        pid = PID.PID(15.,1/2.,2.,.1)
        self.__leftengine.set_speed(-240)
        self.__rightengine.set_speed(-240)
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        while self.__command_going:
            distance1 = self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distance2 = self.__rightengine.get_count()*self.__perimeter*self.__gearratio
            speeddif = pid.new_value(distance1-distance2,0.1)
            self.__rightengine.set_speed(-240 + speeddif)
            time.sleep(0.05)
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)
    # A method to turn left
    def left(self):
        self.__rightengine.set_speed(240)
        while self.__command_going:
            pass
        self.__rightengine.set_speed(0)
    # A method to turn right
    def right(self):
        self.__leftengine.set_speed(240)
        while self.__command_going:
            pass
        self.__leftengine.set_speed(0)

    # A method to stop driving
    def stop(self):
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)

    def follow_line1(self):
        follow = c1.Frederik()
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        pidleft = PID.PID2(50.,5.,10.,0.5,0)
        pidright = PID.PID2(50.,5.,10.,0.5,0)
        goaldistanceleft,goaldistanceright = follow.get_data()[0],follow.get_data()[1]
        while self.__going:
            distanceleft = self.__leftengine.get_count()*self.__perimeter*self.__gearratio
            distanceright = self.__rightengine.get_count()*self.__perimeter*self.__gearratio
            speedleft = pidleft.new_value(goaldistanceleft-distanceleft,0.1)
            speedright = pidright.new_value(goaldistanceright-distanceright,0.1)
            speedleft,speedright = correct_speed3(speedleft,speedright)
            self.__leftengine.set_speed(speedleft)
            self.__rightengine.set_speed(speedright)
            if (abs(goaldistanceleft - distanceleft)< 1.) and (abs(goaldistanceright - distanceright) < 1.):
                goaldistanceleft += follow.get_data()[0]
                goaldistanceright += follow.get_data()[1]
            time.sleep(0.1)
        follow.stop()
        self.__leftengine.set_speed(0)
        self.__rightengine.set_speed(0)

    def correct_speed3(self,lspeed,rspeed):
        lst = [float(lspeed),float(rspeed)]
        maxipos = maxabspos(lst)
        minipos = (maxipos+1)%2
        fraction = abs(lst[minipos]/lst[maxipos])
        if abs(lst[maxipos]) > 255:
            lst[maxipos] = sign(lst[maxipos]) * 255.0
            lst[minipos] = sign(lst[minipos]) * max(MINIMUM_SPEED,255.0 * fraction)
        elif abs(lst[minipos]) < MINIMUM_SPEED:
            lst[minipos] = sign(lst[minipos]) * MINIMUM_SPEED
            lst[maxipos] = sign(lst[maxipos]) * min(255.,MINIMUM_SPEED * 1./fraction)
        return lst[0],lst[1]
    # A method to drive a given distance
    def ride_distance(self,distance,going=False):
        distance = distance - (2.1 + 0.06*distance)
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        P = math.sqrt(abs(distance)) * 5./math.sqrt(200.)
        if DEBUG:
            print 'P', P
        D =  (1./20.)
        I =  (1./50.)
        pid1 = PID.PID(P,D,I,.5)
        pid2 = PID.PID(25.,1.,7.5,.1)
        speed = MINIMUM_SPEED*2.
        if DEBUG:
            print speed
        self.__leftengine.set_speed(speed)
        self.__rightengine.set_speed(speed)
        while (speed !=0 and (self.__going or going)):
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
    elif abs(speed) < MINIMUM_SPEED or abs(speed+speed_diff) < MINIMUM_SPEED:
            if sign(speed)* speed_diff > 0:
                   return [MINIMUM_SPEED,MINIMUM_SPEED+sign(speed)*speed_diff]
            else:
                   return [MINIMUM_SPEED-sign(speed)*speed_diff,MINIMUM_SPEED]
        return [speed,speed+speed_diff]


    ## A method to rotate
    def rotate(self,radial,going):
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
        distance = self.__widthcar/2. * abs(radial)
        pid1 = PID.PID(10.,1./2.,10/2.,.6)
        pid2 = PID.PID(10.,1./2.,10/2.,.6)
        speed1 = pid1.new_value(distance,0.1)
        speed2 = pid2.new_value(-distance,0.1)
        if DEBUG:
            print 'Speed: ', speed1, speed2
        outer_engine.set_speed(speed1)
        inner_engine.set_speed(speed2)
        while (not (speed1 == 0 and speed2 == 0)) and (self.__command_going or going):
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
    # Only one wheel rotate in stead of two
    def rotate2(self,radial):
        ## reset the counters of the engiense
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        if degree < 0:
            inner_engine = self.__leftengine
        else:
            inner_engine = self.__rightengine
        distance = abs(radial) * self.__widthcar
        pid = PID.PID2(20.,1./2.,5.,0.7,distance)
        speed = MINIMUM_SPEED
        inner_engine.set_speed(MINIMUM_SPEED)
        while speed != 0 and self.__command_going:
            distance = inner_engine.get_count() * self.__gearratio * self.__perimeter
            speed = pid.new_value(distance,0.1)
            if DEBUG:
                print speed
            inner_engine.set_speed(speed)
            time.sleep(.1)

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
