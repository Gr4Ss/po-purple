from Control import *
import time
import BrickPi_thread
el,er=Engine.Engine('A'),Engine.Engine('B')
thread = BrickPi_thread.BrickPi_Thread([el,er])
thread.on()
control = Control(el,er)
for i in range(100):
    control.drive(1,1,0.1)
    time.sleep(0.1)
