import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import scipy
from scipy import interpolate
#from scipy.interpolate import splder
from scipy.optimize import fsolve
import random
import time
print scipy.__version__

def createSequence(n):
    list = []
    for i in xrange(0,n):
        list.append(i)
    return list

def addFotos():
    fotoList = []
    fotoList.append('cam2')
    for i in xrange(0,10):
        fotoList.append('picture_'+str(i))
    for i in xrange(0,9):
        fotoList.append('picture_A'+str(i))
    fotoList.remove('picture_8')
    fotoList.remove('picture_A8')
    fotoList.remove('picture_A7')
    fotoList.remove('picture_4')
    
    return fotoList
    
def toGrayScale(image):
    gray_image_array = image.convert('L')
    gray_image = np.asarray(gray_image_array).copy()
    return [gray_image, gray_image_array]

def plot(pixel_list, string):
    plt.figure()
    indices = createSequence(len(pixel_list))
    plt.plot(indices, pixel_list, "x")
    print 'amount of '+ string + ' is:  ' + str(len(pixel_list))
    plt.show()

def plot2(pixel_list, width, heigth):
    plt.figure()
    plt.plot(pixel_list[0], pixel_list[1], "x")
    plt.axis([0,heigth,0,width])
    plt.show()

def plot3(pixel_list):
    plt.figure()
    plt.plot(pixel_list[0], pixel_list[1], '.')
    plt.show()
    
# calculate the lighting in an image based on gray values an order these
def calculateLighting(gray_image, width, heigth, interval, showLightingPlot):
    pixel_list = []
    for y in xrange(0, heigth/interval):
        for x in xrange(0,width/interval):
            location = (interval*x,interval*y)
            pixel_list.append(gray_image.getpixel(location))
    pixel_list = np.sort(pixel_list)
    
    if (showLightingPlot == 1):
        plot(pixel_list, 'sorted grayscale')
    return pixel_list

# calculates a tipping value of a gray image array. The consistency of the shape of
# the (ordened) curve of lighting throughout the image is used.
def calculateTippingValue(gray_image, width, heigth, interval, interval2, showLightingPlot):
    pixel_list = calculateLighting(gray_image, width, heigth, interval, showLightingPlot)
    searchedPixels = pixel_list[len(pixel_list)/2:]
    diff = []
    for i in xrange(0, (len(searchedPixels) - 1)/interval2):
        diff.append(searchedPixels[i*interval2] - searchedPixels[(i-1)*interval2])
    maximum = max(diff)
    maxindex = -1
    for i in xrange(1, len(diff)):
        if diff[i] == maximum:
            maxindex = i*interval2
    tippingValue = searchedPixels[maxindex]
    showSearchPixelsLightingPlot = 0
    showDiffLightingPlot = 0
    if (showSearchPixelsLightingPlot == 1):
        plot(searchedPixels, 'searched values')
    if (showDiffLightingPlot == 1):
        plot(diff, 'diff values')
    return tippingValue

# converts array to absolute black and white based on previously mentioned tipping value
def toBlackAndWhite(gray_image, tippingValue, showBlackAndWhite):
    gray_image[gray_image < tippingValue] = 0
    gray_image[gray_image >= tippingValue] = 255
    if showBlackAndWhite == 1:
        blackAndWhite = Image.fromarray(gray_image)
        blackAndWhite.show()
    return gray_image


def thinGroups(group_list, n):
    new_group_list = []
    for group in group_list:
        new_group = []
        x_list = group[0]
        y_list = group[1]
        k=0
        x_rem = []
        y_rem = []
        for i in xrange(0, len(x_list)):
            k+=1
            if k == n:
                x_rem.append(group[0][i])
                y_rem.append(group[1][i])
                k = 0
        new_group.append(x_rem)
        new_group.append(y_rem)
        new_group_list.append(new_group)
    return new_group_list
            

