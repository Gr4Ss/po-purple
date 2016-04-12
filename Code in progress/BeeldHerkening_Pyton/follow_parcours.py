import numpy
import os,sys,inspect
#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../BeeldHerkening_Lua")
from lua_python_bridge import *
#-----------END IMPORTS------------------

DEBUG = True
'''
'''
class Ratio:
	def __init__(self,PositionLeftWheel,PositionRightWheel,packet_delivery=False,directions=[]):
		# Storing the position of the left wheel
		self.left_wheel = PositionLeftWheel
		# Storing the position of the right wheel
		self.right_wheel = PositionRightWheel
		# If packet delivery flag is set the server will not follow the directions listed in
		# direction list but instead use data from the packet delivery server to choose it next direction
		self.packet_delivery = packet_delivery
		# Variabele storing the last used ratio
		self.last_speed = (0,0)
		# List storing the direction to be followed
		self.direction_list = directions
		# List storing the valid directions
		self.valid_directions = ['forward','left','right']
		# Possible driving states:
		# - normal: just normal driving
		# - split_detection: a possible split (crossroad, T-flat, T-left, T-right) is
		# 		detected so a check is preformed
		# - split_turning: Turning on a split (not a normal left,right)
		self.driving_state = 'normal'
		# Variable storing the sum of the ratio's during the turn and the number of ratios
		self.split_ratio = [0,0]
		# Storing a int representing the split check phase
		self.split_check_phase = 0
		# Storing a list with the layouts discovered during checking
		self.split_check_layout= []
		self.split_layout = None
		#
		self.split_count = 0
		# Variable storing how many normal are seen after a split to check that we can go to normal state
		self.back_on_track_count = 0
		# Parameters to edit
		# Variable storing the number of images that must be normal after a split
		# turn to determine if we are back on track
		self.back_on_track_threshold = 3
		#
		self.recognize_direction_boundary = 0.4
		# Variable storing the minimum speed
		self.minimum_speed = 60
		# Variable storing the maximum speed
		self.maximum_speed = 200
		# Variable storing the threshold value for going to split detection state.
		self.split_count_threshold = 2
	'''
	Method to append a direction to direction list.
	The given parameter may be a single direction or a list of directions.
	'''
	def append_directions(self,directions):
		if hasattr(directions, __iter__):
			for d in directions:
				if d in valid_directions:
					self.direction_list.append(d)
		elif directions in valid_directions:
			self.direction_list.append(directions)
	'''
	Method to clear the direction list.
	'''
	def clear_directions(self):
		self.direction_list = []
	'''
	Method that return the speed (left,right) based on the current image, the direction list, ...
	'''
	def get_speed(self):
		# Get the points which are intersecting with the drawn lines.
		left,top,right,bottom = get_points()
		# Determine the layout of the current image
		current_layout = classify_image(left,top,right)
		if self.driving_state == 'normal':
			if (not is_special(current_layout)) or current_layout == None:
				s = self.get_normal_speed(left,top,right,current_layout)
				self.last_speed = s
				return s
			else:
				self.split_count += 1
				if (self.split_count >= self.split_count_threshold):
					self.driving_state = 'split_detection'
					s = (0,0)
					self.last_speed = s
					return s
				else:
					if current_layout == 'T-flat':
						left_des = mean_y(left)
						right_des = mean_y(right)
						ratio = self.to_ratio(((left_des[0] + right_des[0])/2,(left_des[1]+right_des[1])/2))
						s = to_speed(ratio,self.minimum_speed)
						self.last_speed = s
						return s
					else:
						ratio = self.to_ratio(mean_x(top))
						s = to_speed(ratio,self.minimum_speed)
						self.last_speed = s
						return s
		# A possible split is detected, extra check is preformed.
		elif self.driving_state == 'split_detection':
			#If we are in split_check_phase 0-4 we just look straight at the intersect
			if self.split_check_phase < 5:
				self.split_check_layout.append(current_layout)
				return (0,0)
			# During split_check_phase 5-10 we turn slightly to the left and back to the center
			elif self.split_check_phase < 11:
				self.split_check_layout.append(current_layout)
				return (self.minimum_speed*sign(self.split_check_phase-7.5),0)
			# During split_check_phase 11-16 we turn slightly to the right and back to the center
			elif self.split_check_phase <17:
				self.split_check_layout.append(current_layout)
				return (0,self.minimum_speed*sign(self.split_check_phase-13.5))
			# All checks are done
			else:
				split_layout = find_layout(self.split_check_layout)
				self.split_check_layout = []
				self.split_check_phase = 0
				if split_layout == None:
					self.driving_state = 'normal'
				else:
					#TODO check if the next direction is possible given the current layout
					#TODO Ask for the next direction if in packet delivery mode
					self.split_layout = split_layout
					self.driving_state = 'split_turning'
				return (0,0)
		# If turning on a split
		elif self.driving_state == 'split_turning':
			if (not is_special(current_layout)):
				self.back_on_track_count +=1
			else:
				self.back_on_track_count = 0
			# Check if we are back on track after the split
			back_on_track = self.back_on_track()
			if back_on_track:
				last_direction = self.recognize_direction()
				if last_direction == direction_list[0]:
					print 'turned correctly to the ' + last_direction
					self.direction_list.pop(0)
				else:
					print 'turned incorrectly to the'+ last_direction +' !'
				# Return back to the normal state
				self.driving_state = 'normal'
				self.split_ratio = [0,0]
				return self.get_normal_speed(left,top,right,current_layout)
			else:
				ratio = self.get_split_ratio(left,top,right,current_layout,self.direction_list[0])
				self.split_ratio[0] += ratio
				self.split_ratio[1] += 1
				return to_speed(ratio,self.minimum_speed)
	def get_normal_speed(self,left,top,right,layout):
		if current_layout == None:
			return self.last_ratio
		elif current_layout == 'normal_straight':
			ratio = self.to_ratio(mean_x(top))
			if ratio != 0:
				basic_speed = max(self.minimum_speed,min(math.log(1./abs(ratio)**2,10)*self.minimum_speed,self.maximum_speed))
				return to_speed(ratio,basic_speed)
			else:
				return (self.maximum_speed,self.maximum_speed)
		elif current_layout == 'normal_left':
			ratio = self.to_ratio(mean_y(left))
			return to_speed(ratio,self.minimum_speed)
		elif current_layout == 'normal_right':
			ratio = self.to_ratio(mean_y(right))
			return to_speed(ratio,self.minimum_speed)
	def get_split_ratio(self,left,top,right,layout,next_direction):
		left_destination = (2, int(height/2))
		right_destination = (width-2, int(height/2))
		if layout == None:
			ratio = (self.last_speed[1]/self.last_speed[0])
			if ratio > 1:
				ratio = (-1)*(1.0 - 1.0/ratio)
    		else:
        		ratio = (1.0 - ratio)
    		return ratio
		if layout == 'normal_straight':
			return self.to_ratio(mean_x(top))
		elif layout == 'normal_right':
			return self.to_ratio(mean_y(right))
		elif layout == 'normal_left':
			return self.to_ratio(mean_y(left))
		elif layout == 'T_flat':
			if next_direction == 'left':
				return self.to_ratio(mean_y(left))
			elif next_direction == 'right':
				return self.to_ratio(mean_y(right))
			else:
				ratio = (self.last_speed[1]/self.last_speed[0])
				if ratio > 1:
					ratio = (-1)*(1.0 - 1.0/ratio)
				else:
					ratio = (1.0 - ratio)
	    		return ratio
		elif layout == 'T_right':
			if next_direction == 'right':
				return self.to_ratio(mean_y(right))
			elif next_direction == 'straight':
				return self.to_ratio(mean_x(top))
			else:
				ratio = (self.last_speed[1]/self.last_speed[0])
				if ratio > 1:
					ratio = (-1)*(1.0 - 1.0/ratio)
				else:
					ratio = (1.0 - ratio)
	    		return ratio
		elif layout == 'T_left':
			if next_direction == 'left':
				return self.to_ratio(mean_y(left))
			elif next_direction == 'straight':
				return self.to_ratio(mean_x(top))
			else:
				ratio = (self.last_speed[1]/self.last_speed[0])
				if ratio > 1:
					ratio = (-1)*(1.0 - 1.0/ratio)
				else:
					ratio = (1.0 - ratio)
	    		return ratio
		elif layout == 'crossroads':
			if next_direction == 'left':
				return self.to_ratio(mean_y(left))
			elif next_direction == 'right':
				return self.to_ratio(mean_y(right))
        	elif next_direction == 'straight':
				return self.to_ratio(mean_x(top))
		else:
			ratio = (self.last_speed[1]/self.last_speed[0])
			if ratio > 1:
				ratio = (-1)*(1.0 - 1.0/ratio)
			else:
				ratio = (1.0 - ratio)
			return ratio

	def recognize_direction(self):
		total_ratio = self.split_ratio[0]
		nb = self.split_ratio[1]
		total_ratio = total_ratio /nb
		print total_ratio
		boundary = self.recognize_direction_boundary
		if abs(total_ratio) < boundary:
			return 'straight'
		elif total_ratio > boundary:
			return 'right'
		else:
			return 'left'

	def to_ratio(self,point):
    		left_distance = sqrt((point[0] - self.left_wheel[0])**2 + (point[1] - self.left_wheel[1])**2)
    		right_distance= sqrt((point[0] - self.right_wheel[0])**2 + (point[1] - self.right_wheel[1])**2)
    		ratio = right_distance/left_distance
    		if ratio > 1:
        		ratio = (-1)*(1.0 - 1.0/ratio)
    		else:
        		ratio = (1.0 - ratio)
    		return ratio
	'''
	Method to check wheter you're back on track after a split turning
	'''
	def back_on_track(self):
		return self.back_on_track_count > self.back_on_track_threshold



