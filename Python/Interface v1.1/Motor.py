from BrickPi import *
BrickPiSetup()

# Class concerning the LEGO-MINDSTORM Motor
# It possible to let the motor run (back and forth) at a given power rate.
class Motor:
    def __init__(self,port):
        ## A motor is connected to a given port ('A','B','C','D')
        self.__port = port
        ## BrickPi command to enable the motor
        exec("BrickPi.MotorEnable[PORT_" + self.__port + "] = 1")
        ## speed = 0 is not running
        ## speed < 0 is running backward
        ## speed > 0 is running forward
        self.__speed = 0
	BrickPiUpdateValues()
	exec('start_angle = BrickPi.Encoder[PORT_'+self.__port+']')
	self.__start_angle = start_angle
    ## Returning the running speed of this Motor
    ## speed = 0 is not running
    ## speed < 0 is running backward
    ## speed > 0 is running forward
    def get_speed(self):
        return self.__speed
    ## Method to set the speed of this motor
    ## If the given is a float it will be round down to an int
    ## If the absolute value of the speed bigger is then 255 the speed will be set to -/+ speed
    def set_speed(self,speed):
	if abs(speed) > 255:
	    speed = 255 if (speed >0) else -255
	self.__speed = int(speed)

    ## Let's run the motor
    def update_value(self):
	exec("BrickPi.MotorSpeed[PORT_" + self.__port + "] =" + str(self.__speed))
    # A method returning the number of rotations of the motor since the last time
    # reset_count() is executed
    def get_count(self):
	exec('angle = BrickPi.Encoder[PORT_'+self.__port+']')
	return (angle-self.__start_angle)/720.
    # A method to reset the counter
    def reset_count(self):
	exec('angle = BrickPi.Encoder[PORT_'+self.__port+']')
	self.__start_angle = angle
	


 
    
  
