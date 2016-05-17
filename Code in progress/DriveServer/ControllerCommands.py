import time
import PID
import Engine
import math
import Light
from utility import *
from follow_parcours import *
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../Socket")
from sockets_client import *
Leftengine = None
Rightengine = None
Perimeter = None
Gearratio = None
Widthcar = None
Distancesensor = None
Rt = None
Init = False
Going = False
DEBUG = True
Socket = None
LeftLamp = None
RightLamp = None

def init(leftengine,rightengine,distancesensor,perimeter,gearratio,widthcar,lled,rled):
    global Leftengine, Rightengine, Distancesensor, Perimeter, Gearratio, Widthcar,  Init,Rt
    print 'INIT'
    if isinstance(leftengine,Engine.Engine) and isinstance(rightengine,Engine.Engine) and isinstance(perimeter,float) and isinstance(gearratio,float) and isinstance(widthcar,float):
        print leftengine
        Leftengine = leftengine
        Rightengine = rightengine
        Distancesensor = distancesensor
        Perimeter = perimeter
        Gearratio = gearratio
        Widthcar = widthcar
        LeftLamp = lled
        RightLamp = rled
        Rt = Ratio((0,287),(480,287),leftengine,rightengine,LeftLamp,RightLamp,distancesensor,False,[])
        Init = True
def init_socket(IP,port):
    global Socket,Rt
    Socket = SocketClient(IP,port)
    Rt.set_socket(Socket)
def send_id(iden):
    global Socket
    data = {'Type':'ParcoursID','ID':iden}
    if Socket != None:
        if not Socket.connected:
            Socket.connect()
        Socket.send_data(data)
        print 'ParcoursID sended'

def update_position(pos):
    Rt.update_position(pos)

def follow_parcours(parcours,iden):
    Rt.reset()
    Rt.packet_delivery = False
    Rt.append_directions(parcours)
    send_id(iden)
    done = False
    while Going and not done:
        s = Rt.get_speed()
        if s[0] == 'Done' or s[1] == 'Done':
            done = True
        else:
            Leftengine.set_speed(s[0])
            Rightengine.set_speed(s[1])
    Leftengine.set_speed(0)
    Rightengine.set_speed(0)

def restart_parcours():
    Rt.packet_delivery = False
    while Going:
        s = Rt.get_speed()
        Leftengine.set_speed(s[0])
        Rightengine.set_speed(s[1])
    Leftengine.set_speed(0)
    Rightengine.set_speed(0)
def packet_delivery(pos):
    Rt.reset()
    Rt.packet_delivery = True
    Rt.update_position(pos)
    while Going:
        s = Rt.get_speed()
        Leftengine.set_speed(s[0])
        Rightengine.set_speed(s[1])
    Leftengine.set_speed(0)
    Rightengine.set_speed(0)

# A method to drive forward
# going must store a pointer to list which first element indicates the going status
def manual_straight(direction):
    if not Init:
        return False
    pid = PID.PID(15.,1/2.,2.,.05)
    global_speed = 140
    Leftengine.set_speed(direction*global_speed)
    Rightengine.set_speed(direction*global_speed)
    Leftengine.reset_count()
    Rightengine.reset_count()
    while Going:
        global_speed = min(global_speed+5,255)
        distance1 = Leftengine.get_count()*Perimeter*Gearratio
        distance2 = Rightengine.get_count()*Perimeter*Gearratio
        speed_diff = pid.value(abs(distance1)-abs(distance2),0.1)
        if speed_diff < 0:
            Leftengine.set_speed(direction*global_speed)
            Rightengine.set_speed(direction*(global_speed + speed_diff))
        else:
            Leftengine.set_speed(direction*(global_speed-speed_diff))
            Rightengine.set_speed(direction*global_speed)
        time.sleep(0.05)
    Leftengine.set_speed(0)
    Rightengine.set_speed(0)
def forward():
    manual_straight(1)
def backward():
    manual_straight(-1)
