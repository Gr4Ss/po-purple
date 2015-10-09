import picamera
import time
import threading

class Camera:
    def __init__(self):
        self.__camera = picamera.PiCamera()
        self.__going = False
        self.__thread = None
    def take_pictures(self):
        while self.__going:
            self.__camera.capture('picture')
            time.sleep(1)
    def on(self):
        self.__going = True
        self.__thread = threading.Thread(target=self.__take_pictures)
        self.__thread.setDaemon('True')
        self.__thread.start()
    def off(self):
        self.__going = False
        self.__thread = None