# groups pixels logiclly together
def groupPixels2(transformed_edges, large_distance):
    x_array = transformed_edges[0]
    y_array = transformed_edges[1]
    bool_in_group = np.ones(len(transformed_edges[0]), dtype=np.int_)
    group_list = []
    group_index = -1
    while True:
        if len(np.nonzero(bool_in_group)[0]) == 0:
            break
        group_index += 1
        group_list.append([[],[]])
        ind = np.where(bool_in_group==1)[0][0]
        x = x_array[ind]
        y = y_array[ind]
        group_list[-1][0].append(x)
        group_list[-1][1].append(y)
        bool_in_group[ind] = 0
        group_list, bool_in_group = addBuddies(x, y, ind,
                x_array, y_array, bool_in_group, group_list, group_index)
    return orderGroups(group_list, large_distance)

def groupPixels3(transformed_edges, large_distance):
    x_array = transformed_edges[0]
    y_array = transformed_edges[1]
    


def orderGroups(group_list, large_distance):
    new_group_list = []
    for group in group_list:
        x_list = group[0]
        y_list = group[1]
        for i in xrange(1, len(x_list)):
            x0 = x_list[i-1]
            y0 = y_list[i-1]
            x1 = x_list[i]
            y1 = y_list[i]
            distance = np.sqrt((y1-y0)**2+(x1-x0)**2)
            if distance > large_distance:
                xend = x_list[i:]
                xend.reverse()
                yend = y_list[i:]
                yend.reverse()
                new_group_list.append([xend+x_list[:i],yend+y_list[:i]])
                break
            if len(x_list)-1==i:
                new_group_list.append(group)
    return new_group_list



def f(x):
    return x*0.020

def addBuddies(x, y, index, x_array, y_array, bool_in_group, group_list, group_index):
    maxRange = f(x)
    # using quicksort ??
    xbuddies = np.where((x_array>x-maxRange) & (x_array<x+maxRange))
    ybuddies = np.where((y_array>y-maxRange) & (y_array<y+maxRange))
    buddy_indices = np.intersect1d(xbuddies, ybuddies)
    buddy_indices_remainder = []
    for buddy_index in buddy_indices:
        if bool_in_group[buddy_index] == 1:
            buddy_indices_remainder.append(buddy_index)
    buddy_indices = buddy_indices_remainder
    distance_list = []
    for buddy_index in buddy_indices:
        xb = x_array[buddy_index]
        yb = y_array[buddy_index]
        distance = np.sqrt((yb-y)**2+(xb-x)**2)
        distance_list.append(distance)
    
    sorted_buddy_indices = [x for (y,x) in sorted(zip(distance_list,buddy_indices))]
    for buddy_index in sorted_buddy_indices:
        if (buddy_index != index):
            group_list[group_index][0].append(x_array[buddy_index])
            group_list[group_index][1].append(y_array[buddy_index])
            bool_in_group[buddy_index] = 0
    sorted_buddy_indices.reverse()
    for buddy_index in sorted_buddy_indices:
        if buddy_index != index:
            group_list, bool_in_group = addBuddies(x_array[buddy_index],y_array[buddy_index], buddy_index,
                                x_array, y_array,bool_in_group, group_list, group_index)
    return group_list, bool_in_group
    
        



# returns something with unit in cm
def XToBirdsEye(x, x_start, x_middle, heigth_camera, heigth):
    x = heigth - x
    a = np.sqrt(1+(heigth_camera**2)/(x_middle**2))
    b = (2*x/heigth*(x_middle - x_start))/((a**2)*(x_middle**2))
    result = (-1)*(heigth_camera**2*b+x_start)/(x_middle*b-1)
    return result

# returns something with unit in pixels.  Inverse of XToBirdsEye.
def XToAngle(x_cm, x_start, x_middle, heigth_camera, heigth):
    theta = np.arctan(heigth_camera/x_cm)
    theta_middle = np.arctan(heigth_camera/x_middle)
    result =  (( x_cm - x_start )*np.sin(theta)*heigth)/( 2*( x_middle - x_start )*np.sin(np.pi/2 - theta + theta_middle)*np.sin(theta_middle))
    return heigth - result

# returns something with unit in cm
def YToBirdsEye(x, y, x_horizon, base_width, width, heigth):
    return (-1)*(( heigth - x_horizon )/( x - x_horizon ))*( (base_width) / (width) )*( (y) - width / 2.0 )

