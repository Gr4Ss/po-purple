import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import scipy
from scipy import interpolate
from scipy.optimize import fsolve
import random
import time

def createSequence(n):
    list = []
    for i in xrange(0,n):
        list.append(i)
    return list

def addFotos():
    fotoList = []
    #fotoList.append('cam2')
    fotoList.append('cam5')
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
    for k in xrange(0, len(group_list)):
        group = group_list[k]
        new_group = new_group_list[k]
        if not (group[0][0] == new_group[0][0] and group[1][0] == new_group[1][0]):
            new_group[0].insert(0,group[0][0])
            new_group[1].insert(0,group[1][0])
        if not (group[0][-1] == new_group[0][-1] and group[1][-1] == new_group[1][-1]):
            new_group[0].append(group[0][-1])
            new_group[1].append(group[1][-1])
    begins =[[],[]]
    ends =[[],[]]
    for new_group in new_group_list:
        begins[0].append(new_group[0][0])
        begins[1].append(new_group[1][0])
        ends[0].append(new_group[0][-1])
        ends[1].append(new_group[1][-1])
    r = 10
    
    result_group_list = []
    connect = []
    for j in xrange(0, len(begins[0])):
        xb = np.array(begins[0])
        yb = np.array(begins[1])
        xe = np.array(ends[0])
        ye = np.array(ends[1])
        begins_connect = list(np.where(((((xb < begins[0][j]+r) & (xb>begins[0][j]-r))) & (((yb < begins[1][j]+r) & (yb>begins[1][j]-r))))
                            )[0])
        ends_connect = list(np.where(((((xe < ends[0][j]+r) & (xe>ends[0][j]-r))) & (((ye < ends[1][j]+r) & (ye>ends[1][j]-r))))
                                )[0])
        begin_to_ends = list(np.where(((((xe < begins[0][j]+r) & (xe>begins[0][j]-r))) & (((ye < begins[1][j]+r) & (ye>begins[1][j]-r))))
                            )[0])
        end_to_begins = list(np.where(((((xb < ends[0][j]+r) & (xb>ends[0][j]-r))) & (((yb < ends[1][j]+r) & (yb>ends[1][j]-r))))
                                )[0]       )
        elem = [None, None, None, None]            
        if len(begins_connect) >1:
            for l in begins_connect:
                if not l == j :
                    elem[0] = l
        if len(ends_connect) >1:
            for l in ends_connect:
                if not l == j :
                    elem[1] = l
        if len(begin_to_ends) >0:
            for l in begin_to_ends:
                if not l == j :
                    elem[2] = l
        if len(end_to_begins) >0:
            for l in end_to_begins:
                if not l == j :
                    elem[3] = l
        connect.append(elem)
    new_connect = []
    for elem in connect:
        new_elem = [None,None]
        if elem[0] == None:
            new_elem[0] = elem[2]
        else:
            new_elem[0] = elem[0]
        if elem[1] == None:
            new_elem[1] = elem[3]
        else:
            new_elem[1] = elem[1]
        new_connect.append(new_elem)
    connect = new_connect
    start = []
    done_indices = []
    was_end_to_end = 0
    clock_list = []
    for elem in connect:
        clock_list.append(-10)
    result_group_indices_list = []
    while True:

        result_group = []
        curr_index = -1
        for k in xrange(0, len(connect)):
            if k not in done_indices:
                curr_index = k
                break
        if curr_index == -1:
            break
        curr = connect[curr_index]

        prev_index = -1
        if curr[0] == None and curr[1] == None:
            #loops to itself
            result_group_indices = []
            result_group_indices.append(curr_index)
            result_group_indices_list.append(result_group_indices)
            done_indices.append(curr_index)

        else:
            result_group_indices = []
            while True:
                if curr_index in done_indices:
                    break
                curr = connect[curr_index]
                end_to = curr[1]
                begin_to = curr[0]
                if prev_index == -1:
                    clock_list[curr_index] = 1
                    prev_index = curr_index
                    curr_index = end_to
                else:
                    if clock_list[prev_index] == 1:
                        if begin_to == prev_index:
                            clock_list[curr_index] = clock_list[prev_index]
                            prev_index = curr_index
                            curr_index = end_to
                        else:
                            clock_list[curr_index] = (-1)*clock_list[prev_index]
                            prev_index = curr_index
                            curr_index = begin_to
                    else:
                        if end_to == prev_index:
                            clock_list[curr_index] = clock_list[prev_index]
                            prev_index = curr_index
                            curr_index = begin_to
                        else:
                            clock_list[curr_index] = (-1)*clock_list[prev_index]
                            prev_index = curr_index
                            curr_index = end_to                        
                done_indices.append(prev_index)
                result_group_indices.append(prev_index)
            result_group_indices_list.append(result_group_indices)
    for g in result_group_indices_list:
        result_group = [[],[]]
        for index in g:
            if clock_list[index] == -1:
                new_group_list[index][0].reverse()
                new_group_list[index][1].reverse()
            result_group[0] = result_group[0] + new_group_list[index][0]
            result_group[1] = result_group[1] + new_group_list[index][1]
        result_group_list.append(result_group)
 
    return result_group_list
            

