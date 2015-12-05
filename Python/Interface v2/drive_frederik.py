
class Frederik:
    global MINIMUM_SPEED
    def __init__(self):
        # Storing the engines of this car
        #self.__widthcar = controller.get_car_width()
        self.__values = []
        self.__going = True
    def stop():
        self.__going = False
    def flush(self):
        self.__values = []
        self.__distance = (0,0)
        controller.flush_engines()
    def add_new_values(self,values):
        for value in values:
            self.__values.append(value)
    def get_data(self):
        if len(self.__values) > 0:
            return self.__values[0]
        else:
            return (0,0)
