import picamera


## class Camera
# A class concerning the camera of the raspberry pi.
##
class Camera:
    # The camera is set to the camera of the pi
    # If an exception occur then an error message is printed
    def __init__(self):
        try:
            self.__camera = picamera.PiCamera()
        except:
            print "Error couldn't find Camera"

    # A picture is taken and saved at picture.jpg
    def take_picture(self, res1=720, res2=480):
        self.__camera.resolution = (res1, res2)
        self.__camera.capture('picture.jpg')
   