# groups pixels logiclly together
def groupPixels2(transformed_edges, large_distance):
    x_array = transformed_edges[0]
    y_array = transformed_edges[1]
    bool_in_group = np.ones(len(transformed_edges[0]), dtype=np.int_)
    group_list = []
    group_index = -1
    
    while True:
        
        if len(np.where(bool_in_group==1)) == 0:
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

def groupPixels3(edges, n):
    x_array = edges[0]
    y_array = edges[1]
    bool_in_group = list(np.ones(len(edges[0]), dtype=np.int_))
    group_list = []
    group_index = -1
    
    while True:
        bool_in_group = np.array(bool_in_group)
        if len(np.where(bool_in_group==1)[0]) == 0:
            break
        group_index += 1
        group = [[],[]]
        ind = np.where(bool_in_group==1)[0][0]

        x = x_array[ind]
        y = y_array[ind]
        group[0].append(x)
        group[1].append(y)
        bool_in_group[ind] = 0
        sides_counter, depth_counter, bool_in_group, return_group, last_index = addBuddies2(ind,
                x_array, y_array, bool_in_group, group, 0, 0, n, False)
        if len(return_group[0]) > 40 :
            group_list.append(return_group)

       
    return group_list


        
def addBuddies2(index, x_array, y_array, bool_in_group, group, sides_counter, depth_counter, n, checkdepth):

    depth_counter += 1
    x = x_array[index]
    y = y_array[index]
    buddy_indices = np.where(
        (((x_array==x-1) | (x_array==x+1)) & ((y_array == y) | ((y_array == y+1) | (y_array == y-1))))
        |
        (((y_array==y-1) | (y_array==y+1)) & (x_array==x)))
    buddy_indices_remainder = []
    for buddy_index in buddy_indices[0]:
        if bool_in_group[buddy_index] == 1 :
            buddy_indices_remainder.append(buddy_index)
    buddy_indices = buddy_indices_remainder 
    if len(buddy_indices) == 0:
        return sides_counter, depth_counter, bool_in_group, group, index
    elif len(buddy_indices) == 1:
        group[0].append(x_array[buddy_indices[0]])
        group[1].append(y_array[buddy_indices[0]])


        sides_counter += 1
        bool_in_group[buddy_indices[0]] = 0
        if checkdepth:
            if sides_counter>n:
                return sides_counter, depth_counter, bool_in_group, group, buddy_indices[0]
        sides_counter, depth_counter, return_bool_in_group, return_group, last_index = addBuddies2(buddy_indices[0],x_array, y_array, bool_in_group, group, sides_counter, depth_counter, n, checkdepth)
        return sides_counter, depth_counter, return_bool_in_group, return_group, last_index

        
    elif (len(buddy_indices) == 2) or (len(buddy_indices) == 2):
        poss = []

        for buddy_index in buddy_indices:
            temp_group = [[],[]]
            temp_bool_in_group = list(bool_in_group)
            temp_group[0] = list(group[0])
            temp_group[1] = list(group[1])
            temp_group[0].append(x_array[buddy_index])
            temp_group[1].append(y_array[buddy_index])
            temp_bool_in_group[buddy_index] = 0            
            pos = addBuddies2(buddy_index, x_array, y_array, temp_bool_in_group,temp_group, sides_counter, depth_counter, n, True)
            poss.append(pos)
        sides_counters = []
        for elem in poss:
            sides_counters.append(elem[0])
        maxsides = max(sides_counters)
        rem_poss = []
        for pos in poss:
            if maxsides == pos[0]:
                rem_poss.append(pos)
        depth_counters = []
        for elem in rem_poss:
            depth_counters.append(elem[1])
        mindepths = min(depth_counters)
        rem_poss2 = []
        for pos in rem_poss:
            if mindepths == pos[1]:
                rem_poss2.append(pos)
        sides_counter, depth_counter, bool_in_group, group, last_index = rem_poss2[0][0],rem_poss2[0][1],rem_poss2[0][2],rem_poss2[0][3],rem_poss2[0][4]
        
        return addBuddies2(last_index, x_array, y_array, bool_in_group, group, sides_counter, depth_counter, n, False)
    else:
        return sides_counter, depth_counter, bool_in_group, group, index 

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
    #edges
    return x*0.02
    #edges2
    #return x*0.0103

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

