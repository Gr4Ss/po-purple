from Image_1 import *
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
if __name__ == '__main__':
    images = ['cam.jpg','cam2.jpg']
    for image in images:
        start = time.time()
        im = load_image(image)
        IMAGE_SIZE = im.shape
        a = fast_check_row(IMAGE_SIZE[0]*0.9,im)
        b= fast_check_row(IMAGE_SIZE[0]*0.8,im)
        c = fast_check_column(IMAGE_SIZE[1]*0.2,im)
        d = fast_check_column(IMAGE_SIZE[1]*0.8,im)
        end = time.time()
        print 'Check', end - start
        plt.plot([x[1] for x in a ],[x[0] for x in a ],'bo',[x[1] for x in b ],[x[0] for x in b ],'bo',[x[1] for x in c ],[x[0] for x in c ],'go',[x[1] for x in d ],[x[0] for x in d ],'go')
        plt.hold(True)
        plt.imshow(im,cmap='gray')
        plt.show()
