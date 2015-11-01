import threading
import time
# A thread concersing the camera thread
class Camera_Thread:
    # The thread is not yet going
    def __init__(self,camera):
        self.__thread = None
        self.__going = False
        self.__camera = camera
    # Method to turn the thread on
    def on(self):
        if self.__thread == None:
            self.__going = True
            self.__thread = threading.Thread(target=self.thread)
            self.__thread.setDaemon('True')
            self.__thread.start()
        else:
            print 'First turn the ongoing thread off'
    # Method to turn thread off
    def off(self):
        if self.__thread != None
            self.__going = False
            self.__thread.join()
            self.__thread = None
        else:
            print 'No thread to turn off'
    # While the thread is going, every second a picture is taken.
    def thread(self):
        while self.__going:
            camera.take_picture()
            time.sleep(1)