def drawParallelSplines(bw, edges,group_list, line_width,
            x_start, x_middle,heigth_camera, base_width, x_horizon,
            width, heigth, spline_flatness, showSpline):
    
    
    if showSpline == 1:
            plt.figure()


    remainder_list = []
    parallel_group_list = []
    first_derivative_list = []
    for i in xrange(0, len(group_list)):
        group = group_list[i]
        if len(group[0]) > 4 :
            remainder_list.append(group)
            x_list = group[0]
            y_list = group[1]
            tck, u = interpolate.splprep([x_list, y_list], s=spline_flatness)
            dis_tot = 0
            for m in xrange(0, len(x_list)-1):
                x = x_list[m]
                y = y_list[m]
                x1 = x_list[m+1]
                y1 = y_list[m+1]

                dis_tot += np.sqrt((y1-y)**2+(x1-x)**2)
            spline_step = 1.0/dis_tot
            step = 16
            u = np.arange(0, 1.00, spline_step/step)
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
                y_line_width = line_width
                x_line_width = line_width*2.0/5.0
                x_parr_out = x + ((x_line_width/2.0)*dy)/(np.sqrt(dx**2+dy**2))
                y_parr_out = y - ((y_line_width/2.0)*dx)/(np.sqrt(dx**2+dy**2))
                x_parr_in = x + ((-1)*(x_line_width/2.0)*dy)/(np.sqrt(dx**2+dy**2))
                y_parr_in = y - ((-1)*(y_line_width/2.0)*dx)/(np.sqrt(dx**2+dy**2))
        
                parallel_group_out[0].append(x_parr_out)
                parallel_group_out[1].append(y_parr_out)
                parallel_group_in[0].append(x_parr_in)
                parallel_group_in[1].append(y_parr_in)
            parallel_group = getCorrectParallelGroup(bw, edges, parallel_group_out, parallel_group_in, x_start, x_middle, heigth_camera,  x_horizon, width, heigth, base_width)
            parallel_group_list.append(parallel_group)
            first_derivative_list.append(first_derivative)
            if showSpline == 1:
                plt.plot(pixels_on_spline[0], pixels_on_spline[1])
                plt.plot(parallel_group[0], parallel_group[1], '.')
    if showSpline == 1:
        #plt.axis([0,100,-50,50])
        plt.show()
    return parallel_group_list, first_derivative_list
    
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
        distances.append(d1)
        distances.append(d2)
    min_dist = min(distances)
    for i in xrange(0, len(distances)):
        if distances[i] == min_dist:
            min_index = i
            break
    chosen_one = parallel_group_list[min_index/2]
    if min_index%2 == 1:
        chosen_one[0].reverse()
        chosen_one[1].reverse()
    return chosen_one, min_index/2 


def buildCorrespondenceList(parallel_group_list, path, path_index):
    correspondence_list = []
    for group in parallel_group_list:
        correspondence_list.append((-1)*np.ones_like(group, dtype=int))
    for group_index in xrange(0, len(parallel_group_list)):
        margin = 0.4
#        if not group_index == path_index:
        if True:
            other_group = parallel_group_list[group_index]
            for i in xrange(0, len(path[0])):
                x = path[0][i]
                y = path[1][i]
                other_group = np.array([np.asarray(other_group[0]), np.asarray(other_group[1])])
                x_n = np.where((other_group[0] < x + margin) & (other_group[0] >   x - margin))
                y_n = np.where((other_group[1] < y + margin) & (other_group[1] >   y - margin))
                intersect = np.intersect1d(x_n, y_n)
                if len(intersect)>0:
                    if not group_index == path_index:
                        correspondence_list[path_index][0][i] = group_index
                        correspondence_list[path_index][1][i] = list(intersect).pop(len(intersect)/2)
                    else:
                        new_intersect = []
                        for k in xrange(0, len(intersect)-1):
                            if np.abs(intersect[k] - intersect[k+1]) > 15:
                                new_intersect.append(intersect[k+1])
                        if len(new_intersect)>0:
                            correspondence_list[path_index][0][i] = group_index
                            correspondence_list[path_index][1][i] = list(new_intersect).pop(len(new_intersect)/2)
    return correspondence_list

def detectDeadEnds(parallel_group_list, path, path_index):
    
    loop_list = []
    self_corr_list = buildCorrespondenceList(parallel_group_list, path, path_index)
    start_check_index = 0
    stop_index = 0
    dead_end_indices = []
    start_list = []
    stop_list = []
    while not stop_index == -1:
        start_index, stop_index, is_reversed = getNextStartIndexInGroup(path, path_index, self_corr_list, start_check_index)
        start_check_index = stop_index
        start_list.append(start_index)
        stop_list.append(stop_index)
    for l in xrange(0, len(start_list)):
        if l == len(start_list)-1:
            if (np.abs(stop_list[l] - start_list[0]) < 70) and (np.sqrt((path[0][start_list[l]] - path[0][stop_list[0]])**2 + (path[1][start_list[l]] - path[1][stop_list[0]])**2)) < 2.0:
                dead_end_indices.insert(0,stop_list[0])
                dead_end_indices.insert(0,start_list[0])
        else:
            if (np.abs(stop_list[l] - start_list[l+1]) < 70) and (np.sqrt((path[0][start_list[l]] - path[0][stop_list[l+1]])**2 + (path[1][start_list[l]] - path[1][stop_list[l+1]])**2) < 2.0):
               # dead_end_indices.append(start_list[l+1])
                dead_end_indices.append(stop_list[l])
                dead_end_indices.append(start_list[l+1])
    return dead_end_indices