def manual_bend(directionx,directiony):
    if not Init:
        return False
    global_speed = 140
    diff = 10
    if directionx <0:
        inner_engine = Leftengine
        outer_engine = Rightengine
    else:
        inner_engine = Rightengine
        outer_engine = Leftengine
    while Going:
        global_speed = min(global_speed+5,255)
        diff = min(diff+5,100)
        outer_engine.set_speed(directiony*global_speed)
        inner_engine.set_speed(directiony*(global_speed-diff))
    Rightengine.set_speed(0)
    Leftengine.set_speed(0)
def forward_left():
    manual_bend(-1,1)
def forward_right():
    manual_bend(1,1)
def backward_left():
    manual_bend(-1,-1)
def backward_right():
    manual_bend(1,-1)
# if direction = 1 : left
# if direction = -1 : right
def manual_rotate(direction):
    global_speed = 140
    Rightengine.set_speed(direction*global_speed)
    Leftengine.set_speed(-direction*global_speed)
    while Going:
        global_speed = min(global_speed+5,255)
        Rightengine.set_speed(direction*global_speed)
        Leftengine.set_speed(-direction*global_speed)
        time.sleep(0.05)
    Rightengine.set_speed(0)
    Leftengine.set_speed(0)

def left():
    manual_rotate(1)

# A method to turn right
def right():
    manual_rotate(-1)

# A method to stop driving
def stop():
    Leftengine.set_speed(0)
    Rightengine.set_speed(0)


def correct_speed3(lspeed,rspeed):
    MINIMUM_SPEED = 100
    lst = [float(lspeed),float(rspeed)]
    maxipos = maxabspos(lst)
    minipos = (maxipos+1)%2
    fraction = abs((lst[minipos]+0.01)/(lst[maxipos]+0.0001))
    if abs(lst[maxipos]) > 255:
        lst[maxipos] = sign(lst[maxipos]) * 255.0
        lst[minipos] = sign(lst[minipos]) * max(MINIMUM_SPEED,255.0 * fraction)
    elif abs(lst[minipos]) < MINIMUM_SPEED:
        lst[minipos] = sign(lst[minipos]) * MINIMUM_SPEED
        lst[maxipos] = sign(lst[maxipos]) * min(255.,MINIMUM_SPEED * 1./fraction)
    return lst[0],lst[1]

# A method to drive a given distance
def ride_distance(distance):
    distance = distance - (2.1 + 0.06*distance)
    Leftengine.reset_count()
    Rightengine.reset_count()
    P = math.sqrt(abs(distance)) * 5./math.sqrt(200.)
    D =  1./20.
    I =  1./50.
    pid1 = PID.PID(P,D,I,.5)
    pid2 = PID.PID(25.,1.,7.5,.1)
    speed = 140
    if DEBUG:
        print speed
    Leftengine.set_speed(speed)
    Rightengine.set_speed(speed)
    while (speed !=0 and Going):
        distance1 = Leftengine.get_count()*Perimeter*Gearratio
        distance2 = Rightengine.get_count()*Perimeter*Gearratio
        if DEBUG:
            print 'Distance:', distance1, distance2
        speed = pid1.value(distance-distance1,0.01)
        speed_diff = pid2.value(distance1-distance2,0.01)
        if DEBUG:
            print 'Speed + Speed diff: ', speed, speed_diff
        lspeed,rspeed = correct_speed(speed,speed_diff)
        if DEBUG:
            print 'Corrected speed:', lspeed,rspeed
        Leftengine.set_speed(lspeed)
        Rightengine.set_speed(rspeed)
        time.sleep(0.01)
    Leftengine.set_speed(0)
    Rightengine.set_speed(0)
def correct_speed(speed,speed_diff):
    MINIMUM_SPEED = 100
    # If the speed or speed + diff is bigger then 255 a correction must happen
    if abs(speed) > 255 or abs(speed+speed_diff) > 255:
        signed = sign(speed)
        # if speed_diff bigger is bigger then 0 the left engine must slow down
        if signed*speed_diff > 0:
            return [signed*(255-sign(speed)*speed_diff),signed*255]
        # if speed_diff < 0 the right engine must slow down
        else:
            return [signed*255,signed*(255 + signed*speed_diff)]
        # If the absolute value is less then the MINIMUM_SPEED its turned up
    elif abs(speed) < MINIMUM_SPEED or abs(speed+speed_diff) < MINIMUM_SPEED:
        signed = sign(speed)
        if signed* speed_diff > 0:
               return [signed*MINIMUM_SPEED,signed* (MINIMUM_SPEED+signed*speed_diff)]
        else:
               return [signed*(MINIMUM_SPEED-signed*speed_diff),signed*MINIMUM_SPEED]
    return [speed,speed+speed_diff]


