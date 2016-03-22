import urllib
from time import sleep

for i in xrange(0, 80):
    urllib.urlretrieve("http://192.168.0.101/cam.jpg", "foto" + str(i) + ".jpg")
    sleep(0.11)
