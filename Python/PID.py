class PID:
    def __init__(self,kp,kd,ki,precision):
	self.__kp = kp
	self.__kd = kd
	self.__ki = ki
	self.__precision = precision
	self.__integral = 0
	self.__error = 0

    def new_value(self,error,dt)
	if error < self.__precision:
	     return 0 
	self.__integral += error *dt
	integral = self.__integral
	differential = (error - self.__error)/dt
	proportional = error
	self.__error = error
	return self.__kp*proportional + self.__kd*differential + self.__ki * integral

