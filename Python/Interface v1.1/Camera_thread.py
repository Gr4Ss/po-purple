import threading
import time

class Camera_Thread:
    def __init__(self,camera):
        self.__thread = None
        self.__going = False
        self.__camera = camera
    def on(self):
        if self.__thread == None:
            self.__going = True
            self.__thread = threading.Thread(target=self.thread)
            self.__thread.setDaemon('True')
            self.__thread.start()
    def off(self):
        if self.__thread != None
            self.__going = False
            self.__thread.join()
            self.__thread = None
    def thread(self):
        while self.__going:
            camera.take_picture()
            time.sleep(1)
