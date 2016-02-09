from Control import *
import time
import BrickPi_thread
thread = BrickPi_thread.BrickPi_thread()
thread.on()
for (i in range(100)):
    drive(1,1,0.1)
    time.sleep(0.1)
