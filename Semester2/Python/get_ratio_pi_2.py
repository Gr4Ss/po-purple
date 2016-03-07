from numpy import sqrt
import Image_1 as im

def merge_pairs(array):
    assert(not is_odd(len(array)))
    return_array = []
    for i in xrange(len(array)/2):
        new_point = ( int((array[-2*i-1][0] + array[-2*i][0])/2.0), int((array[-2*i-1][1] + array[-2*i][1])/2.0) )
        return_array.append(new_point)
    return return_array

def get_ratio(image,
              x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
              last_ratio,
              column_factor, row_factor,
<<<<<<< HEAD
              correction, a):

=======
              correction):
    
>>>>>>> 0b37317a76df2d299514577ac4dfb62b7bd53fca
    intersections = convert_to_pairs(image, height, width, column_factor, row_factor)


    
    lengths = []
    intersection_points = []
    alt = 0
    for intersection in intersections:
        lengths.append(len(intersection))
    nb_of_odds = 0
    nb_of_non_zero_evens = 0

    [print len(intersect) for intersect in intersections]

    for ln in lengths:
        if is_odd(ln):
            nb_of_odds += 1
        elif ln == 0:
            pass
        else:
            nb_of_non_zero_evens += 1
    if nb_of_odds > 1:
        alt = 1
    for intersection in intersections:
        if not is_odd(len(intersection)):
            white_line_points = merge_pairs(intersection)
            intersection_points.append(white_line_points)
        else:
            if len(intersection) == 1:
                if nb_of_non_zero_evens > 0:
                    intersection_points.append([])
                else:
                    intersection_points.append(intersection)
            else:
                # CHOICE
                # a) ignore odd number of points greater than 3
                # intersection_points.append([])
                # b) throw foto away
                # c) alternative
                alt = 1


    if alt == 0:
        white_lines = intersection_points[0] + intersection_points[1] + intersection_points[2]
        ## + intersection_points[3] # if top_row_intersections is needed
        destination = choose_path(white_lines)
    else:
        destination = alternative(intersections, width)
    x_des = destination[0]
    y_des = destination[1]
    left_distance = sqrt((x_des - x_wheel_left)**2 + (y_des - y_wheel_left)**2)
    right_distance= sqrt((x_des - x_wheel_right)**2 + (y_des - y_wheel_right)**2)
    ratio = right_distance/left_distance
    last_ratio = correction*ratio
    return correction*ratio

def alternative(intersections, width):
    nb_left = len(intersections[0])
    nb_right = len(intersections[2])
    if nb_right<nb_left and not nb_left == nb_right:
        destination = (2,2)
        return destination
    else:
        destination = (width-2,2)
        return destination
    for elem in intersections[1]:
        if elem[0] < width/2:
            nb_left += 1
        else:
            nb_right += 1
    if nb_right<nb_left:
        destination = (2,2)
        return destination
    else:
        destination = (width-2,2)
        return destination

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
    right_column_intersections = im.fast_check_column(right_column, image, bottom_row, top_row)
    ##top_row_intersections = im.fast_check_row(top_row, image, left_column, right_column)
    bottom_row_intersections = im.fast_check_row(bottom_row, image,  left_column, right_column)
    return (left_column_intersections, bottom_row_intersections, right_column_intersections, # top_row_intersections,
    )

def choose_path(white_lines):
    return white_lines[0]
