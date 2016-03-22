import PIL.Image as Image
import numpy as np
import scipy.signal as sig


pieterX = 1/18.*np.array([[-3,-6,0,6,3],[-6,-12,0,12,6],[-3,-6,0,6,3]])
pieterY = 1/18.*np.array([[-3,-6,-3],[-6,-12,-6],[0,0,0],[6,12,6],[3,6,3]])

def load_image(adres):
    img = Image.open(adres)
    return img

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def fast_check_column(column,image,start=0,end=-1):
    global pieterY
    if end == -1:
        end = image.size[1]
    img = image.crop((column-1,start,column+2,end))
    npimg = np.array(img)

    TRESHHOLD = 26
    gray = rgb2gray(npimg)
    # Convoluting the column + columns to the left and the right  with the sobel mask
    Gy = np.abs(sig.convolve2d(gray,pieterY,'valid'))
    # Check where in the colom the gradient is bigger than the threshhold
    # + The +1 comes from here !!!!
    t = np.where(Gy[3:-3,0]>TRESHHOLD)[0]+3
    # Thinning the convolution creates 4/5 point for each shift
    # Hold only the biggest one
    return [(column,t[i]+start) for i in xrange(t.shape[0]) if not check_neighbours_y(Gy,t,i)]
def check_neighbours_y(Gy,t,i):
    return Gy[t[i],0] <= Gy[t[i]-1,0]  or Gy[t[i],0] <  Gy[t[i]+1,0]
def fast_check_row(row,image,start=0,end=-1):
    global pieterX
    if end == -1:
        end = image.size[0]
    TRESHHOLD = 26
    img = image.crop((start,row-1,end,row+2))
    npimg = np.array(img)
    gray = rgb2gray(npimg)
    Gx = np.abs(sig.convolve2d(gray,pieterX,'valid'))
    t = np.where(Gx[0,3:-3]>TRESHHOLD)[0]+3
    return [(t[i]+start,row) for i in xrange(t.shape[0]) if not check_neighbours_x(Gx,t,i)]
def check_neighbours_x(Gx,t,i):
    return Gx[0,t[i]] <= Gx[0,t[i]-1]  or Gx[0,t[i]] <  Gx[0,t[i]+1]
