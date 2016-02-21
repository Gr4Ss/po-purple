from Image_1 import *
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
if __name__ == '__main__':
    images = ['cam.jpg','cam2.jpg']
    for image in images:
        start = time.time()
        im = load_image(image)
        r4,c4 = fast_check_row(IMAGE_SIZE[0]*0.9,gray)
        rt1,ct1 = fast_check_row(IMAGE_SIZE[0]*0.8,gray)
        r4,c4 = np.append(r4,rt1),np.append(c4,ct1)
        r5,c5 = fast_check_collom(IMAGE_SIZE[1]*0.2,gray)
        rt3,ct3 = fast_check_collom(IMAGE_SIZE[1]*0.8,gray)
        r5,c5 = np.append(r5,rt3),np.append(c5,ct3)
        end = time.time()
        print 'Check', end - start
        plt.plot(c4,r4,'bo',c5,r5,'go')
        plt.hold(True)
        plt.imshow(im,cmap='gray')
        plt.show()