# returns something with unit in pixels. Inverse of YToBirdsEye.
def YToAngle(x_cm, y_cm, x_start, x_middle, heigth_camera, x_horizon, width, heigth):
    x = XToAngle(x_cm, x_start, x_middle, heigth_camera, x_horizon)
    return (-1)*y_cm/((( x - x_horizon )/( heigth - x_horizon ))*( (base_width) / (width) )) + width / 2.0


# transforms a list of pixels into a list of birds eye viewed distances
def toBirdsEye(pixel_list, x_start, x_middle, heigth_camera, x_horizon, base_width, width, heigth):
    new_distance_list = np.array([np.zeros(len(pixel_list[0]), dtype=np.float), np.zeros(len(pixel_list[0]), dtype=np.float)])
    for i in xrange(0, len(pixel_list[0])):
        x = float(pixel_list[0][i])
        y = float(pixel_list[1][i])
        x_cm = XToBirdsEye(float(x), x_start, x_middle, heigth_camera, heigth)
        y_cm = YToBirdsEye(float(x), float(y), x_horizon, base_width, width, heigth)
        new_distance_list[0][i] = x_cm
        new_distance_list[1][i] = y_cm
    return new_distance_list

# transforms a list of birds eye viewed distances to a list of pixels on the angle and heigth the camera is on
def toAngle(distance_list, x_start, x_middle, heigth_camera,  x_horizon, width, heigth, base_width):
    new_pixel_list = [[],[]]
    for i in xrange(0, len(distance_list[0])):
        x_cm = distance_list[0][i]
        y_cm = distance_list[1][i]
        theta = np.arctan(heigth_camera/x_cm)
        theta_middle = np.arctan(heigth_camera/x_middle)
        x = heigth - (( x_cm - x_start )*np.sin(theta)*heigth)/( 2*( x_middle - x_start )*np.sin(np.pi/2 - theta + theta_middle)*np.sin(theta_middle))
        y = (-1)*y_cm/((( heigth - x_horizon )/( x - x_horizon ))*( (base_width) / (width) )) + width / 2.0
        new_pixel_list[0].append(x)
        new_pixel_list[1].append(y)
    return new_pixel_list
        
def toAngleOnePixel(x_cm, y_cm, x_start, x_middle, heigth_camera, base_width, x_horizon, width, heigth):
    theta = np.arctan(heigth_camera/x_cm)
    theta_middle = np.arctan(heigth_camera/x_middle)
    x = heigth - (( x_cm - x_start )*np.sin(theta)*heigth)/( 2*( x_middle - x_start )*np.sin(np.pi/2 - theta + theta_middle)*np.sin(theta_middle))
    y = y_cm/((( x - x_horizon )/( heigth - x_horizon ))*( (base_width) / (width) )) + width / 2.0
    return x,y

def linkGroups2(bw, edges,group_list, line_width,
            x_start, x_middle,heigth_camera, base_width, x_horizon,
            width, heigth, spline_flatness, showSpline, transformed_edges):
    
    
    if showSpline == 1:
            plt.figure()


    remainder_list = []
    parallel_group_list = []

    for i in xrange(0, len(group_list)):
        group = group_list[i]
        if len(group[0]) > 4 :
            remainder_list.append(group)
            x_list = group[0]
            y_list = group[1]
            tck, u = interpolate.splprep([x_list, y_list], s=spline_flatness)
            pixels_on_spline = interpolate.splev(u, tck)
            first_derivative = interpolate.splev(u, tck, der=1)
            t,c,k = tck
            parallel_group_out = [[],[]]
            parallel_group_in = [[],[]]
            for j in xrange(0, len(pixels_on_spline[0])):
                x = pixels_on_spline[0][j]
                y = pixels_on_spline[1][j]
                dx = first_derivative[0][j]
                dy = first_derivative[1][j]
                x_parr_out = x + ((line_width/2.0)*dy)/(np.sqrt(dx**2+dy**2))
                y_parr_out = y - ((line_width/2.0)*dx)/(np.sqrt(dx**2+dy**2))
                x_parr_in = x + ((-1)*(line_width/2.0)*dy)/(np.sqrt(dx**2+dy**2))
                y_parr_in = y - ((-1)*(line_width/2.0)*dx)/(np.sqrt(dx**2+dy**2))
        
                parallel_group_out[0].append(x_parr_out)
                parallel_group_out[1].append(y_parr_out)
                parallel_group_in[0].append(x_parr_in)
                parallel_group_in[1].append(y_parr_in)
            parallel_group = getCorrectParallelGroup(bw, edges, parallel_group_out, parallel_group_in, x_start, x_middle, heigth_camera,  x_horizon, width, heigth, base_width)
            parallel_group_list.append(parallel_group)
            if showSpline == 1:
                plt.plot(pixels_on_spline[0], pixels_on_spline[1])
                plt.plot(parallel_group[0], parallel_group[1], '.')
    if showSpline == 1:
        plt.plot(transformed_edges[0], transformed_edges[1], ',')
        plt.axis([0,100,-50,50])
        plt.show()
    return parallel_group_list
    
