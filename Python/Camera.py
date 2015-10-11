import picamera
import time
import threading


time = 1
## class Camera
# A class concerning the camera of the raspberry pi.
##
class Camera:
    global time
    # @post The camera is set to the camera of the pi
    # @post The camera is not yet going
    # @post There is yet no thread
    def __init__(self):
        self.__camera = picamera.PiCamera()
        self.__going = False
        self.__thread = None
    # While self.__going is True, each global_time a picture (saved as picture.jpg) is taken.
    def take_pictures(self):
        while self.__going:
            self.__camera.capture('picture.jpg')
            time.sleep(time)
    # Start a new thread with take pictures
    # @post The thread is set to new thread
    # @post Camera is going
    def on(self):
        self.__going = True
        self.__thread = threading.Thread(target=self.__take_pictures)
        self.__thread.setDaemon('True')
        self.__thread.start()
    # To stop the camera
    # @post The camera is not longer going
    # @post There is no thread more
    def off(self):
        self.__going = False
        self.__thread = None
