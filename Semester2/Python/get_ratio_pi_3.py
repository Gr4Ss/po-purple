from numpy import sqrt
import Image_2 as im

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
    len_queue = 40
    queue.insert(0, ratio)
    if len(queue) > len_queue:
        queue.pop()
    return queue

def get_ratio(img,
              x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right,
              last_ratio,
              column_factor, row_factor,
              ratio_queue, layout_queue, direction_list):
    image = im.load_image(str(img))
    height = image.size[1]
    width = image.size[0]
    intersections = convert_to_pairs(image, height, width, column_factor, row_factor)
    lengths = []
    intersection_points = []
    for intersection in intersections:
        lengths.append(len(intersection)) 
    left = intersections[0]
    top = intersections[1]
    right = intersections[2]
    bottom = intersections[3]
    
    left, top, right = get_points(left, right, bottom, top)
    points = left + top + right
    if len(left) == 0 and len(right) == 0 and len(top) == 0:
        return last_ratio
    
    elif ((len(left) == 0 and len(right) == 0 and len(top) > 0)):
        return choose_path(ratio_queue, layout_queue, direction_list, [cog_y(points)], 'normal_straight', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)
        
    elif (len(left) == 0 and len(right) > 0 and len(top) == 0):
        return choose_path(ratio_queue, layout_queue, direction_list, [cog_x(points)], 'normal_right', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)
        
    elif (len(left) > 0 and len(right) == 0 and len(top) == 0) :
        return choose_path(ratio_queue, layout_queue, direction_list, [cog_x(points)], 'normal_left', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)
        
    elif len(left) > 0 and len(right) > 0 and len(top) == 0:
        left_des = cog_y(left)
        right_des = cog_y(right)
        return choose_path(ratio_queue, layout_queue, direction_list, [left_des, right_des], 'T_flat', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)

    elif len(left) > 0 and len(right) == 0 and len(top) > 0:
        left_des = cog_y(left)
        top_des = cog_x(top)
        return choose_path(ratio_queue, layout_queue, direction_list, [left_des, top_des], 'T_left', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)

    elif len(left) == 0 and len(right) > 0 and len(top) > 0:
        right_des = cog_y(right)
        top_des = cog_x(top)
        return choose_path(ratio_queue, layout_queue, direction_list, [top_des, right_des], 'T_right', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)
        
    else:
        left_des = cog_x(top)
        right_des = cog_y(right)
        top_des = cog_x(top)
        return choose_path(ratio_queue, layout_queue, direction_list, [left_des, top_des, right_des], 'crossroads', x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height)



