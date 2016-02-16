import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.signal as sig
import matplotlib
import time
import Image
sobelX = 1/2.*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
sobelY = 1/2.*np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

def show_image(image):
    plt.imshow(image,cmap='gray')
    plt.show()
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def fast_check_collom(collom,image):
    global sobelY
    TRESHHOLD = 35
    result_row = np.empty(0)
    result_collom = np.empty(0)
    temp = image[:,collom-1:collom+2]
    Gy = np.abs(sig.convolve2d(temp,sobelY,'same'))
    t = np.where(Gy[1:-2,1]>TRESHHOLD)[0]
    i = 0
    while i < t.shape[0]:
        if t[i]+1 < Gy.shape[0] and t[i]-1>0:
            if Gy[t[i]+1,1] <= Gy[t[i],1]  or Gy[t[i]+1,1] <  Gy[t[i]+2,1]:
                t = np.delete(t,i)
            else:
                i+=1
        else:
            i+=1
    result_row = np.append(result_row,t+1)
    result_collom = np.append(result_collom,np.ones(t.shape)*collom)
    return result_row,result_collom

def fast_check_row(row,image):
    global sobelX
    TRESHHOLD = 35
    result_row = np.empty(0)
    result_collom = np.empty(0)
    temp = image[row-1:row+2,:]
    Gx = np.abs(sig.convolve2d(temp,sobelX,'same'))
    t = np.where(Gx[1,1:-2]>TRESHHOLD)[0]
    i = 0
    while i < t.shape[0]:
        if t[i]+1 < Gx.shape[1] and t[i]-1>0:
            if Gx[1,t[i]+1] <= Gx[1,t[i]]  or Gx[1,t[i]+1] <  Gx[1,t[i]+2]:
                t = np.delete(t,i)
            else:
                i+=1
        else:
            i+=1
    result_row = np.append(result_row,np.ones(t.shape)*row)
    result_collom = np.append(result_collom,t+1)
    return result_row,result_collom

