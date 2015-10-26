import threading
import time

class GPIO_Thread:
    def __init__(self,sensors):
	self.__thread = None
	self.__going = False
	self.__sensors = sensors
    def on(self):
	self.__going = True
	self.__thread = threading.Thread(target=self.thread)
	self.__thread.setDaemon('True')
	self.__thread.start()
    def off(self):
	self.__going = False
	self.__thread.join()
	self.__thread = None
    def thread(self):
	while self.__going:
	    for i in self.__sensors:
		i.update_value()
	    time.sleep(0.1)