def buildCorrectPath(parallel_group_list, path, path_index, direction_list, correspondence_list):
    new_path = [[],[]]
    last = 'stop'
    stop_index = -1

    for i in xrange(1, len(correspondence_list[path_index][0])-1):
        x = path[0][i]
        y = path[1][i]
        link = correspondence_list[path_index][0][i]
        link_next = correspondence_list[path_index][0][i+1]
        #print link, link_next, i, path[0][i], path[1][i]
        is_reverse = False
 
        if (not link_next == link and last == 'start') or (i==len(correspondence_list[path_index][0])-2 and not link==-1):

            stop_index = i
            link_index_stop = correspondence_list[path_index][1][i]
            last = 'stop'
        elif (not link_next == link and last == 'stop') or (i==1 and not link==-1):
            last = 'start'
            link_index_start = correspondence_list[path_index][1][i+1]
 
        if last == 'stop' and stop_index == i:
            new_path = [[],[]]
            if link_index_start>link_index_stop:

                is_reverse = True
            if False:
                pass
            else:
                left_path, right_path, linked_group_index, belongs_to = getLeftAndRight(parallel_group_list,
                                correspondence_list, path, path_index, stop_index, x, y, is_reverse)
##                plt.figure()
##                plt.plot(left_path[0], left_path[1], '.')
##                plt.plot(right_path[0], right_path[1], ',')
##                plt.show()
                if direction_list == []:
                    next_direction = ''
                else:
                    next_direction = direction_list.pop(0)
                if next_direction == 'right':
                    if belongs_to == 'right':
                        print 'a'
                        parallel_group_list[linked_group_index] = right_path
                        correspondence_list = buildCorrespondenceList(parallel_group_list, right_path, linked_group_index)
##                        print correspondence_list
##                        plt.figure()
##                        for group in parallel_group_list:
##                            plt.plot(group[0], group[1])
##                            plt.plot(group[0][0], group[1][0], '^')
##                        plt.plot(left_path[0], left_path[1], '.')
##                        plt.plot(left_path[0][0], left_path[1][0], 'p')
##                        plt.show()
                        #rest_of_path = buildCorrectPath(parallel_group_list, right_path, linked_group_index, direction_list, correspondence_list)
                        sta, sto, bla = getNextStartIndexInGroup(right_path, linked_group_index, left_group_correspondence_list, stop_index+2) 
                        rest_of_path = [[],[]]
                        rest_of_path[0] = right_path[0][:sta/2]
                        rest_of_path[1] = right_path[1][:sta/2]
                    else:
                        parallel_group_list[path_index] = right_path
                        correspondence_list = buildCorrespondenceList(parallel_group_list, right_path, path_index)
                        #rest_of_path = buildCorrectPath(parallel_group_list, right_path, path_index, direction_list, correspondence_list)
                        sta, sto, bla = getNextStartIndexInGroup(right_path, path_index, correspondence_list, stop_index+1) 
                        rest_of_path = [[],[]]
                        rest_of_path[0] = right_path[0][0:sta/2]

                        rest_of_path[1] = right_path[1][0:sta/2]
                    new_path[0] = path[0][:stop_index+1] + rest_of_path[0]
                    new_path[1] = path[1][:stop_index+1] + rest_of_path[1]
                    return new_path
                elif next_direction == 'left':
                    if belongs_to == 'left':
                        
                        parallel_group_list[linked_group_index] = left_path
                        correspondence_list = buildCorrespondenceList(parallel_group_list, left_path, linked_group_index)
                        sta, sto, bla = getNextStartIndexInGroup(left_path, linked_group_index, correspondence_list, stop_index+1) 
                        rest_of_path = [[],[]]
                        rest_of_path[0] = left_path[0][0:sta/2]
                        rest_of_path[1] = left_path[1][0:sta/2]        