def check_mask(a,d1,d2,c,r,h,image_size,image):
    global sobelX,sobelY
    TRESHHOLD = 1000
    result_row = np.empty(0)
    result_collom = np.empty(0)
    result_theta = np.empty(0)
    result_G = np.empty(0)
    for i in xrange(d1,d2):
        temp = image[image_size-a-1:image_size-a+2,i-1:i+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
                result_row = np.append(result_row,[image_size-a])
                result_collom = np.append(result_collom,[i])
                result_G = np.append(result_G,G)
                result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    for j in xrange(image_size-(a+c),image_size-a):
        temp = image[j-1:j+2,d1-1:d1+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
            result_row = np.append(result_row,[j])
            result_collom = np.append(result_collom,[d1])
            result_G = np.append(result_G,G)
            result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    for k in xrange(image_size-(a+c),image_size-a):
        temp = image[j-1:j+2,d2-1:d2+2]
        Gx = np.sum(sobelX*temp)
        Gy = np.sum(sobelY*temp)
        G = Gx*Gx + Gy*Gy
        if G > TRESHHOLD:
            result_row = np.append(result_row,[k])
            result_collom = np.append(result_collom,[d2])
            result_G = np.append(result_G,G)
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
            result_G = np.append(result_G,G)
            result_theta = np.append(result_theta,np.arctan(Gy/Gx))
    return result_row,result_collom,result_G,result_theta


def canny(gray):
    TRESHOLD = 25
    sobelX = 1/4.*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    sobelY = 1/4.*np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    start = time.time()
    Gx = np.abs(sig.convolve2d(gray,sobelX))
    Gy = np.abs(sig.convolve2d(gray,sobelY))
    end = time.time()
    print 'Convolution takes: ', end-start
    G = np.sqrt(Gx**2+Gy**2)[4:-4,4:-4]
    print np.max(G)
    theta = np.arctan(Gy/Gx)
    t = np.where(G>TRESHOLD)
    t = [t[0], t[1]]
    i = 0
    while i < len(t[0]):
        if t[0][i]+1 < G.shape[0] and t[1][i]+1 < G.shape[1]:
            if (-0.125*np.pi<= theta[t[0][i]][t[1][i]] and theta[t[0][i]][t[1][i]]<=0.125*np.pi) or np.isnan(theta[t[0][i]][t[1][i]]):
                if G[t[0][i]][t[1][i]] < G[t[0][i]][t[1][i]-1]  or G[t[0][i]][t[1][i]] <  G[t[0][i]][t[1][i]+1]:
                    t[0] = np.delete(t[0],i)
                    t[1] = np.delete(t[1],i)
                else:
                    i+=1
            elif 0.125*np.pi< theta[t[0][i]][t[1][i]] and theta[t[0][i]][t[1][i]]<=0.375*np.pi:
                if G[t[0][i]][t[1][i]] < G[t[0][i]+1][t[1][i]+1]  or G[t[0][i]][t[1][i]] <  G[t[0][i]-1][t[1][i]-1]:
                    t[0] = np.delete(t[0],i)
                    t[1] = np.delete(t[1],i)
                else:
                    i+=1
            elif -0.375*np.pi<= theta[t[0][i]][t[1][i]] and theta[t[0][i]][t[1][i]]<-0.125*np.pi:
                if G[t[0][i]][t[1][i]] < G[t[0][i]-1][t[1][i]+1]  or G[t[0][i]][t[1][i]] <  G[t[0][i]+1][t[1][i]-1]:
                    t[0] = np.delete(t[0],i)
                    t[1] = np.delete(t[1],i)
                else:
                    i+=1
            else:
                 if G[t[0][i]][t[1][i]] < G[t[0][i]+1][t[1][i]]  or G[t[0][i]][t[1][i]] <  G[t[0][i]-1][t[1][i]]:
                    t[0] = np.delete(t[0],i)
                    t[1] = np.delete(t[1],i)
                 else:
                    i+=1
        else:
            t[0] = np.delete(t[0],i)
            t[1] = np.delete(t[1],i)
    return t[1],t[0]

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
    start = time.time()
    img = mpimg.imread('cam.jpg')
    #gray = Image.open('cam.jpg').convert('LA')
    #show_image(img)
    #gray = matplotlib.colors.rgb_to_hsv(img)
    gray = rgb2gray(img)
    #gray = img[:,:,3]
    #show_image(gray)
    IMAGE_SIZE = gray.shape
    #print IMAGE_SIZE
    #a = int(0.1*IMAGE_SIZE[0])
    #b = int(0.6*IMAGE_SIZE[1])
    #c = int(0.5*IMAGE_SIZE[0])
    #h = int(0.3*IMAGE_SIZE[0])
    #r = int(b**2/(8.*h) + h/2.)
    #d1 = int((IMAGE_SIZE[1]-b)/2)
    #d2 = IMAGE_SIZE[1]-d1
    #print a,d1,d2,c,r
    #r1,c1 = generate_mask(a,d1,d2,c,r,h,IMAGE_SIZE[0])
    #start = time.time()
    #r2,c2,G,theta = check_mask(a,d1,d2,c,r,h,IMAGE_SIZE[0],gray)
    #print r2,c2
    #end = time.time()
    #print end-start
    #start = time.time()
    r4,c4 = fast_check_row(IMAGE_SIZE[0]*0.9,gray)
    rt1,ct1 = fast_check_row(IMAGE_SIZE[0]*0.8,gray)
    r4,c4 = np.append(r4,rt1),np.append(c4,ct1)
    rt2,ct2 = fast_check_collom(IMAGE_SIZE[1]*0.2,gray)
    r4,c4 = np.append(r4,rt2),np.append(c4,ct2)
    rt3,ct3 = fast_check_collom(IMAGE_SIZE[1]*0.8,gray)
    r4,c4 = np.append(r4,rt3),np.append(c4,ct3)
    end = time.time()
    print 'row collom check', end - start
    #plt.plot(c1,r1,'go')
    #plt.hold(True)
    #plt.plot(c2,r2,'ro')
    #plt.plot([50],[150],'go')
    #plt.hold(True)
    plt.plot(c4,r4,'bo')
    plt.hold(True)
    plt.imshow(gray,cmap='gray')
    plt.show()
    #x3,y3 = canny(gray)
    #plt.plot(x3,y3,'go')
    #plt.hold(True)
    #plt.imshow(gray,cmap='gray')
    #plt.show()
if __name__ == '__main__':
    main()
