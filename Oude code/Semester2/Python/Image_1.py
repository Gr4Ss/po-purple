import PIL.Image as Image
import numpy as np
import scipy.signal as sig
import time

# Improvements?
#  - Other mask eg Kroon, Scharr ???
#  - Other / dynamic treshholding
sobelX = 1/2.*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
sobelY = 1/2.*np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

pieterX = 1/18.*np.array([[-3,-6,0,6,3],[-6,-12,0,12,6],[-3,-6,0,6,3]])
pieterY = 1/18.*np.array([[-3,-6,-3],[-6,-12,-6],[0,0,0],[6,12,6],[3,6,3]])
pieterYF = 1/18.*np.array([[-3,-6,-3],[-6,-12,-6],[0,0,0],[6,12,6],[3,6,3]],order='F')
# Loads the image at the given adres
def load_image(adres):
    img = Image.open(adres)
    array = np.array(img)
    return array
def load_image2(adres):
    img = Image.open(adres)
    return img
# Convert image to rgb
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray
# Convert image to rgb
def rgb2gray2(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = np.float32(0.2989) * r + np.float32(0.5870) * g + np.float32(0.1140) * b
    return gray

# Method to show the image using matplotlib
def show_image(image):
    plt.imshow(image,cmap='gray')
    plt.show()

# Method to fast check for big black-white gradient shift
# Returns 1 point for every black-white pass
# Only passes in horizontal direction are detected
def fast_check_column(column,image,start=0,end=-1):
    global pieterY
    TRESHHOLD = 25
    gray = rgb2gray(image[start:end,column-1:column+2])
    # Convoluting the column + columns to the left and the right  with the sobel mask
    Gy = np.abs(sig.convolve2d(gray,pieterY,'same'))
    # Check where in the colom the gradient is bigger than the threshhold
    # + The +1 comes from here !!!!
    t = np.where(Gy[3:-3,1]>TRESHHOLD)[0]+3
    # Thinning the convolution creates 4/5 point for each shift
    # Hold only the biggest one

    i = t.shape[0]-1
    while i >= 0:
        if Gy[t[i],1] <= Gy[t[i]-1,1]  or Gy[t[i],1] <  Gy[t[i]+1,1]:
            t = np.delete(t,i)
        i-=1

    return [(column,t[i]+start) for i in range(t.shape[0])]
# Method to fast check for big black-white gradient shift
# Returns 1 point for every black-white pass
# Only passes in horizontal direction are detected
def fast_check_column2(column,image,start=0,end=-1):
    global pieterY
    if end == -1:
        end = image.size[1]
    img = image.crop((column-1,start,column+2,end))
    npimg = np.array(img)

    TRESHHOLD = 25
    gray = rgb2gray(npimg)
    # Convoluting the column + columns to the left and the right  with the sobel mask
    Gy = np.abs(sig.convolve2d(gray,pieterY,'valid'))
    # Check where in the colom the gradient is bigger than the threshhold
    # + The +1 comes from here !!!!
    t = np.where(Gy[3:-3,0]>TRESHHOLD)[0]+3
    # Thinning the convolution creates 4/5 point for each shift
    # Hold only the biggest one
    return [(column,t[i]+start) for i in xrange(t.shape[0]) if not check_neighbours_y(Gy,t,i)]
def fast_check_column3(column,image,start=0,end=-1):
    t1 = time.time()
    if end == -1:
        end = image.size[1]
    img = image.crop((column-1,start,column+2,end))
    npimg = np.array(img,order='F')

    TRESHHOLD = 25.0
    gray = rgb2gray(npimg)
    # Convoluting the column + columns to the left and the right  with the sobel mask
    Gy = np.abs(sig.convolve2d(gray,pieterYF,'valid'))
    # Check where in the colom the gradient is bigger than the threshhold
    # + The +1 comes from here !!!!
    t = np.where(Gy[:,0]>TRESHHOLD)[0]
    # Thinning the convolution creates 4/5 point for each shift
    # Hold only the biggest one
    print time.time() - t1
    return [(column,(t[i]+start)) for i in xrange(t.shape[0]) if not check_neighbours_y(Gy,t,i)]
def check_neighbours_y(Gy,t,i):
    return Gy[t[i],0] <= Gy[t[i]-1,0]  or Gy[t[i],0] <  Gy[t[i]+1,0]
def fast_check_row2(row,image,start=0,end=-1):
    global pieterX
    if end == -1:
        end = image.size[0]
    TRESHHOLD = 25
    img = image.crop((start,row-1,end,row+2))
    npimg = np.array(img)
    gray = rgb2gray(npimg)
    Gx = np.abs(sig.convolve2d(gray,pieterX,'valid'))
    t = np.where(Gx[0,3:-3]>TRESHHOLD)[0]+3
    return [(t[i]+start,row) for i in xrange(t.shape[0]) if not check_neighbours(Gx,t,i)]
def fast_check_row3(row,image,start=0,end=-1):
    t1= time.time()
    if end == -1:
        end = image.size[0]
    TRESHHOLD = 25
    img = image.crop((start,row-1,end,row+2))
    npimg = np.array(img)
    gray = rgb2gray(npimg)
    Gx = np.abs(sig.convolve2d(gray,pieterX,'valid'))
    t = np.where(Gx[0,:]>TRESHHOLD)[0]
    print 'ri', time.time() - t1
    return [((t[i]+start),row) for i in xrange(t.shape[0]) if not check_neighbours(Gx,t,i)]

def check_neighbours(Gx,t,i):
    return Gx[0,t[i]] <= Gx[0,t[i]-1]  or Gx[0,t[i]] <  Gx[0,t[i]+1]
# Method to fast check for big black-white gradient shift
# Returns 1 point for every black-white pass
# Only vertical changes are detected
def fast_check_row(row,image,start=0,end=-1):
    global pieterX
    TRESHHOLD = 25

    gray = rgb2gray(image[row-1:row+2,start:end])
    Gx = np.abs(sig.convolve2d(gray,pieterX,'same'))

    t = np.where(Gx[1,3:-3]>TRESHHOLD)[0]+3

    i = t.shape[0]-1
    while i >= 0:
        if Gx[1,t[i]] <= Gx[1,t[i]-1]  or Gx[1,t[i]] <  Gx[1,t[i]+1]:
            t = np.delete(t,i)
        i -= 1

    return [(t[i]+start,row) for i in range(t.shape[0])]
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
