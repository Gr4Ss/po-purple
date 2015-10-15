import picamera
import time
import threading



## class Camera
# A class concerning the camera of the raspberry pi.
##
class Camera:
    # @post The camera is set to the camera of the pi
    # @post The camera is not yet going
    # @post There is yet no thread
    def __init__(self):
        self.__camera = picamera.PiCamera()

    # While self.__going is True, each global_time a picture (saved as picture.jpg) is taken.
    def take_picture(self):
        self.__camera.capture('picture.jpg')
   