def choose_path(ratio_queue, layout_queue, direction_list, args, layout, x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right, width, height):
    
    left_destination = (2, int(height/2))
    right_destination = (width-2, int(height/2))
    ratio_guess = guess_ratio(ratio_queue)
    next_direction = direction_list[0]
    if layout == 'normal_straight' or layout == 'normal_left' or layout == 'normal_right':
        ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
    elif layout == 'T_flat':
        if next_direction == 'left':
            ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction == 'right':
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction == 'straight':
            ratio_new = to_ratio(((args[0][0] + args[1][0])/2,((args[0][1]+args[1][1])/2)), x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        else:
            raise AssertionError
    elif layout == 'T_right' or layout == 'T_left':
        if next_direction == 'left':
            ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction == 'right':
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction == 'straight':
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        else:
            raise AssertionError        
    elif layout == 'crossroads':
        if next_direction == 'left':
            ratio_new = to_ratio(args[0], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction == 'right':
            ratio_new = to_ratio(args[2], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        elif next_direction == 'straight':
            ratio_new = to_ratio(args[1], x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right)
        else:
            raise AssertionError        
    else:
        raise AssertionError

    weight_of_guess = 0.0
    layout_queue = add_to_queue(layout_queue, layout)
    return_ratio = (weight_of_guess) * ratio_guess + (1.0 - weight_of_guess) * ratio_new
    ratio_queue = add_to_queue(ratio_queue, return_ratio)
    new_ratio_queue, new_layout_queue, new_direction_list = update_direction_list_and_queues(ratio_queue, layout_queue, direction_list)
    return return_ratio, new_layout_queue, new_ratio_queue, new_direction_list

   
def to_ratio(point, x_wheel_left, y_wheel_left, x_wheel_right, y_wheel_right):
    left_distance = sqrt((point[0] - x_wheel_left)**2 + (point[1] - y_wheel_left)**2)
    right_distance= sqrt((point[0] - x_wheel_right)**2 + (point[1] - y_wheel_right)**2)
    ratio = right_distance/left_distance

    if ratio > 1:
        ratio = (-1)*(1.0 - 1.0/ratio)
    else:
        ratio = (1.0 - ratio)
    return ratio

def inverse_ratio(ratio):
    if ratio < 0:
        return 1.0-ratio
    else:
        return (1.0/(ratio))-1.0
    
def guess_ratio(queue):
    if queue == []:
        return 1.0
    weights, sum_weights = get_weights(queue)
    ratio_guess = 0
    for i in xrange(0, len(queue)):
        ratio_guess += weights[i]*queue[i]
    past_weighted_ratio = ratio_guess/sum_weights
    return past_weighted_ratio
     
def get_weights(queue):
    weights = []
    sum_weights = 0
    for i in xrange(1, len(queue)+1):
        current_weight = 1/i
        weights.append(current_weight)        
        sum_weights += current_weight
    return weights, sum_weights
    
def update_direction_list_and_queues(ratio_queue, layout_queue, direction_list):
    if len(layout_queue) < 5:
        return ratio_queue, layout_queue, direction_list
    check_list = layout_queue[:5]
    back_on_track = 1
    for elem in check_list:
        if elem == 'normal_straight' or elem == 'normal_right' or elem == 'normal_left':
            pass
        else:
            back_on_track = 0
    if back_on_track == 1:
        last_direction = get_direction(layout_queue, 4, ratio_queue)
        if last_direction == direction_list[0]:
            print 'turned correctly to the ' + last_direction
            print layout_queue
            return [], [], direction_list[1:]
        else:
            if last_direction == "No node found":
                print last_direction
                return [], [], direction_list
            else:
                print 'turned incorrectly!'
                print layout_queue                
                return [], [], direction_list
    return ratio_queue, layout_queue, direction_list
    
def get_average_ratio(ratio_queue, indices):
    average = 0
    for index in indices:
        average += ratio_queue[index]
    average = average/len(indices)
    return average

def get_most_common_in_queue(layout_queue):
    nb_normal = 0
    nb_T_flat = 0
    nb_T_left = 0
    nb_T_right = 0
    nb_crossroads = 0
    for layout in layout_queue:
        if layout == "normal_left" or layout == "normal_right" or layout == "normal_straight":
            nb_normal += 1
        elif layout == "T_flat":
            nb_T_flat += 1
        elif layout == "T_left":
            nb_T_left += 1
        elif layout == "T_right":
            nb_T_right += 1
        elif layout == "crossroads":
            nb_crossroads += 1
        else:
            raise AssertionError
    numbers = [nb_normal, nb_T_flat, nb_T_left, nb_T_right, nb_crossroads]
    max_index = numbers.index(max(numbers))
    if max_index == 0:
        return 'normal'
    elif max_index == 1:
        return 'T_flat'
    elif max_index == 2:
        return 'T_left'
    elif max_index == 3:
        return 'T_left'
    elif max_index == 4:
        return 'crossroads'
    else:
        raise AssertionError


def get_direction(layout_queue, size, ratio_queue):
    direction_list = ['normal_left','normal_right','normal_straight','T_flat','T_left','crossroads']
    direction = recognize_direction(layout_queue, size, direction_list, ratio_queue)
    if not direction == "No node found":
        return direction
    else:
        return "No node found"
        
    
def recognize_direction(layout_queue, size, direction_list, ratio_queue):
    for i in xrange(0, len(layout_queue)-size):
        curr_layout = layout_queue[i]
        indices = []
        nb = 0
        nb_special = 0
        for k in xrange(i, i + size):            
            if layout_queue[k] in direction_list[2:]:
                nb_special += 1
                indices.append(k)        
        if nb > size - 1:
            for index in indices:
                total_ratio = 0
                for index in indices:
                    total_ratio += ratio_queue[index]
                total_ratio = total_ratio / len(indices)
                boundry = 0.2
                if abs(total_ratio) < boundry:
                    return 'straight'
                elif total_ratio > boundry:
                    return 'right'
                else:
                    return 'left'
    return "No node found"     
                
        
def get_points(left, right, bottom, top):
    if len(bottom) == 2:
        return left, top, right
    else:
        max_index = -1
        if len(bottom) == 1:
            others = left + top + right
            if len(others) == 0:
                return pop_from(left, top, right, max_index)
            maxi = 0
            for other in others:
                if other[1] > maxi:
                    maxi = other[1]
            for other in others:
                if other[1] == maxi:
                    max_index = others.index(other)
            if max_index  == -1:
                return left, top, right
            return pop_from(left, top, right, max_index)
        elif len(bottom) == 0:            
            others = left + top + right
            if len(others)<2:
                return left, top, right
            maxi = 0
            for other in others:
                if other[1] > maxi:
                    maxi = other[1]
            for other in others:
                if other[1] == maxi:
                    max_index = others.index(other)
            if max_index == -1:
                return left, top, right
            others.pop(max_index)
            maxi = 0
            for other in others:
                if other[1] > maxi:
                    maxi = other[1]
            for other in others:
                if other[1] == maxi:
                    max_index = others.index(other)
            if max_index == -1:
                return left, top , right
            others.pop(max_index)
            return pop_from(left, top, right, max_index)
        else:
            return left, top, right
        
def pop_from(left, top, right, max_index):
    if max_index < len(left):
        left.pop(max_index)
    elif max_index < len(left)+len(top):
        top.pop(max_index-len(left))
    else:
        right.pop(max_index-len(left)-len(top))
    return left, top, right
    
def convert_to_pairs(image, height, width, column_factor, row_factor):
    left_column = int(width*column_factor)
    right_column = width - left_column
    bottom_row = int(height*row_factor)
    top_row = height - bottom_row
    left_column_intersections = im.fast_check_column(left_column, image, bottom_row, top_row)
    right_column_intersections = im.fast_check_column(right_column, image, bottom_row, top_row)
    bottom_row_intersections = im.fast_check_row(bottom_row, image,  left_column, right_column)
    top_row_intersections = im.fast_check_row(top_row, image,  left_column, right_column)
    return (left_column_intersections, bottom_row_intersections, right_column_intersections, top_row_intersections)

