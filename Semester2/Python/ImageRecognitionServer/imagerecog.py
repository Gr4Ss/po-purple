
import time
import math
from PID import *
import get_ratio_pi3 as ratio
import SpeedSenderSocket as sckt
dsckt = sckt.SpeedSenderSocket('10.42.0.23',6000)

def run(self):
    minimum_speed = 90.
    maximum_speed = 170.
    x_wheel_left = 0
    y_wheel_left = 287
    x_wheel_right = 480
    y_wheel_right = 287
    last_ratio = 1.0
    column_factor = 0.05 # <0.5
    row_factor = 0.05   # <0.5
    group_factor = 15
    correction = 1.0
    des = 0
    pd1 = PD(100.,50.,0.)
    pid2 = PID(1.,.0,.0,0.)
    while True:
        ratio = get_ratio(x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
                          last_ratio,
                          column_factor, row_factor,
                          correction)
        last_ratio = ratio
        if ratio < 0:
            ratio = abs(ratio)
            global_speed = pd1.value(math.log(1./(1-math.sqrt(ratio)),0.1))
            global_speed = min(max(minimum_speed,global_speed),maximum_speed)
            new_ratio = 1 - pid2(1-ratio,0.1)
            data = (global_speed,global_speed*new_ratio)
        elif ratio == 0:
            data = (maximum_speed,maximum_speed)
        else:
            global_speed = pd1.value(math.log(1./(1-math.sqrt(ratio))),0.1)
            global_speed = min(max(minimum_speed,global_speed),maximum_speed)
            new_ratio = 1 - pid.pid2(1-ratio,0.1)
            data = (global_speed*new_ratio,global_speed)
        dsckt.send(data)
