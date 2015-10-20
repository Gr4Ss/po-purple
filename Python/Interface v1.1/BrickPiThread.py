import threading
from BrickPi import *

class BrickPiThread:
    def __init__(self,motoren,sensoren):
        self.__engines = motoren
        self.__sensors = sensoren
        self.__going = False
        self.__thread = None
    def on(self):
        self.__going = True
        self.__thread = threading.Thread(target=self.thread)
        self.__thread.setDaemon('True')
        self.__thread.start()
    def off(self):
        self.__going = False
        self.__thread = None
    def thread(self):
	k = 0
        while self.__going:
            for i in self.__engines:
                i.update_value()
            BrickPiUpdateValues()
            k += 1
            if k == 10:
                k = 0
                for j in self.__sensors:
                    j.update_value()
            time.sleep(0.01)
