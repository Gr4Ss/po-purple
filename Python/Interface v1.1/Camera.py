import picamera
import time
import threading



## class Camera
# A class concerning the camera of the raspberry pi.
##
class Camera:
    # The camera is set to the camera of the pi
    # If an exception occur then an error message is printed
    def __init__(self):
        try:
            self.__camera = picamera.PiCamera()
        except:
            print "Error couldn't find Camera"

    # A picture is taken and saved at picture.jpg
    def take_picture(self):
        self.__camera.capture('picture.jpg')
   