# Returns the x coordinate of the first point and the average
# x coordinate for all points
def mean_x(points):
    pointss = numpy.array(points)
    mean_x = numpy.average(pointss, axis=0)[0]
    return (mean_x, points[0][1])

# Returns the y coordinate of the first point and the average
# y coordinate for all points
def mean_y(points):
    pointss = numpy.array(points)
    mean_y = numpy.average(pointss, axis=0)[1]
    return (points[0][0], mean_y)

'''Method to classify an image.
 Possible results: 'normal_left','normal_right','normal_straight'
 'T-flat','T-right','T-left','crossroads' or None when no points are detected
 Intersections in the form of [left,top,right]
'''
def classify_image(intersections):
	# There are no points on the image, do as before
	if len(left) == 0 and len(right) == 0 and len(top) == 0:
		return None
	# There are points on the top row of the image, it's just a normal straight.
	elif ((len(left) == 0 and len(right) == 0 and len(top) > 0)):
		return 'normal_straight'
	# There are points on the right side of the image, go right.
	elif (len(left) == 0 and len(right) > 0 and len(top) == 0):
		return 'normal_right'
	# There are points on the left side of the image, go left.
	elif (len(left) > 0 and len(right) == 0 and len(top) == 0):
		return 'normal_left'
	# There are points on the left and right side of the image.
	elif len(left) > 0 and len(right) > 0 and len(top) == 0:
		return 'T_flat'
	# There are points on the left and the top side of the image
	elif len(left) > 0 and len(right) == 0 and len(top) > 0:
		return 'T_left'
	# There are points on the right and the top side of the image
	elif len(left) == 0 and len(right) > 0 and len(top) > 0:
		return 'T_right'
	# Else there are crossroads which are detected
	else:
		return 'crossroads'

def to_speed(ratio,basic_speed):
	# If ratio is bigger then one than left must drive a bigger distance then right
	if ratio >= 0:
		rspeed = (1.-ratio)*basic_speed
		# If the right speed is very low it must drive backward
		if (rspeed < self.minimum_speed*0.75):
			rspeed = (-1.)*self.minimum_speed
		# If the right speed is low it must drive the minimum speed
		elif (rspeed < self.minimum_speed):
			rspeed = self.minimum_speed
		return (basic_speed,rspeed)
	else:
		lspeed = (1.+ratio)*basic_speed
		# If the left speed is very low it must drive backward
		if (lspeed < self.minimum_speed*0.75):
			lspeed = (-1.)*self.minimum_speed
		# If the right speed is low it must drive the minimum speed
		elif (lspeed < self.minimum_speed):
			lspeed = self.minimum_speed
		return (lspeed,basic_speed)


def sign(value):
	return 0 if value ==0 else (1 if value > 0 else -1)

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

def find_layout(layout_queue):
    nb_special = 0
    nb_special = len(layout_queue) - nb_normal
    if nb_special < 2:
        return "normal"
    else:
        return get_most_common_in_queue(layout_queue)

def is_special(layout):
    return (layout.split('_')[0]!= 'normal')


        
