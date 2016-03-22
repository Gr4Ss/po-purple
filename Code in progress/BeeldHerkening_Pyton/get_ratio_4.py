import numpy
import Image_2 as img

global layout_queue, ratio_queue

# Returns the x coordinate of the first point and the average
# x coordinate for all points
def cog_x(points):
    pointss = numpy.array(points)
    cog_x = numpy.average(pointss, axis=0)[0]
    return (cog_x, points[0][1])

# Returns the y coordinate of the first point and the average
# y coordinate for all points
def cog_y(points):
    pointss = numpy.array(points)
    cog_y = numpy.average(pointss, axis=0)[1]
    return (points[0][0], cog_y)

# Add the item to the queue, while maintaining the maximum queue length
def add_to_queue(queue, ratio):
    len_queue = 40
    queue.insert(0, ratio)
    if len(queue) > len_queue:
        queue.pop()
    return queue

def get_ratio(imageAddress, xCoLeft, yCoLeft, xCoRight, yCoRight, last_ratio,
              column_factor, row_factor, direction_list):
    # Load in the current image
    image = im.load_image(str(imageAddress))
    imgHeight = image.size[1]
    imgWidth = image.size[0]
	
    # Get the points which are intersecting with the drawn lines.
    intersections = getIntersectingPoints(image, imageHeight, imageWidth, column_factor, row_factor)
    left = intersections[0]
    top = intersections[1]
    right = intersections[2]
    bottom = intersections[3]
    
	
    left, top, right = getPoints(left, right, bottom, top)
	
    points = left + top + right
	
    # There are no points on the image, do as before
    if len(left) == 0 and len(right) == 0 and len(top) == 0:
        return last_ratio
    
    # There are points on the top half of the image, go straight.
    elif ((len(left) == 0 and len(right) == 0 and len(top) > 0)):
        return choose_path(ratio_queue, layout_queue, direction_list, [cog_y(points)], 'normal_straight', xCoLeft, yCoLeft, xCoRight, yCoRight)
       
    # There are points on the right side of the image, go right.
    elif (len(left) == 0 and len(right) > 0 and len(top) == 0):
        return choose_path(ratio_queue, layout_queue, direction_list, [cog_x(points)], 'normal_right', xCoLeft, yCoLeft, xCoRight, yCoRight)
        
    # There are points on the left side of the image, go left.
    elif (len(left) > 0 and len(right) == 0 and len(top) == 0) :
        return choose_path(ratio_queue, layout_queue, direction_list, [cog_x(points)], 'normal_left', xCoLeft, yCoLeft, xCoRight, yCoRight)
        
    # There are points on the left and right side of the image.
    elif len(left) > 0 and len(right) > 0 and len(top) == 0:
        left_des = cog_y(left)
        right_des = cog_y(right)
        return choose_path(ratio_queue, layout_queue, direction_list, [left_des, right_des], 'T_flat', xCoLeft, yCoLeft, xCoRight, yCoRight)

    # There are points on the left and the top side of the image
    elif len(left) > 0 and len(right) == 0 and len(top) > 0:
        left_des = cog_y(left)
        top_des = cog_x(top)
        return choose_path(ratio_queue, layout_queue, direction_list, [left_des, top_des], 'T_left', xCoLeft, yCoLeft, xCoRight, yCoRight)

    # There are points on the right and the top side of the image
    elif len(left) == 0 and len(right) > 0 and len(top) > 0:
        right_des = cog_y(right)
        top_des = cog_x(top)
        return choose_path(ratio_queue, layout_queue, direction_list, [top_des, right_des], 'T_right', xCoLeft, yCoLeft, xCoRight, yCoRight)
    
    # Else there are crossroads which are detected
    else:
        left_des = cog_x(top)
        right_des = cog_y(right)
        top_des = cog_x(top)
        return choose_path(ratio_queue, layout_queue, direction_list, [left_des, top_des, right_des], 'crossroads', xCoLeft, yCoLeft, xCoRight, yCoRight)


