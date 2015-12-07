import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import interpolate
import time
import FollowLine7 as fl
import urllib

showLightingPlot = 0
showBlackAndWhite = 0
showPlot = 0
showBirdsEye = 0
showSpline = 0
showScDer = 0
showTimes = 0
showPath = 0
cutPicture = 1
showTotal = 0

# add fotolins
fotoList = fl.addFotos()

# PARAMETERS

# Lighting parameters
interval = 2
interval2 = 1

# Canny parameters
threshold2 = 100
threshold1 = 50

# Grouping parameters
maxRange = 0.5
large_distance = 1.7

# Transformations
x_start = 5.4          # [cm]
x_middle = 10.9        # [cm]
x_horizon = -13        # [pixels]
heigth_camera = 3.5    # [cm]
base_width = 6.7       # [cm]
line_width = 1.7       # [cm]


heigth = 208
if cutPicture == 1:
    cut_x = 40
    x_middle_new_px = (heigth - cut_x)/2 + cut_x
    x_middle = fl.XToBirdsEye(float(x_middle_new_px),
                                  x_start, x_middle, heigth_camera, heigth)
    x_horizon = x_horizon - cut_x
    
  # Linking parameter
spline_flatness = 1.7



total_time = 0
current_path = []
current_position = [0.0,0.0,0.0]

direction_list = ['left','left','right']
o=0 
while o < 10:
    o+=1
#__________________________________________________START_____________________________________________

# download picture + timestamp or somethinig to determine the current position.
# GET: position_difference
# GET: picture/foto
    

    start = time.time()
    # foto = urllib.urlretrieve("http://192.168.137.156/cam.jpg", "azertyuiop.jpg")
    # color_image = Image.open(foto[0])
    color_image = Image.open('TEST3.jpg')
    (width, heigth) = color_image.size
# convert to grayscale
    gray_values = fl.toGrayScale(color_image)
    gray = gray_values[0]
    gray_image = gray_values[1]
    toGray = time.time()
    
# calculate tippingValue
    tippingValue = fl.calculateTippingValue(gray_image, width, heigth,
                                            interval, interval2, showLightingPlot)
    tippingValue = 120
# convert to absolute black and white
    bw = fl.toBlackAndWhite(gray, tippingValue, showBlackAndWhite)
    toBlackAndWhite = time.time()

# cut top part of picture
    if cutPicture ==1:
        bw = bw[cut_x:heigth]
        heigth = len(bw)

# Canny edge detection
    edges = cv2.Canny(bw, threshold1, threshold2)
    if showPlot == 1:
        p = np.nonzero(edges)
        fl.plot2(p, width, heigth)
    Canny = time.time()
    edges2 = fl.detectEdges(bw)
    
    group_list2 = fl.groupPixels3(edges2, 10)


# transform to a birds eye view
    # transformed_edges = fl.toBirdsEye(np.nonzero(edges), x_start,
    #                                  x_middle, heigth_camera ,x_horizon,
    #                                  base_width, width,heigth)
    #if showBirdsEye == 1:
    #    fl.plot3(transformed_edges)
    transform = time.time()

# roughly group pixels together in logical groups
    #group_list = fl.groupPixels2(transformed_edges, large_distance)
   
    group = time.time()
    group_list2 = fl.thinGroups(group_list2, 5)
    new_group_list = []
    for group in group_list2:
        new_group = fl.toBirdsEye(group, x_start,
                                      x_middle, heigth_camera ,x_horizon,
                                      base_width, width,heigth)
        new_group_list.append(new_group)
    group_list = new_group_list
    
# link groups
    parallel_group_list, first_derivative_list = fl.drawParallelSplines(bw, edges2, group_list, line_width,
            x_start, x_middle,heigth_camera, base_width, x_horizon,
            width, heigth, spline_flatness, showSpline)
    dead_end_list = []
    self_link = []
    for par_group in parallel_group_list:
        dead_end_list.append(fl.detectDeadEnds([par_group],par_group, 0))
    new_parallel_group_list = []
    for k in xrange(0, len(parallel_group_list)):

        par_group = parallel_group_list[k]
        dead_end = dead_end_list[k]
        if dead_end == [-1,-1]:
            self_link.append(k)
            new_parallel_group_list.append(par_group)
        else:
            p = 0
            while p < len(dead_end):
                a=dead_end[p]
                b=dead_end[p-1]
                new_group = [[],[]]
                new_group[0] = par_group[0][b:a]
                new_group[1] = par_group[1][b:a]
                if not len(new_group[0]) < 4:
                    new_parallel_group_list.append(new_group)
                p+= 2
            new_group = [[],[]]
            new_group[0] = par_group[0][dead_end[-1]:]
            new_group[1] = par_group[1][dead_end[-1]:]
            if not len(new_group[0]) < 4:
                new_parallel_group_list.append(new_group)
    link = time.time()
    parallel_group_list = new_parallel_group_list

# choose path
    first_path, first_path_index = fl.choosePath(parallel_group_list)
    correspondence_list = fl.buildCorrespondenceList(parallel_group_list,
                first_path, first_path_index)
    correct_path = fl.buildCorrectPath(parallel_group_list,
                first_path, first_path_index, direction_list, correspondence_list)
    if showPath == 1:
        plt.figure()
        plt.plot(correct_path[0], correct_path[1], 'p')
        plt.plot(correct_path[0][0], correct_path[1][0], '^')
        plt.plot(correct_path[0][-1], correct_path[1][-1], '^')
        for group in parallel_group_list:
            plt.plot(group[0], group[1], ',')
        plt.show()
    left_dis_list, right_dis_list = fl.transformPathToMotorPaths(parallel_group_list, correct_path,0.0,13.5, spline_flatness)


    if showTotal == 1:
        plt.figure()
##        plt.plot(correct_path[0], correct_path[1], 'p')
##        plt.plot(correct_path[0][0], correct_path[1][0], '^')
##        plt.plot(correct_path[0][-1], correct_path[1][-1], '^')

        for group in parallel_group_list:
            plt.plot(group[0], group[1])
        for group in group_list:
            plt.plot(group[0], group[1], ',')
        #plt.ion()
        plt.show()

        
#____________________________________________________________END__________________________________________


# print everything
    end = time.time()
    total_time += (end - start)
    if showTimes == 1:
        
        print 'times:  '
        print 'to grayscale:        ' + str(toGray - start)
        print 'to black and white:  ' + str(toBlackAndWhite - toGray)
        print 'edge detection:      ' + str(Canny - toBlackAndWhite)
        print 'transform to bird:   ' + str(transform - Canny)
        print 'grouping:            ' + str(group - transform)
        print 'linking:             ' + str(link - group)
        print 'total time:          ' + str(end - start)
        
    

