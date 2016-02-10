import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.signal as sig
import time
sobelX = 1/2.*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
sobelY = 1/2.*np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

def show_image(image):
    plt.imshow(image,cmap='gray')
    plt.show()
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray
def check_mask(a,d1,d2,c,r,h,image_size,image):
    global sobelX,sobelY
    TRESHHOLD = 750
    result_row = np.empty(0)
    result_collom = np.empty(0)
    result_theta = np.empty(0)
    for i in xrange(d1,d2):
        temp = image[image_size-a-1:image_size-a+2,i-1:i+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
            result_row = np.append(result_row,[image_size-a])
            result_collom = np.append(result_collom,[i])
            result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    for j in xrange(image_size-(a+c),image_size-a):
        temp = image[j-1:j+2,d1-1:d1+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
            result_row = np.append(result_row,[j])
            result_collom = np.append(result_collom,[d1])
            result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    for k in xrange(image_size-(a+c),image_size-a):
        temp = image[j-1:j+2,d2-1:d2+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
            result_row = np.append(result_row,[k])
            result_collom = np.append(result_collom,[d2])
            result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    x0 = (d1+d2)/2
    for l in range(d1,d2):
        rnb = int(-np.sqrt(r**2-(l-x0)**2)+image_size - (a+c-(r-h)))
        temp = image[rnb-1:rnb+2,l-1:l+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
            result_row = np.append(result_row,[rnb])
            result_collom = np.append(result_collom,[l])
            result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    return result_row,result_collom

def generate_mask(a,d1,d2,c,r,h,image_size):
    row,col = np.empty(0),np.empty(0)
    for i in xrange(d1,d2):
        row = np.append(row,[image_size-a])
        col = np.append(col,[i])
    for j in xrange(image_size-(a+c),image_size-a):
        row = np.append(row,[j])
        col = np.append(col,[d1])
    for k in xrange(image_size-(a+c),image_size-a):
        row = np.append(row,[k])
        col = np.append(col,[d2])
    x0 = (d1+d2)/2
    for l in range(d1,d2):
        row = np.append(row,[int(-np.sqrt(r**2-(l-x0)**2)+image_size - (a+c-(r-h)))])
        col = np.append(col,[l])
    return row,col

def to_left_bottom_origin(row,col,image_size):
    return col,image_size[0] - row

def main():
    img = mpimg.imread('picture.jpg')
    show_image(img)
    gray = rgb2gray(img)
    show_image(gray)
    IMAGE_SIZE = gray.shape
    print IMAGE_SIZE
    a = int(0.1*IMAGE_SIZE[0])
    b = int(0.6*IMAGE_SIZE[1])
    c = int(0.5*IMAGE_SIZE[0])
    h = int(0.3*IMAGE_SIZE[0])
    r = int(b**2/(8.*h) + h/2.)
    d1 = int((IMAGE_SIZE[1]-b)/2)
    d2 = IMAGE_SIZE[1]-d1
    print a,d1,d2,c,r
    r1,c1 = generate_mask(a,d1,d2,c,r,h,IMAGE_SIZE[0])
    start = time.time()
    r2,c2 = check_mask(a,d1,d2,c,r,h,IMAGE_SIZE[0],gray)
    end = time.time()
    print end-start
    plt.plot(c1,r1,'go')
    plt.hold(True)
    plt.plot(c2,r2,'ro')
    #plt.plot([50],[150],'go')
    plt.hold(True)
    plt.imshow(gray,cmap='gray')
    plt.show()
if __name__ == '__main__':
    main()
