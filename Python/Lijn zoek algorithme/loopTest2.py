import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import interpolate
import time
import FollowLine5 as fl


showLightingPlot = 0
showBlackAndWhite = 0
showPlot = 1
showGroups = 0
showBirdsEye = 0
showSpline = 1
showScDer = 0
showTimes = 1
cutPicture = 1

# add fotolins
fotoList = fl.addFotos()

# PARAMETERS

# Lighting parameters
interval = 8
interval2 = 2

# Canny parameters
threshold2 = 100
threshold1 = 50

# Grouping parameters
maxRange = 0.2
large_distance = 1.0

# Transformations
x_start = 5.5         # [cm]
x_middle = 12.4       # [cm]
x_horizon = -5        # [pixels]
heigth_camera = 4.4   # [cm]
base_width = 6.2      # [cm]
#line_width = 1.9      # [cm]
line_width = 2.3/2.0

heigth = 480
if cutPicture == 1:
    cut_x = heigth*0.01
    x_middle_new_px = (heigth - cut_x)/2 + cut_x
    x_middle = fl.XToBirdsEye(float(x_middle_new_px),
                                  x_start, x_middle, heigth_camera, heigth)
    x_horizon = x_horizon - cut_x
    
# Linking parameter
spline_flatness = 0.5



total_time = 0
for foto in fotoList:

#__________________________________________________START_____________________________________________

    print " "
    print str(foto) + ':   '
    start = time.time()
    
    color_image = Image.open(foto+'.jpg')
    (width, heigth) = color_image.size
    print width
    print heigth
# convert to grayscale
    gray_values = fl.toGrayScale(color_image)
    gray = gray_values[0]
    gray_image = gray_values[1]
    toGray = time.time()
    
# calculate tippingValue
    tippingValue = fl.calculateTippingValue(gray_image, width, heigth,
                                            interval, interval2, showLightingPlot)
    
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
        print p
        fl.plot2(p, width, heigth)
    Canny = time.time()

# transform to a birds eye view
    transformed_edges = fl.toBirdsEye(np.nonzero(edges), x_start,
                                      x_middle, heigth_camera ,x_horizon,
                                      base_width, width,heigth)
    if showBirdsEye ==1:
        fl.plot3(transformed_edges)
    transform = time.time()
    
# roughly group pixels together in logical groups
    group_list = fl.groupPixels2(transformed_edges, large_distance)
    group_list = fl.thinGroups(group_list, 5)
    
    if showGroups == 1:
        plt.figure()
        for group in group_list:
            plt.plot(group[0], group[1], ".")
        plt.show()
    group = time.time()
    
        
# link groups
    fl.linkGroups2(bw, edges, group_list, line_width,
            x_start, x_middle,heigth_camera, base_width, x_horizon,
            width, heigth, spline_flatness, showSpline, transformed_edges)
    link = time.time()

    
#____________________________________________________________END__________________________________________


# print everything
    end = time.time()
    print 'Done in ' + str(end - start)
    total_time += (end - start)
    img = cv2.imread(foto+'.jpg')
    if showTimes == 1:
        
        print 'times:  '
        print 'to grayscale:        ' + str(toGray - start)
        print 'to black and white:  ' + str(toBlackAndWhite - toGray)
        print 'edge detection:      ' + str(Canny - toBlackAndWhite)
        print 'transform to bird:   ' + str(transform - Canny)
        print 'grouping:            ' + str(group - transform)
        print 'linking:             ' + str(link - group)
        print 'total time:          ' + str(end - start)
    
print str(total_time) + ' sec needed for ' + str(len(fotoList)) + ' pictures'

