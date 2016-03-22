import sockets_simple_client as sock

class Frederik:
    global MINIMUM_SPEED
    def __init__(self,string):
        # Storing the engines of this car
        #self.__widthcar = controller.get_car_width()
        self.__values = []
        sock.sendString(string)
    def stop():
        sock.sendString('**END**')
    def flush(self):
        self.__values = []
    def call_server(self):
        left,right = sock.fetchTables()
        self.add_new_values(left,right)
    def add_new_values(self,left,right):
        if len(left) != len(right):
            raise Exception
        for k in range(len(left)):
            tup = (left[k],right[k])
            self.__values.append(tup)
    def get_data(self):
        if len(self.__values) > 0:
            return self.__values.pop(0)
        else:
            try:
                sock.sendString('OK')
                self.call_server()
            except:
                return (0,0)