##                        print correspondence_list
##                        plt.figure()
##                        for group in parallel_group_list:
##                            plt.plot(group[0], group[1])
##                            plt.plot(group[0][0], group[1][0], '^')
##                        plt.plot(left_path[0], left_path[1], '.')
##                        plt.plot(left_path[0][0], left_path[1][0], 'p')
##                        plt.show()
                        #rest_of_path = buildCorrectPath(parallel_group_list, left_path, linked_group_index, direction_list, correspondence_list)
                    else:
                        parallel_group_list[path_index] = left_path
                        correspondence_list = buildCorrespondenceList(parallel_group_list, left_path, path_index)
                        sta, sto, bla = getNextStartIndexInGroup(left_path, path_index, correspondence_list, stop_index+1) 
                        rest_of_path = [[],[]]
                        rest_of_path[0] = left_path[0][0:sta/2]
                        rest_of_path[1] = left_path[1][0:sta/2]
                        #rest_of_path = buildCorrectPath(parallel_group_list, left_path, path_index, direction_list, correspondence_list)
                    new_path[0] = path[0][:stop_index+1] + rest_of_path[0]
                    new_path[1] = path[1][:stop_index+1] + rest_of_path[1]
                    return new_path
                elif next_direction == 'straight':
                    if belongs_to == 'right':
                        left_group_index = path_index
                        right_group_index = linked_group_index
                        left_group_correspondence_list = correspondence_list
                        right_group_correspondence_list = buildCorrespondenceList(parallel_group_list, right_path, right_group_index)
                        start_check_index = correspondence_list[path_index][1][stop_index]
                        if is_reverse:
                           start_check_index = len(parallel_group_list[left_group_index]) - start_check_index                        
                        left_start_index, left_stop_index, left_reverse_state = getNextStartIndexInGroup(left_path, left_group_index, left_group_correspondence_list, stop_index)
                        right_start_index, right_stop_index, right_reverse_state = getNextStartIndexInGroup(right_path, right_group_index, right_group_correspondence_list, start_check_index)
                    else:
                        right_group_index = path_index
                        left_group_index = linked_group_index
                        right_group_correspondence_list = correspondence_list
                        left_group_correspondence_list = buildCorrespondenceList(parallel_group_list, left_path, left_group_index)
                        start_check_index = correspondence_list[path_index][1][stop_index]
                        if is_reverse:
                           start_check_index = len(parallel_group_list[left_group_index]) - start_check_index
                        left_start_index, left_stop_index, left_reverse_state = getNextStartIndexInGroup(left_path, left_group_index, left_group_correspondence_list, start_check_index)
                        right_start_index, right_stop_index, right_reverse_state = getNextStartIndexInGroup(right_path, right_group_index, right_group_correspondence_list, stop_index)
                    if left_start_index == -1 or right_start_index == -1:
                        print 'trying to drive straight in normal Y split or crossroads not fully visible'
                        new_path[0] = path[0][:stop_index+1]
                        new_path[1] = path[1][:stop_index+1]
                        return new_path
                    else:
                        link_left = left_group_correspondence_list[left_group_index][0][left_start_index]
                        link_right = right_group_correspondence_list[right_group_index][0][right_start_index]
                        link_left_index = left_group_correspondence_list[left_group_index][1][left_start_index]
                        link_right_index = right_group_correspondence_list[right_group_index][1][right_start_index]
                        left_of_right_path = [[],[]]
                        right_of_left_path = [[],[]]
                        if left_reverse_state:
                            right_of_left_path[0] = parallel_group_list[link_left][0][link_left_index:]
                            right_of_left_path[1] = parallel_group_list[link_left][1][link_left_index:]
                        else:
                            right_of_left_path[0] = parallel_group_list[link_left][0][:link_left_index]
                            right_of_left_path[1] = parallel_group_list[link_left][1][:link_left_index]
                            right_of_left_path[0].reverse()
                            right_of_left_path[1].reverse()
                        if right_reverse_state:
                            left_of_right_path[0] = parallel_group_list[link_right][0][link_right_index:]
                            left_of_right_path[1] = parallel_group_list[link_right][1][link_right_index:]
                        else:
                            left_of_right_path[0] = parallel_group_list[link_right][0][:link_right_index]
                            left_of_right_path[1] = parallel_group_list[link_right][1][:link_right_index]
                            left_of_right_path[0].reverse()
                            left_of_right_path[1].reverse()
                        left_of_right_correspondence_list = buildCorrespondenceList([left_of_right_path,right_of_left_path], left_of_right_path, 0)
                        left_of_right_start_index, left_of_right_stop_index, left_of_right_reverse_state = getNextStartIndexInGroup(left_of_right_path, 0, left_of_right_correspondence_list, 0)

                        
                        if left_of_right_start_index == -1:
                            print 'trying to drive straight in normal Y split or crossroads not fully visible'
                            new_path[0] = path[0][:stop_index+1]
                            new_path[1] = path[1][:stop_index+1]
                            return new_path
                        else:
                            left_of_right_path[0] = left_of_right_path[0][left_of_right_start_index:]
                            left_of_right_path[1] = left_of_right_path[1][left_of_right_start_index:]
                            parallel_group_list[link_right] = left_of_right_path
                            correspondence_list = buildCorrespondenceList(parallel_group_list, left_of_right_path, link_right)
                            #rest_of_path = buildCorrectPath(parallel_group_list, left_of_right_path, link_right, direction_list, correspondence_list)
                            sta, sto, bla = getNextStartIndexInGroup(left_of_right_path, left_of_right_start_index, left_group_correspondence_list, stop_index+1) 
                            rest_of_path = [[],[]]
                            rest_of_path[0] = left_of_right_path[0][0:sta/2]
                            rest_of_path[1] = left_of_right_path[1][0:sta/2]
                            new_path[0] = path[0][:stop_index+1] + rest_of_path[0]
                            new_path[1] = path[1][:stop_index+1] + rest_of_path[1]
                            return new_path
                else:
                    new_path[0] = path[0][:stop_index]
                    new_path[1] = path[1][:stop_index]
                    return new_path
    new_path[0] = path[0][:stop_index]
    new_path[1] = path[1][:stop_index]
    return new_path
                        