## A method to rotate
def rotate(radial):
    ## reset the counters of the engiense
    Leftengine.reset_count()
    Rightengine.reset_count()
    ## Determine which is the inner most wheel
    if radial > 0:
        inner_engine = Rightengine
        outer_engine = Leftengine
    else:
        inner_engine = Leftengine
        outer_engine = Rightengine
    # Calculate the distance to be driven
    distance = Widthcar/2. * abs(radial)
    pid1 = PID.PID(10.,1./2.,10/2.,.6)
    pid2 = PID.PID(10.,1./2.,10/2.,.6)
    speed1 = pid1.value(distance,0.1)
    speed2 = pid2.value(-distance,0.1)
    outer_engine.set_speed(speed1)
    inner_engine.set_speed(speed2)
    while (not (speed1 == 0 and speed2 == 0)) and (Going):
        distance1 = outer_engine.get_count()*Perimeter*Gearratio
        distance2 = inner_engine.get_count()*Perimeter*Gearratio
        speed1 = pid1.value(distance - distance1,0.1)
        speed2 = pid2.value(-distance - distance2,0.1)
        outer_engine.set_speed(speed1)
        inner_engine.set_speed(speed2)
        time.sleep(0.1)

def ride_polygon(distance,sides=4):
    angle = math.pi - (math.pi * (sides-2)/sides) + 0.2
    while sides > 0:
        ride_distance(distance)
        time.sleep(0.1)
        rotate(angle)
        time.sleep(0.1)
        sides -= 1



def correct_speed2(inspeed,outspeed):
    MINIMUM_SPEED = 100
    # Only usefull when outspeed bigger then inspeed
    if abs(outspeed) > abs(inspeed):
        routspeed = sign(outspeed) * min(255,abs(outspeed))
        routspeed = sign(outspeed) * max(MINIMUM_SPEED*1.1,abs(outspeed))
        rinspeed = sign(outspeed) * abs(max(abs(inspeed),5)/outspeed) * routspeed
        return rinspeed,routspeed
    return inspeed,outspeed

def ride_circ(radius):
    if abs(radius) <20:
        raise Exception
    pid1 = PID.PID(10.,1/20.,1/50.,1.)
    pid2 = PID.PID(10.,1/20.,1/50.,1.)
    if radius>0:
        inner_engine = Rightengine
        outer_engine = Leftengine
    else:
        inner_engine = Leftengine
        outer_engine = Rightengine
    inner_engine.reset_count()
    outer_engine.reset_count()
    angle_per_loop = 1.5/(float(radius))
    angle = angle_per_loop
    speed1 = pid1.value(angle*(2*math.pi*abs(radius))-0,0.1)
    speed2 = pid2.value(angle*(2*math.pi*(abs(radius)+ 0))-0,0.1)
    inner_engine.set_speed(speed1)
    outer_engine.set_speed(speed2)
    while (not (speed1==0 and speed2==0)) and Going:
        distance1 = inner_engine.get_count()*Perimeter*Gearratio
        distance2 = outer_engine.get_count()*Perimeter*Gearratio
        if DEBUG:
            print 'Distance: ', distance1, distance2
        speed1 = pid1.value(angle*abs(radius)-distance1,0.1)
        speed2 = pid2.value(angle*(abs(radius)+ Widthcar)-distance2,0.1)
        if DEBUG:
            print 'Speed: ',speed1,speed2
        ## Wat volgt is misschien nuttig
        ispeed, ospeed = correct_speed2(speed1,speed2)
        if DEBUG:
            print 'Corrected speed: ', ispeed, ospeed
        inner_engine.set_speed(ispeed)
        outer_engine.set_speed(ospeed)
        if angle <= 2*math.pi + 0.3:
            angle += angle_per_loop
        time.sleep(0.1)
    inner_engine.set_speed(0)
    outer_engine.set_speed(0)
