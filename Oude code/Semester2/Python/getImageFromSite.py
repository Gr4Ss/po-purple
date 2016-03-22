import urllib
from time import sleep

for i in xrange(0, 80):
    urllib.urlretrieve("http://10.42.0.23/cam.jpg", "foto" + str(i) + ".jpg")
    sleep(0.1)
