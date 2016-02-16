import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.signal as sig
import time

# Improvements?
#  - Other mask eg Kroon, Scharr ???
#  - Other / dynamic treshholding
sobelX = 1/2.*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
sobelY = 1/2.*np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

# Loads the image at the given adres
def load_image(adres):
    img = mpimg.imread(adres)
    return rgb2gray(img)
# Convert image to rgb
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray
# Method to show the image using matplotlib
def show_image(image):
    plt.imshow(image,cmap='gray')
    plt.show()

# Method to fast check for big black-white gradient shift
# Returns 1 point for every black-white pass
# Only passes in horizontal direction are detected
def fast_check_column(column,start,end,image):
    global sobelY
    TRESHHOLD = 35
    # Convoluting the column + columns to the left and the right  with the sobel mask
    Gy = np.abs(sig.convolve2d(image[:,column-1:column+2],sobelY,'same'))
    # Check where in the colom the gradient is bigger than the threshhold
    # + The +1 comes from here !!!!
    t = np.where(Gy[start+1:end-1,1]>TRESHHOLD)[0]
    # Thinning the convolution creates 4/5 point for each shift
    # Hold only the biggest one
    i = 0
    while i < t.shape[0]:
        if t[i]+1 < Gy.shape[0] and t[i]-1>0:
            if Gy[t[i]+1,1] <= Gy[t[i],1]  or Gy[t[i]+1,1] <  Gy[t[i]+2,1]:
                t = np.delete(t,i)
            else:
                i+=1
        else:
            i+=1
    # Adding 1 because of +
    return [(t[i]+1,column) for i in range(t.shape[0])]
# Method to fast check for big black-white gradient shift
# Returns 1 point for every black-white pass
# Only vertical changes are detected
def fast_check_row(row,start,end,image):
    global sobelX
    TRESHHOLD = 35
    Gx = np.abs(sig.convolve2d(image[row-1:row+2,:],sobelX,'same'))
    t = np.where(Gx[1,start+1:end-1]>TRESHHOLD)[0]
    i = 0
    while i < t.shape[0]:
        if t[i]+1 < Gx.shape[1] and t[i]-1>0:
            if Gx[1,t[i]+1] <= Gx[1,t[i]]  or Gx[1,t[i]+1] <  Gx[1,t[i]+2]:
                t = np.delete(t,i)
            else:
                i+=1
        else:
            i+=1
    return [(row,t[i]+1) for i in range(t.shape[0])]
# A method that calculate the d between a list of points
# returns a list in the form [((p1,p2),d(p1,p2)),((p1,p3),d(p1,p3)), ...]
def calculate_distance(points):
    result = []
    for i in range(len(points)):
        for j in range(i,len(points)):
            result.append(((points[i],points[j]),d(points[i],points[j])))
    return result
# returns the square of the distance between A and B
def d(A,B):
    return (A[0]-B[0])*(A[0]-B[0]) + (A[1]-B[1])*(A[1]-B[1])
