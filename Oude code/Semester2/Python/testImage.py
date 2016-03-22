from Image_1 import *
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
if __name__ == '__main__':
    images = ['cam.jpg','cam2.jpg','cam.jpg','cam2.jpg','cam.jpg','cam2.jpg','cam.jpg','cam2.jpg','cam.jpg','cam2.jpg','cam.jpg','cam2.jpg']
    for image in images:


        #start = time.time()
        #im = load_image(image)
        #IMAGE_SIZE = im.shape
        #a = fast_check_row(IMAGE_SIZE[0]*0.9,im)
        #b= fast_check_row(IMAGE_SIZE[0]*0.8,im)
        #c = fast_check_column(IMAGE_SIZE[1]*0.2,im)
        #d = fast_check_column(IMAGE_SIZE[1]*0.8,im)
        #end = time.time()
        #print 'Check 1', end - start
        #plt.plot([x[0] for x in a ],[x[1] for x in a ],'bo',[x[0] for x in b ],[x[1] for x in b ],'bo',[x[0] for x in c ],[x[1] for x in c ],'go',[x[0] for x in d ],[x[1] for x in d ],'go')
        #plt.hold(True)
        #plt.imshow(im,cmap='gray')
        #plt.show()


        start = time.time()
        im = load_image2(image)
        c1 = time.time()
        print 'Load Image', c1- start
        IMAGE_SIZE = im.size
	c = fast_check_column2(int(IMAGE_SIZE[0]*0.2),im)
        a = fast_check_row3(int(IMAGE_SIZE[1]*0.7),im)
        b= fast_check_row3(int(IMAGE_SIZE[1]*0.8),im)
        c2 = time.time()
        print 'Rows', c2-c1
        c = fast_check_column3(int(IMAGE_SIZE[0]*0.2),im)
        d = fast_check_column3(int(IMAGE_SIZE[0]*0.8),im)
        end = time.time()
        print 'Columns', end - c2
        print 'Check 3', end - start
        start = time.time()
        im = load_image2(image)
        c3 = time.time()
        print 'Load Image2', c3-start
        IMAGE_SIZE = im.size
        a = fast_check_row2(int(IMAGE_SIZE[1]*0.7),im)
        b= fast_check_row2(int(IMAGE_SIZE[1]*0.8),im)
        c4 = time.time()
        print 'Row2',c4-c1
        c = fast_check_column2(int(IMAGE_SIZE[0]*0.2),im)
        d = fast_check_column2(int(IMAGE_SIZE[0]*0.8),im)
        end = time.time()
        print 'Column', end-c4
        print 'Check 2', end - start
        #plt.plot([x[0] for x in a ],[x[1] for x in a ],'bo',[x[0] for x in b ],[x[1] for x in b ],'bo',[x[0] for x in c ],[x[1] for x in c ],'go',[x[0] for x in d ],[x[1] for x in d ],'go')
        #plt.hold(True)
        #plt.imshow(im,cmap='gray')
        #plt.show()