def getCorrectParallelGroup(bw, edges, group1, group2, x_start, x_middle, heigth_camera,  x_horizon, width, heigth, base_width):
    group1l = toAngle(group1, x_start, x_middle, heigth_camera,  x_horizon, width, heigth, base_width)
    group2l = toAngle(group2, x_start, x_middle, heigth_camera,  x_horizon, width, heigth, base_width)
    c1 = 0
    c2 = 0
    for i in  xrange(0, len(group1[0])):
        x_parr_in_px = group1l[0][i]
        y_parr_in_px = group1l[1][i]
        if x_parr_in_px >= heigth or x_parr_in_px < 0 or y_parr_in_px >= width or y_parr_in_px < 0: 
            pass
        else:
            if bw[x_parr_in_px][y_parr_in_px] == 255:
                c1+=1
    for i in xrange(0, len(group2[0])):
        x_parr_out_px = group2l[0][i]
        y_parr_out_px = group2l[1][i]
        if x_parr_out_px >= heigth or x_parr_out_px < 0 or y_parr_out_px >= width or y_parr_out_px < 0:
            pass
        else:
            if bw[x_parr_out_px][y_parr_out_px] == 255:
                c2+=1
    if c2>c1:
        return group2
    else:
        return group1


# chooses a path to follow
# this will become very important in the second semester
def choosePath(parallel_group_list):
    distances = []
    for group in parallel_group_list:
        x1 = group[0][0]
        y1 = group[1][0]
        x2 = group[0][-1]
        y2 = group[1][-1]
        d1 = np.sqrt(x1**2 + y1**2)
        d2 = np.sqrt(x2**2 + y2**2)
        distances.append(d1, d2)
    min_dist = min(distances)
    for i in xrange(0, len(distances)):
        if distances[i] == min_dist:
            min_index = i
            break
    chosen_one = parallel_group_list[min_index/2]
    if min_index%2 == 1:
        chosen_one.reverse()
    return chosen_one

def calculateCurvature(x, y, dx, dy, ddx, ddy):
    return (dx*ddy - ddx*dy)/((dx**2+dy**2)**(3/2))

def calculateSpeeds(path, spline_flatness, future_time):
    tck, u = interpolate.splprep([path[0], path[1]], s=spline_flatness)
    pixels_on_spline = interpolate.splev(u, tck)
    first_derivative = interpolate.splev(u, tck, der=1)
    second_derivative = interpolate.splev(u, tck, der=2)
    time_list = []
    left_motor = []
    right_motor = []
    for i in xrange(0, len(pixels_on_spline[0])-1):
        x = pixels_on_spline[0][i]
        y = pixels_on_spline[1][i]
        x_next = pixels_on_spline[0][i+1]
        y_next = pixels_on_spline[1][i+1]
        dx = first_derivative[0][i]
        dy = first_derivative[1][i]
        ddx = second_derivative[0][i]
        ddy = second_derivative[1][i]
        kappa = calculateCurvature(x, y, dx, dy, ddx, ddy)
        v_c = 9.81/kappa
        
        distance = np.sqrt((y_next-y)**2+(x_next-x)**2)
        delta_time = distance/v_c
        time_list.append(delta_time)
        
        

        
        
        
        
        


    