def getNextStartIndexInGroup(path, path_index, correspondence_list, start_check_index):
    last = 'stop'
    stop_index = -1
    is_reversed = False
    for i in xrange(start_check_index+1, len(correspondence_list[path_index][0])-1):
        link = correspondence_list[path_index][0][i]
        link_next = correspondence_list[path_index][0][i+1]
        if (not link_next == link and last == 'start') or (i==len(correspondence_list[path_index][0])-2 and not link==-1):
            stop_index = i
            link_index_stop = correspondence_list[path_index][1][i]
            last = 'stop'
        elif (not link_next == link and last == 'stop') or (i==start_check_index+1 and not link==-1):
            last = 'start'
            start_index = i
            link_index_start = correspondence_list[path_index][1][i+1]
        if last == 'stop' and stop_index == i:
            if link_index_start>link_index_stop:
                is_reversed = True
            return start_index+1, stop_index, is_reversed

    return -1,-1,-1

                
def getLeftAndRight(parallel_group_list, correspondence_list, path, path_index, stop_index, x, y, is_reverse):        

    theta_stop = np.arctan((path[1][stop_index]-path[1][stop_index-1])/(path[0][stop_index]-path[0][stop_index-1]))
    if (path[0][stop_index]-path[0][stop_index-1]) < 0:
        if (path[1][stop_index]-path[1][stop_index-1]) >= 0 :
            theta_stop+=np.pi
        else:
            theta_stop+=(-1)*np.pi
    theta_stop = (np.pi/2-theta_stop)
    comparison_pixel_index_on_path = min(len(path[0])-1, stop_index + 10)
    x = path[0][comparison_pixel_index_on_path]
    y = path[1][comparison_pixel_index_on_path]
    linked_group_index = correspondence_list[path_index][0][stop_index]
    pixel_index_on_link = correspondence_list[path_index][1][stop_index]
    linked_group = parallel_group_list[linked_group_index]
    if not pixel_index_on_link == len(linked_group[0])-1:
        if not is_reverse:
            comparison_pixel_index_on_link = min(len(linked_group[0])-1,pixel_index_on_link+5)
        else:
            comparison_pixel_index_on_link = max(0,pixel_index_on_link - 5)                        
        x_link = linked_group[0][comparison_pixel_index_on_link]
        y_link = linked_group[1][comparison_pixel_index_on_link]
        x_link_rot = np.cos(theta_stop)*x_link - np.sin(theta_stop)*y_link
        x_rot = np.cos(theta_stop)*x - np.sin(theta_stop)*y
        left_path = [[],[]]
        right_path = [[],[]]
        if x_rot < x_link_rot:
            left_path[0] = path[0][stop_index+1:]
            left_path[1] = path[1][stop_index+1:]
            belongs_to = 'right'
            if is_reverse:
                right_path[0] = linked_group[0][:pixel_index_on_link]
                right_path[1] = linked_group[1][:pixel_index_on_link]   
            else:
                right_path[0] = linked_group[0][pixel_index_on_link:]
                right_path[1] = linked_group[1][pixel_index_on_link:]
                right_path[0].reverse()
                right_path[1].reverse()
        else:
            right_path[0] = path[0][stop_index+1:]
            right_path[1] = path[1][stop_index+1:]
            belongs_to = 'left'  
            if is_reverse:
                left_path[0] = linked_group[0][:pixel_index_on_link]
                left_path[1] = linked_group[1][:pixel_index_on_link]
                left_path[0].reverse()
                left_path[1].reverse()
            else:
                left_path[0] = linked_group[0][pixel_index_on_link+1:]
                left_path[1] = linked_group[1][pixel_index_on_link+1:]
    else:
        # end of linked group
        return [[],[]], [[],[]] , -1, 'left'                
##    plt.figure()
##    plt.plot(left_path[0], left_path[1], '.')
##    plt.plot(left_path[0][0], left_path[1][0], 'p')
##    plt.plot(right_path[0], right_path[1], ',')
##    plt.plot(right_path[0][0], right_path[1][0], '')
##    plt.plot(path[0][stop_index], path[1][stop_index], '^')
##    plt.plot(linked_group[0][0], linked_group[1][0], '*')
##    plt.plot(path[0][0], path[1][0], '')
##    plt.plot(linked_group[0][pixel_index_on_link], linked_group[1][pixel_index_on_link], '^')
##    plt.show()

    if not (left_path == [[],[]] and right_path == [[],[]]):
        return left_path, right_path, linked_group_index, belongs_to
    else:
        raise AssertionError

