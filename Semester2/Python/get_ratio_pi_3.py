from numpy import sqrt
import Image_1 as im

def cog_x(points):
    cog_x = 0
    for point in points:
        cog_x += point[0]
    cog_x = cog_x/len(points)
    return (cog_x, points[0][1])

def cog_y(points):
    cog_y = 0
    for point in points:
        cog_y += point[1]
    cog_y = cog_y/len(points)
    return (points[0][0], cog_y)

def add_to_queue(queue, ratio):
    len_queue = 20
    queue.insert(0, ratio)
    if len(queue) > len_queue:
        queue.pop()
    return queue

def get_ratio(image,
              x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
              last_ratio,
              column_factor, row_factor,
              ratio_queue, layout_queue, direction_list):

    intersections = convert_to_pairs(image, height, width, column_factor, row_factor)
    ## IMAGE PIETER
    lengths = []
    intersection_points = []
    for intersection in intersections:
        lengths.append(len(intersection))
    for intersect in intersections:
        print len(intersect) 
    left = intersections[0]
    top = intersections[1]
    right = intersections[2]
    points = left + top + right
    next_direction = direction_list[0]
    
    if len(left) == 0 and len(right) == 0 and len(top) == 0:
        return last_ratio
    
    elif ((len(left) == 0 and len(right) == 0 and len(top) > 0)):
        return choose_path(ratio_queue, next_direction, threshold, [cog_y(points)], 'normal_straight', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        
    elif (len(left) == 0 and len(right) > 0 and len(top) == 0):
        return choose_path(ratio_queue, next_direction, threshold, [cog_x(points)], 'normal_left', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        
    elif (len(left) > 0 and len(right) == 0 and len(top) == 0) :
        return choose_path(ratio_queue, next_direction, threshold, [cog_x(points)], 'normal_right', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        
    elif len(left) > 0 and len(right) > 0 and len(top) == 0:
        left_des = cog_y(left)
        right_des = cog_y(right)
        return choose_path(ratio_queue, next_direction, threshold, [left_des, rigth_des], 'T_flat', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)

    elif len(left) > 0 and len(right) == 0 and len(top) > 0:
        left_des = cog_y(left)
        top_des = cog_x(top)
        return choose_path(ratio_queue, next_direction, threshold, [left_des, top_des], 'T_left', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)

    elif len(left) == 0 and len(right) > 0 and len(top) > 0:
        right_des = cog_y(right)
        top_des = cog_x(top)
        return choose_path(ratio_queue, next_direction, threshold, [top_des, right_des], 'T_right', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        
    else:
        left_des = cog_x(top)
        right_des = cog_y(right)
        top_des = cog_x(top)
        return choose_path(ratio_queue, next_direction, threshold, [left_des, top_des, right_des], 'crossroads', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)



def choose_path(ratio_queue, layout_queue, next_direction, threshold, args, layout, x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right):
    left_destination = (2, int(heigth/2))
    right_destination = (width-2, int(height/2))
    ratio_guess = guess_ratio(ratio_queue)
    if layout.equals('normal_straight') or layout.equals('normal_left') or layout.equals('normal_right'):
         ratio_new = args[0]
    elif layout.equals('T_flat'):
        if next_direction.equals('left'):
            ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction.equals('right'):
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction.equals('straight'):
            ratio_new = to_ratio((args[0] + args[1])/2, x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        else:
            raise AssertionError
    elif layout.equals('T_right') or layout.equals('T_left'):
        if next_direction.equals('left'):
            ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction.equals('right'):
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction.equals('straight'):
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        else:
            raise AssertionError        
    elif layout.equals('crossroads'):
        if next_direction.equals('left'):
            ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction.equals('right'):
            ratio_new = to_ratio(args[2], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction.equals('straight'):
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        else:
            raise AssertionError        
    else:
        raise AssertionError

    weight_of_guess = 0.5
    
    layout_queue = add_to_queue(layout_queue, layout)
    new_layout_queue, new_direction_list = update_direction_list_and_queue(layout_queue, direction_list)    
    return_ratio = (weight_of_guess) * ratio_guess + (1.0 - weight_of_guess) * ratio_new
    ratio_queue = add_to_queue(ratio_queue, return_ratio)    
    return return_ratio, new_layout_queue, new_direction_list

   
def to_ratio(point, x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right):
    left_distance = sqrt((x_des - x_wheel_left)**2 + (y_des - y_wheel_left)**2)
    right_distance= sqrt((x_des - x_wheel_right)**2 + (y_des - y_wheel_right)**2)
    ratio = right_distance/left_distance
    if ratio > 1:
        ratio = -1.0/ratio
    return ratio

def guess_ratio(queue):
    weights, sum_weights = get_weights(queue)
    ratio_guess = 0
    for i in xrange(0, len(queue)):
        ratio_guess += weigths[i]*queue[i]
    past_weighted_ratio = ratio_guess/sum_weights
    return past_weighted_ratio
     
def get_weights(queue):
    weights = []
    sum_weights = 0
    for i in xrange(1, len(queue)):
        current_weigth = 1/i
        weights.append(current_weight)        
        sum_weigths += current_weight
    return weights, sum_weights
    
def update_direction_list_and_queue(queue, direction_list):
    if len(queue)<5:
        return queue, direction_list
    check_list = queue[:5]
    back_on_track = 1
    for elem in check_list:
        if elem.equals('normal_straight') or elem.equals('normal_right') or elem.equals('normal_left'):
            pass
        else:
            back_on_track = 0
    if back_on_track == 1:
        print 'implement counting crossroads'
        print queue
        return queue, direction_list

def convert_to_pairs(image, height, width, column_factor, row_factor):
    left_column = int(width*column_factor)
    right_column = width - left_column
    bottom_row = int(height*row_factor)
    top_row = height - bottom_row
    left_column_intersections = im.fast_check_column(left_column, image, bottom_row, top_row)
    right_column_intersections = im.fast_check_column(right_column, image, bottom_row, top_row)
    bottom_row_intersections = im.fast_check_row(bottom_row, image,  left_column, right_column)
    return (left_column_intersections, bottom_row_intersections, right_column_intersections)

