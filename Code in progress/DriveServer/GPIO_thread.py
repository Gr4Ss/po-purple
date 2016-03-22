import threading
import time
# A thread concerning the GPIO sensors
class GPIO_Thread:
    def __init__(self,sensors):
	self.__thread = None
	self.__going = False
	self.__sensors = sensors
    # Method to turn thread on.
    def on(self):
        if self.__thread == None:
            # First set thread on
            self.__going = True
            # Set the thread
            self.__thread = threading.Thread(target=self.thread)
            # Deamonise the thread
            self.__thread.setDaemon('True')
            # Start the thread
            self.__thread.start()
        else:
            print 'First turn the ongoing thread off'
    def off(self):
        if self.__thread != None:
            self.__going = False
            self.__thread.join()
            self.__thread = None
        else:
            print 'No thread to turn off'
    def thread(self):
	while self.__going:
	    for i in self.__sensors:
		i.update_value()
	    time.sleep(0.1)