# Choose which path you are going to take
def choose_path(ratio_queue, layout_queue, direction_list, args, layout, xCoLeft, yCoLeft, xCoRight, yCoRight):
    # Guess the ratio from the ratio queue.
    ratio_guess = guess_ratio(ratio_queue)
	
    next_direction = direction_list[0]
	
    # Calculate ratios for all different layouts
    if layout == 'normal_straight' or layout == 'normal_left' or layout == 'normal_right':
        ratio_new = to_ratio(args[0], xCoLeft, yCoLeft, xCoRight, yCoRight)
    elif layout == 'T_flat':
        if next_direction == 'left':
            ratio_new = to_ratio(args[0], xCoLeft, yCoLeft, xCoRight, yCoRight)
        elif next_direction == 'right':
            ratio_new = to_ratio(args[1], xCoLeft, yCoLeft, xCoRight, yCoRight)
        elif next_direction == 'straight':
            ratio_new = to_ratio(((args[0][0] + args[1][0])/2,((args[0][1]+args[1][1])/2)), xCoLeft, yCoLeft, xCoRight, yCoRight)
        else:
            raise AssertionError
    elif layout == 'T_right' or layout == 'T_left':
        if next_direction == 'left':
            ratio_new = to_ratio(args[0], xCoLeft, yCoLeft, xCoRight, yCoRight)
        elif next_direction == 'right':
            ratio_new = to_ratio(args[1], xCoLeft, yCoLeft, xCoRight, yCoRight)
        elif next_direction == 'straight':
            ratio_new = to_ratio(args[1], xCoLeft, yCoLeft, xCoRight, yCoRight)
        else:
            raise AssertionError        
    elif layout == 'crossroads':
        if next_direction == 'left':
            ratio_new = to_ratio(args[0], xCoLeft, yCoLeft, xCoRight, yCoRight)
        elif next_direction == 'right':
            ratio_new = to_ratio(args[2], xCoLeft, yCoLeft, xCoRight, yCoRight)
        elif next_direction == 'straight':
            ratio_new = to_ratio(args[1], xCoLeft, yCoLeft, xCoRight, yCoRight)
        else:
            raise AssertionError        
    else:
        raise AssertionError

    # Guess the ratio from the ratio queue.
    ratio_guess = guess_ratio(ratio_queue)
    weight_of_guess = 0.0
    layout_queue = add_to_queue(layout_queue, layout)
	
    return_ratio = (weight_of_guess) * ratio_guess + (1.0 - weight_of_guess) * ratio_new
    ratio_queue = add_to_queue(ratio_queue, return_ratio)
    new_ratio_queue, new_layout_queue, new_direction_list = update_direction_list_and_queues(ratio_queue, layout_queue, direction_list)
    return return_ratio, new_layout_queue, new_ratio_queue, new_direction_list

   
def to_ratio(point, xCoLeft, yCoLeft, xCoRight, yCoRight):
    left_distance = sqrt((point[0] - xCoLeft)**2 + (point[1] - yCoLeft)**2)
    right_distance= sqrt((point[0] - xCoRight)**2 + (point[1] - yCoRight)**2)
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
    print layout_queue
    check_list = layout_queue[:5]
    back_on_track = 1
    for elem in check_list:
        if elem == 'normal_straight' or elem == 'normal_right' or elem == 'normal_left':
            pass
        else:
            back_on_track = 0
    if back_on_track == 1:
        last_direction = get_direction(layout_queue, 5, ratio_queue)
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

def get_most_common_in_queue(layout_queue):
    return max(set(layout_queue), key=layout_queue.count)


def get_direction(layout_queue, size, ratio_queue):
    direction_list = ['normal_straight','normal_right','normal_left','T_flat','T_left','T_right','crossroads']
    direction = recognize_direction2(layout_queue, size, direction_list, ratio_queue)
    return direction

        
    
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
                
def recognize_direction2(layout_queue, size, direction_list, ratio_queue):
    start_special = -1
    end_special = -1
    for i in xrange(0, len(layout_queue)):    
        if is_special(layout_queue[i]) and start_special == -1:
            start_special = i
        if (not is_special(layout_queue[i]) or i == len(layout_queue)-1) and not start_special == -1:
            end_special = i
        if not end_special == -1 and not start_special == -1:
            if abs(end_special-start_special)<4:
                start_special = -1
                end_special = -1
            else:
                total_ratio = 0
                nb = 0
                for j in xrange(start_special, end_special):
                    total_ratio += ratio_queue[j]
                    nb += 1
                total_ratio = total_ratio /nb
                print total_ratio
                boundry = 0.2
                if abs(total_ratio) < boundry:
                    return 'straight'
                elif total_ratio > boundry:
                    return 'right'
                else:
                    return 'left'                            
    return "No node found"

def is_special(layout):
    return (layout in ['T_flat','T_left','T_right','crossroads'])

#Get the appropriate columns for crossroad detection
def getPoints(left, right, bottom, top):
    if len(bottom) == 2:
        return left, top, right
    else:
        max_index = -1
        if len(bottom) == 1:
            others = left + top + right
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
    
# Return the points which are intersecting with the drawn lines.
def getIntersectingPoints(image, height, width, column_factor, row_factor):
    left_column = int(width*column_factor)
    right_column = width - left_column
    bottom_row = int(height*row_factor)
    top_row = height - bottom_row
    left_column_intersections = im.fast_check_column(left_column, image, bottom_row, top_row)
    right_column_intersections = im.fast_check_column(right_column, image, bottom_row, top_row)
    bottom_row_intersections = im.fast_check_row(bottom_row, image,  left_column, right_column)
    top_row_intersections = im.fast_check_row(top_row, image,  left_column, right_column)
    return (left_column_intersections, bottom_row_intersections, right_column_intersections, top_row_intersections)

