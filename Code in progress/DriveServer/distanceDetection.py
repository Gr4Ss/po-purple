from Sensor import *
from time import *

sensor = DistanceSensor()
#warning levels:
# <50 : 1
# <40 : 2
# <30 : 3
# <20 : 4
# <10 : 5
warning = -1
warningLevels = [50.0,40.0,30.0,20.0,10.0]
certainity = False
getting_closer = False
counter = 0
previous_warning = -1
while True:
    if previous_warning < warning:
        counter += 1
        if counter == 3:
            getting_closer = True
    else if previous_warning != warning:
        counter = 0
    previous_warning = warning    
    distance = sensor.update_value()
    for x in range(len(warningLevels)):
        if distance <= warningLevels[x]:
            if certainity:
                warning = x
                certainity = False
		sleep(0.05)
                continue
            else:
                certainity = True
		sleep(0.05)
                continue
    if not certainity:
        warning = -1
    certainity = False
    sleep(0.05)

def getDistanceData():
    return warning, getting_closer
