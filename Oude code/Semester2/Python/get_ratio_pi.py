import numpy as np
import Image_1 as im
import Image



def get_ratio(img,
              x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
              last_ratio,
              column_factor, row_factor,
              correction):
    image = im.load_image(str(img))
    height = len(image)
    width = len(image[0])
    intersections = convert_to_pairs(image, height, width, column_factor, row_factor)
    print intersection
    for intersection in intersections:
        new_intersection = []
        if is_odd(len(intersection)):
            return last_ratio
    left_white_lines = []
    for i in xrange(0,len(intersections[0])/2):
        new_point = (intersections[0][2*i], intersections[0][2*i+1])
        left_white_lines.append(new_point)
    top_white_lines = []
    for i in xrange(len(intersections[2])/2):
        new_point = (intersections[2][2*i], intersections[2][2*i+1])
        top_white_lines.append(new_point)
    right_white_lines = []
    for i in xrange(len(intersections[1])/2):
        new_point = (intersections[1][-2*i-1], intersections[1][-2*i])
        right_white_lines.append(new_point)
    bottom_white_lines = []
    for i in xrange(0,len(intersections[3])/2):
        new_point = (intersections[3][-2*i-1], intersections[3][-2*i])
        bottom_white_lines.append(new_point)
    # + top_white_lines
    white_lines = left_white_lines  + right_white_lines + bottom_white_lines
    destination = choose_path(white_lines)


    x_right = destination[0][0]
    y_right = destination[0][1]
    x_left = destination[1][0]
    y_left = destination[1][1]

    left_distance = np.sqrt((x_left - x_wheel_left)**2 + (y_left - y_wheel_left)**2)
    right_distance= np.sqrt((x_right - x_wheel_right)**2 + (y_right - y_wheel_right)**2)
    ratio = right_distance/left_distance
    last_ratio = correction*ratio
    #print 'Ratio:  ' + str(correction*ratio)
    return correction*ratio

def is_odd(number):
    return number%2 == 1

def convert_to_pairs(image, height, width, column_factor, row_factor):
    # left column is the column with the lowest x coordinate
    left_column = int(width*column_factor)
    right_column = width - left_column
    # bottom row is the one with the lowest y coordinate
    bottom_row = int(height*row_factor)
    top_row = height - bottom_row
    left_column_intersections = im.fast_check_column(left_column, image, bottom_row, top_row)
    print left_column_intersections
    right_column_intersections = im.fast_check_column(right_column, image, bottom_row, top_row)
    print right_column_intersections
    top_row_intersections = im.fast_check_row(top_row, image, left_column, right_column)
    bottom_row_intersections = im.fast_check_row(bottom_row, image,  left_column, right_column)
    return (left_column_intersections, right_column_intersections, top_row_intersections, bottom_row_intersections)

def is_redundant_point(tuple1, tuple2):
    return (fuzzyequal (tuple1[0], tuple2[0], group_factor) or fuzzyequal (tuple1[1], tuple2[1], group_factor))

def fuzzyequal(x, y, epsilon):
    return (abs(x-y) < epsilon)

def choose_path(white_lines):
    return white_lines[0]