def recognizeCurrentPath(previous_path, parallel_group_list,
                         current_position, position_difference):
    disx = position_difference[0]
    disy = position_difference[1]
    theta = position_difference[2]
    for group in parallel_group_list:
        real_world_group = [[],[]]
        for i in xrange(0, len(group[0])):
            x = group[0][i]
            y = group[1][i]
            x_real = (x - disx)*np.cos(theta) - (y - disy)*np.sin(theta)
            y_real = (x - disx)*np.sin(theta) + (y - disy)*np.cos(theta)
            real_world_group[0].append(x_real)
            real_world_group[1].append(y_real)
        for i in xrange(0, len(previous_path[0])):
            x = previous_path[0][i]
            y = previous_path[1][i]
         
    
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

def detectEdges(bw):
    x_list, y_list = np.where(bw == 255)
    x_list_hhw = []
    y_list_hhw = []
    x_rem = []
    y_rem = []
    for i in xrange(0, len(x_list)):
        x = x_list[i]
        y = y_list[i]
        if i == 0:
            if not (y == 0 and x ==0):
                if not checkIfDouble(x, y, x_rem, y_rem):
                   x_rem.append(x)
                   y_rem.append(y)                      
        elif i == len(x_list)-1:
            if not (y == len(bw[0])-1 and x == len(bw)-1):
                if not checkIfDouble(x, y, x_rem, y_rem):
                    x_rem.append(x)
                    y_rem.append(y)        
        else:
            if y%(len(bw[0])) + 1 == len(bw[0]):

##                if x_list[i-1] == x and y - 1 == y_list[i-1]:
##                    x_list_hhw.append(x)
##                    y_list_hhw.append(y)
##                else:
##                    x_rem.append(x)
##                    y_rem.append(y)
                if not checkIfDouble(x, y, x_rem, y_rem):
                    x_rem.append(x)
                    y_rem.append(y)
            elif y%(len(bw[0])) == 0:
##                if x == x_list[i+1] and  y + 1 == y_list[i+1]:
##                    x_list_hhw.append(x)
##                    y_list_hhw.append(y)
##                else:
##                    x_rem.append(x)
##                    y_rem.append(y)
                if not checkIfDouble(x, y, x_rem, y_rem):
                    x_rem.append(x)
                    y_rem.append(y)
            else:
                if x_list[i-1] == x and x == x_list[i+1] and y + 1 == y_list[i+1] and y - 1 == y_list[i-1]:
                    x_list_hhw.append(x)
                    y_list_hhw.append(y)
                else:
                    if not checkIfDouble(x, y, x_rem, y_rem):
                        x_rem.append(x)
                        y_rem.append(y)
    x_list2 = [x for (y,x) in sorted(zip(y_list,x_list))]
    y_list2 = sorted(y_list)
    for i in xrange(0, len(y_list2)):
        x = x_list2[i]
        y = y_list2[i]
        if i == 0:
            if not (y == 0 and x ==0):
                if not checkIfDouble(x, y, x_rem, y_rem):
                    x_rem.append(x)
                    y_rem.append(y)                       
        elif i == len(x_list)-1:
            if not (y == len(bw[0])-1 and x == len(bw)-1):
                if not checkIfDouble(x, y, x_rem, y_rem):
                    x_rem.append(x)
                    y_rem.append(y)        
        else:
            if y%(len(bw[0])) + 1 == len(bw[0]):

##                if y_list2[i-1] == y and x - 1 == x_list2[i-1]:
##                    x_list_hhw.append(x)
##                    y_list_hhw.append(y)
##                else:
##                    x_rem.append(x)
##                    y_rem.append(y)
                if not checkIfDouble(x, y, x_rem, y_rem):
                    x_rem.append(x)
                    y_rem.append(y)
            elif y%(len(bw[0])) == 0:
##                if y == y_list2[i+1] and  x + 1 == x_list2[i+1]:
##                    x_list_hhw.append(x)
##                    y_list_hhw.append(y)
##                else:
##                    x_rem.append(x)
##                    y_rem.append(y)
                x_rem.append(x)
                y_rem.append(y)
            else:
                if y_list2[i-1] == y and y == y_list2[i+1] and x + 1 == x_list2[i+1] and x - 1 == x_list2[i-1]:
                    x_list_hhw.append(x)
                    y_list_hhw.append(y)
                else:
                    if not checkIfDouble(x, y, x_rem, y_rem):
                        x_rem.append(x)
                        y_rem.append(y)

    return x_rem, y_rem

