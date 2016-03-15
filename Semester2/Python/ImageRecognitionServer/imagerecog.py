
import time
import math
from PID import *
import get_ratio_pi_3 as ratio
import SpeedSenderSocket as sckt
dsckt = sckt.SpeedSenderSocket('10.42.0.23',6001)

def run():
    minimum_speed = 70.
    maximum_speed = 95.
    ratio_queue = [0]
    layout_queue = ["normal_straight"]
    last_ratio = 0
    direction_list = ["left","left","right"]
    x_wheel_left = 0
    y_wheel_left = 287
    x_wheel_right = 480
    y_wheel_right = 287
    last_ratio = 0.0
    column_factor = 0.02 # <0.5
    row_factor = 0.02   # <0.5
    des = 0
    pd1 = PD(50.,20.,0.)
    pid2 = PID(1.,.0,.0,0.)
    while True:
        start = time.time()
        try:
        	rat,layout_queue,ratio_queue,direction_list = ratio.get_ratio('/dev/shm/cam.jpg',x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
	        last_ratio,column_factor, row_factor,ratio_queue,layout_queue,direction_list)
        except:
            print 'ERROR'
            rat = last_ratio
            last_ratio = rat
        if rat>0:
            rat = abs(rat)
            global_speed = pd1.value(math.log(1./rat),0.1)
            global_speed = min(max(minimum_speed,global_speed),maximum_speed)
            new_ratio = 1-pid2.value(rat,0.1)
            if new_ratio <0.2:
                data = (global_speed,global_speed*-1)
            else:
                data = (global_speed,global_speed*new_ratio*1.5)
        elif rat == 0:
            data = (maximum_speed,maximum_speed)
        else:
            rat = abs(rat)
            global_speed = pd1.value(math.log(1./(rat)),0.1)
            global_speed = min(max(minimum_speed,global_speed),maximum_speed)
            new_ratio = 1-pid2.value(rat,0.1)
            if new_ratio <0.2:
                data = (global_speed*-1,global_speed)
            else:
                data = (global_speed*new_ratio*1.5,global_speed)
        dsckt.send(data)
	end = time.time()
	print end -start
	if end -start <0.1:
	    time.sleep(0.1 -(end-start))
	
run()
