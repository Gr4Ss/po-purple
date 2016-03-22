from Image import *

class Driver:
    def __init__(self,pictureadress,debug):
        self.__current_image = None
        self.__time_image = None
        self.__nb_bad_pictures = None
        self.__picture_adress = pictureadress
        self.__DEBUG = debug
    def  check_new_image(self):
        image = load_image(self.__picture_adress)
        if self.__DEBUG:
            show_image(image)
        width,height = image.shape
        row1 = fast_check_row(int(0.9*height))
        row2 = fast_check_row(int(0.8*height))
        # TO DO: REMOVE NOISE
        # TO DO: CHECK CROSSINGS + ROUTE
        if len(row1) == 2 and len(row2) == 2:
            dxl = (row1[0][0]-row2[0][0])/(row1[0][1]-row2[0][1])
            dxr = (row1[1][0]-row2[1][0])/(row1[1][1]-row2[1][1])
            # TO DO: CHECK IF dxl and dxr don't differ to much
            # TO DO: Calculate distance left/right wheel

        else:
            # TO DO check row 0.1*height, 0.2* height
            pass