def checkIfDouble(x, y, x_array, y_array):
    x_array = np.array(x_array)
    y_array = np.array(y_array)
    double_ind = np.where((x_array == x) & (y_array == y))
    
    double_ind = list(double_ind[0])
    if len(double_ind)>0:
        return True
    else:
        return False
#bw = np.array([np.array([0,255,255,255,255,0]),np.array([0,255,255,255,255,0]),np.array([0,255,255,255,255,255]),np.array([0,255,255,255,255,255]),np.array([0,255,255,255,255,255]),np.array([0,255,255,255,255,255]),np.array([0,255,255,255,255,255])])
#edges3 = detectEdges(bw)

#group_list = groupPixels3(edges3, 2)
##plt.figure()
##for group in group_list:
##    plt.plot(group[0], group[1], '.')
##plt.show()

def transformPathToMotorPaths(parallel_group_list,path, camera_to_axis, wheel_distance, spline_flatness):
    path[0].insert(0,0)
    path[1].insert(0,0)
    if len(path[0])<4:
        pixels_on_spline = [path[0][0], path[0][-1]],[path[1][-1],path[1][-1]]
        drx = path[0][-1]-path[0][0]
        dry = path[1][-1]-path[1][0]
        first_derivative = [[drx, drx],[dry, dry]]
    else:
        tot_dis = 0
        for k in xrange(0, len(path[0])):
            x = path[0][k]
            y = path[1][k]
            x0 = path[0][k-1]
            y0 = path[1][k-1]
            tot_dis += np.sqrt((y-y0)**2+(x-x0)**2)
        tck, u = interpolate.splprep([path[0], path[1]], s=spline_flatness)
        unew = np.arange(0, 1.00,1.0/tot_dis)
        pixels_on_spline = interpolate.splev(unew, tck)
        first_derivative = interpolate.splev(unew, tck, der=1)
        second_derivative = interpolate.splev(unew, tck, der = 2)
    left_motor = [[],[]]
    right_motor = [[],[]]
    curv_list = []
    left_dis_list = []
    right_dis_list = []
    for i in xrange(0, len(pixels_on_spline[0])):
        x = pixels_on_spline[0][i]
        y = pixels_on_spline[1][i]
        dx = first_derivative[0][i]
        dy = first_derivative[1][i]
        ddx = second_derivative[0][i]
        ddy = second_derivative[1][i]
        x_parr_out = x + ((wheel_distance/2.0)*dy)/(np.sqrt(dx**2+dy**2)) + camera_to_axis
        y_parr_out = y - ((wheel_distance/2.0)*dx)/(np.sqrt(dx**2+dy**2)) 
        x_parr_in = x + ((-1)*(wheel_distance/2.0)*dy)/(np.sqrt(dx**2+dy**2)) + camera_to_axis
        y_parr_in = y - ((-1)*(wheel_distance/2.0)*dx)/(np.sqrt(dx**2+dy**2)) 
        left_motor[0].append(x_parr_in)
        left_motor[1].append(y_parr_in)
        right_motor[0].append(x_parr_out)
        right_motor[1].append(y_parr_out)
        curv_list.append(calculateCurvature(x,y,dx,dy,ddx,ddy))

    
    for k in xrange(0, len(left_motor[0])):
        if 1.00/curv_list[i] < wheel_distance/2.00:
            
            if k == 0:
                
                left_dis_list.append((-1)*np.sqrt((left_motor[0][k] - 0)**2 + (left_motor[1][k] - 0)**2))
            else:
                left_dis_list.append((-1)*
                    np.sqrt(
                        (left_motor[0][k] - left_motor[0][k-1])**2 + (left_motor[1][k] - left_motor[1][k-1])**2
                        )
                    )
        else:
            if k == 0:
                left_dis_list.append(np.sqrt((left_motor[0][k] - 0)**2 + (left_motor[1][k] - 0)**2))
            else:
                left_dis_list.append(np.sqrt((left_motor[0][k] - left_motor[0][k-1])**2 + (left_motor[1][k] - left_motor[1][k-1])**2))
            
    for k in xrange(0, len(right_motor[0])):
        if 1.00/curv_list[i] < wheel_distance/2.00:
            if k == 0:
                right_dis_list.append((-1)*np.sqrt((right_motor[0][k] - 0)**2 + (right_motor[1][k] - 0)**2))
            else:
                right_dis_list.append((-1)*np.sqrt((right_motor[0][k] - right_motor[0][k-1])**2 + (right_motor[1][k] - right_motor[1][k-1])**2))
        else:
            if k == 0:
                right_dis_list.append(np.sqrt((right_motor[0][k] - 0)**2 + (right_motor_list[1][k] - 0)**2))
            else:
                right_dis_list.append(np.sqrt((right_motor[0][k] - right_motor[0][k-1])**2 + (right_motor[1][k] - right_motor[1][k-1])**2))

    return left_dis_list, right_dis_list
    
    
