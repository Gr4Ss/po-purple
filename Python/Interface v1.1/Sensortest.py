from Sensor import *

sensor = MindstromSensor(2,'EV3_INFRARED_M0')
while True:
    sensor.update_value()
    print sensor.get_value()
