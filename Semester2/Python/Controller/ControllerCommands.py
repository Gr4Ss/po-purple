
# A method to drive forward
def forward(self):
    pid = PID.PID(15.,1/2.,2.,.05)
    global_speed = 140
    self.__leftengine.set_speed(global_speed)
    self.__rightengine.set_speed(global_speed)
    self.__leftengine.reset_count()
    self.__rightengine.reset_count()
    while self.__command_going:
        global_speed = min(global_speed+5,255)
        distance1 = self.__leftengine.get_count()*self.__perimeter*self.__gearratio
        distance2 = self.__rightengine.get_count()*self.__perimeter*self.__gearratio
        speeddif = pid.new_value(distance1-distance2,0.1)
        if speed_diff < 0:
            self.__leftengine.set_speed(global_speed)
            self.__rightengine.set_speed(global_speed + speeddif)
        else:
            self.__leftengine.set_speed(global_speed-speeddif)
            self.__rightengine.set_speed(global_speed)
        time.sleep(0.05)
    self.__leftengine.set_speed(0)
    self.__rightengine.set_speed(0)
    # A mehtod to drive backward
    def backward(self):
        pid = PID.PID(15.,1/2.,2.,.05)
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
        global_speed = 140
        self.__rightengine.set_speed(global_speed)
        self.__leftengine.set_speed(-global_speed)
        while self.__command_going:
            global_speed = min(global_speed+5,255)
            self.__rightengine.set_speed(global_speed)
            self.__leftengine.set_speed(-global_speed)
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

    def correct_speed3(self,lspeed,rspeed):
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
        while (speed !=0 and (self.__command_going or going)):
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
    def rotate(self,radial,going):
        ## reset the counters of the engiense
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        ## Determine which is the inner most wheel
        if radial > 0:
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
    def rotate2(self,radial,going):
        ## reset the counters of the engiense
        self.__leftengine.reset_count()
        self.__rightengine.reset_count()
        if radial < 0:
            inner_engine = self.__leftengine
        else:
            inner_engine = self.__rightengine
        distance = abs(radial) * self.__widthcar
        pid = PID.PID2(20.,1./2.,7.5,0.7,distance)
        speed = MINIMUM_SPEED
        inner_engine.set_speed(MINIMUM_SPEED)
        while speed != 0 and (self.__command_going or going):
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
