import os,sys,inspect
import time
from math import *
from Engine import *
from PID import *
import distanceDetection as dist_detec
from Sensor import *
from IO_thread import *
#first change the cwd to the script pathf
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../BeeldHerkening_Lua")
from lua_python_bridge import *
from PacketDeliveryServer import *

#-----------END IMPORTS------------------

DEBUG = True
'''
'''
class Ratio:
	def __init__(self,PositionLeftWheel,PositionRightWheel,engine_left,engine_right,distance_sensor,packet_delivery=False,directions=[]):
		self.distance_sensor = distance_sensor
		# Storing the position of the left wheel
		self.left_wheel = PositionLeftWheel
		# Storing the position of the right wheel
		self.right_wheel = PositionRightWheel
		# If packet delivery flag is set the server will not follow the directions listed in
		# direction list but instead use data from the packet delivery server to choose it next direction
		self.packet_delivery = packet_delivery
		self.packet_delivery_server = Packet_Delivery_Server((1,2),'localhost',7000)
		# Variabele storing the last used ratio
		self.last_ratio = 0
		# List storing the direction to be followed
		self.direction_list = directions
		# List storing the valid directions
		self.valid_directions = ['straight','left','right']
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
		# turn to determine if we are  on track
		self.back_on_track_threshold = 3
		self.estimate = None
		self.estimate_PID = PID(20,0.2,0.3,0.5)
		self.left_engine = engine_left
		self.right_engine = engine_right
		self.recognize_direction_boundary = 0.35
		# Variable storing the minimum speed
		self.minimum_speed = 60
		# Variable storing the maximum speed
		self.maximum_speed = 115
		self.turning_speed = 120
		self.turning_reversing_speed = 0.7*60
		# Variable storing the threshold value for going to split detection state.
		self.split_count_threshold = 1
		self.split_sharpness = [0,0,0]
		self.next_direction = None
		self.reversing_count = 0
		self.reversing_limit = 10
		self.block_count = 0
		self.block_limit = 3
	def reset(self):
		self.clear_directions()
		self.block_count = 0
		self.reversing_count = 0
		self.driving_state = 'normal'
		self.last_ratio = 0
		self.split_ratio = [0,0]
		self.split_check_phase = 0
		self.split_check_layout= []
		self.split_layout = None
		self.split_count = 0
		self.back_on_track_count = 0
		self.split_sharpness = [0,0,0]
		self.reversing_count = 0
		self.block_count = 0
	def start_packet_delivery_mode(self):
		self.packet_delivery = True
	def stop_packet_delivery_mode(self):
		self.packet_delivery = False
	def update_position(self,position):
		self.packet_delivery_server.update_position(position)
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
		# Bepaal afstand tot opstakel
		d = self.distance_sensor.get_value()
		if d != None:
			slow_down = dist_detec.distance_detection(d)
		else:
			slow_down = 0
		if slow_down >= 255 and not self.driving_state == 'reversing':
			self.block_count += 1
			if (self.block_count >= self.block_limit) and self.packet_delivery:
				if self.packet_delivery_server.can_turn_around():
					self.driving_state == 'reversing'
					self.block_count = 0
				else:
					self.block_count = 0
					return (0,0)
			else:
				return (0,0)
		else:
			self.block_count = 0
		if self.driving_state == 'normal':
			if self.estimate != None:
				left_distance = self.left_engine.get_count()
				right_distance = self.right_engine.get_count()
				distance_driven = (left_distance+right_distance)/2
				estimate_speed = self.estimate_PID.get_value(self.estimate-distance_driven,1)
			if current_layout == None or (not is_special(current_layout)):
				r,sr = self.get_normal_ratio(left,top,right,current_layout)
				#print 'speed ratio', sr,
				bs = max(self.minimum_speed,min(sr*self.minimum_speed,self.maximum_speed))-slow_down
				#bs = self.maximum_speed
				#print ' basic speed', bs
				if bs < self.minimum_speed:
					return (0,0)
				else:
					return self.to_speed(r,bs)
			else:
				self.split_count += 1
				if (self.split_count >= self.split_count_threshold):
					self.driving_state = 'split_detection'
					return (0,0)
				else:
					if current_layout == 'T_flat':
						left_des = mean_y(left)
						right_des = mean_y(right)
						ratio = self.to_ratio(((left_des[0] + right_des[0])/2,(left_des[1]+right_des[1])/2))
						s = self.to_speed(ratio,self.minimum_speed)
						self.last_ratio = ratio
						return s
					else:
						ratio = self.to_ratio(mean_x(top))
						s = self.to_speed(ratio,self.minimum_speed)
						self.last_ratio = ratio
						return s
		# A possible split is detected, extra check is preformed.
		elif self.driving_state == 'split_detection':
			if self.split_check_phase == 0:
				if (len(left) >0 and mean_y(left) < 50):
					self.split_check_phase += 1
					print 'forward'
					return (self.minimum_speed,self.minimum_speed)
				elif (len(right) >0 and mean_y(right) < 50):
					self.split_check_phase += 1
					print 'forward'
					return (self.minimum_speed,self.minimum_speed)
				else:
					self.split_check_phase += 1
					return (0,0)
			#If we are in split_check_phase 0-4 we just look straight at the intersect
			elif self.split_check_phase < 5:
				self.split_check_layout.append(current_layout)
				self.split_check_phase += 1
				l,r = self.calculate_turn_sharpness(left,right)
				self.split_sharpness[0] += l
				self.split_sharpness[1] += r
				self.split_sharpness[2] += 1.
				return (0,0)
			else:
				split_layout = find_layout(self.split_check_layout)
				print 'Detect split with layout', split_layout
				self.split_check_layout = []
				self.split_check_phase = 0
				if split_layout == None or split_layout == 'normal':
					self.driving_state = 'normal'
					print  'To normal state'
				elif split_layout == 'normal_left' or split_layout == 'normal_right':
					self.estimate = None
					self.driving_state = 'normal_turning'
					self.split_layout = split_layout
					print 'To normal turning'
				else:
					self.split_layout = split_layout
					if not self.packet_delivery:
						self.driving_state = 'split_turning'
						print ' To split turning'
						self.next_direction = self.direction_list[0]
					else:
						direction = self.packet_delivery_server.at_split()
						if direction == 'origin':
							self.driving_state = 'reversing'
						else:
							self.driving_state = 'split_turning'
							print ' To split turning'
							self.next_direction = direction
					#self.expected_turning_frames = self.calculate_expected_turning_frames()
					self.expected_turning_frames = 0
				self.split_sharpness = [0,0,0]
				return (-self.minimum_speed,-self.minimum_speed)
		elif self.driving_state == 'normal_turning':
			if current_layout == None:
				self.back_on_track_count += 0.5
			elif current_layout == "normal_straight":
				self.back_on_track_count += 1
			else:
				self.back_on_track_count = 0
			back_on_track = self.back_on_track()
			if back_on_track:
				print 'Correctly turned!'
				# Return back to the normal state
				self.driving_state = 'normal'
				self.back_on_track_count = 0
				r,sr = self.get_normal_ratio(left,top,right,current_layout)
				bs = max(self.minimum_speed,min(sr*self.minimum_speed,self.maximum_speed))-slow_down
				#bs = self.maximum_speed
				if bs < self.minimum_speed:
					return (0,0)
				else:
					return self.to_speed(r,sr)
			else:
				r = self.get_normal_turning_ratio(left,top,right,current_layout)
				self.last_ratio = r
				return self.to_speed(r,self.turning_speed)
		elif self.driving_state == 'reversing':
			if self.reversing_count >= self.reversing_limit:
				if current_layout == "normal_straight":
					self.driving_state = 'normal'
					self.reversing_count = 0
					if self.packet_delivery:
						self.packet_delivery_server.turned_around()
					r,sr = self.get_normal_ratio(left,top,right,current_layout)
					self.last_ratio = r
					return to_speed(r,self.maximum_speed)

			else:
				self.reversing_count += 1
				return (-self.maximum_speed,self.maximum_speed)

		# If turning on a split
		elif self.driving_state == 'split_turning':
			if current_layout == None:
				self.back_on_track_count += 0.1
			elif (not is_special(current_layout)):
				if current_layout == 'normal_straight':
					self.back_on_track_count +=1
				else:
					self.back_on_track_count += 0.5
			else:
				self.back_on_track_count = 0
			# Check if we are back on track after the split
			back_on_track = self.back_on_track()
			if back_on_track:
				last_direction = self.recognize_direction()
				if self.packet_delivery:
					distance = self.packet_delivery_server.turned(last_direction)
					self.estimate = distance
					if distance != None:
						self.estimate_PID.reset()
						self.left_engine.reset_count()
						self.right_engine.reset_count()
				else:
					if last_direction == self.direction_list[0]:
						print 'turned correctly to the ' + last_direction
						self.direction_list.pop(0)
					else:
						print 'turned incorrectly to the '+ last_direction +' !'
				# Return back to the normal state
				self.driving_state = 'normal'
				self.split_ratio = [0,0]
				self.back_on_track_count = 0
				r,sr = self.get_normal_ratio(left,top,right,current_layout)
				self.last_ratio = r
				bs = max(self.minimum_speed,min(sr*self.minimum_speed,self.maximum_speed))-slow_down
				#bs = self.maximum_speed
				if bs < self.minimum_speed:
					return (0,0)
				else:
					return (0,0)

			else:
				ratio = self.get_split_ratio(left,top,right,current_layout,self.direction_list[0])
				self.split_ratio[0] += ratio
				self.split_ratio[1] += 1
				s = self.to_speed(ratio,self.turning_speed)
				self.last_ratio = ratio
				return s

	def get_normal_turning_ratio(self,left,top,right,current_layout):
		if current_layout == None:
			return self.last_ratio
		elif current_layout == 'normal_straight':
			ratio = self.to_ratio(mean_x(top))
			return ratio
		elif self.split_layout == 'normal_left':
			if current_layout == 'normal_left' or current_layout == 'T_left' or current_layout == 'crossroads' or current_layout =='T_flat':
				ratio = self.to_ratio(mean_y(left))
				return ratio
			else:
				return self.last_ratio
		elif self.split_layout == 'normal_right':
			if current_layout == 'normal_right' or current_layout == 'T_right' or current_layout == 'crossroads' or current_layout =='T_flat':
				ratio = self.to_ratio(mean_y(right))
				return ratio
			else:
				return self.last_ratio

	def get_normal_ratio(self,left,top,right,current_layout):
		if current_layout == None:
			if self.last_ratio != 0:
				return self.last_ratio,log(2./abs(self.last_ratio)**2,10)
			else:
				return self.last_ratio,1
		elif current_layout == 'normal_straight':
			ratio = self.to_ratio(mean_x(top))
			if ratio != 0:
				speed_ratio = log(2./abs(ratio)**2,10)
				return ratio,speed_ratio
			else:
				return ratio,1
		elif current_layout == 'normal_left':
			ratio = self.to_ratio(mean_y(left))
			return ratio,0
		elif current_layout == 'normal_right':
			ratio = self.to_ratio(mean_y(right))
			return ratio,0


	def get_split_ratio(self,left,top,right,layout,next_direction):
		if layout == None or (not is_special(layout) and self.split_ratio[1] < self.expected_turning_frames):
			return self.last_ratio
		elif layout == 'normal_straight':
			return self.to_ratio(mean_x(top))
		elif layout == 'normal_right' and self.next_direction != 'left':
			return self.to_ratio(mean_y(right))
		elif layout == 'normal_left' and self.next_direction != 'right':
			return self.to_ratio(mean_y(left))
		elif layout == 'T_flat':
			if next_direction == 'left':
				return self.to_ratio(mean_y(left))
			elif next_direction == 'right':
				return self.to_ratio(mean_y(right))
			else:
				return self.last_ratio
		elif layout == 'T_right':
			if next_direction == 'right':
				return self.to_ratio(mean_y(right))
			elif next_direction == 'straight':
				return self.to_ratio(mean_x(top))
			else:
				return self.last_ratio
		elif layout == 'T_left':
			if next_direction == 'left':
				return self.to_ratio(mean_y(left))
			elif next_direction == 'straight':
				return self.to_ratio(mean_x(top))
			else:
				return self.last_ratio
		elif layout == 'crossroads':
			if next_direction == 'left':
				return self.to_ratio(mean_y(left))
			elif next_direction == 'right':
				return self.to_ratio(mean_y(right))
			elif next_direction == 'straight':
				return self.to_ratio(mean_x(top))
			print 'You shouldn\'t  be here'
		else:
			return self.last_ratio

	def recognize_direction(self):
		total_ratio = self.split_ratio[0]
		nb = self.split_ratio[1]
		total_ratio = total_ratio /nb
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
		ratio = (right_distance/left_distance)
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
	def to_speed(self,ratio,basic_speed,turn_back = True):
		# If ratio is bigger then one than left must drive a bigger distance then right
		if ratio >= 0:
			lspeed = basic_speed
			rspeed = (1.-ratio)*basic_speed
			# If the right speed is very low it must drive backward
			if (rspeed < self.turning_reversing_speed) and turn_back:
				rspeed = (-1.)*self.minimum_speed
			# If the right speed is low it must drive the minimum speed
			elif (rspeed < self.minimum_speed):
				lspeed = self.minimum_speed/(1.-ratio)
				rspeed = self.minimum_speed
			return (lspeed,rspeed)
		else:
			lspeed = (1.+ratio)*basic_speed
			rspeed = basic_speed
			# If the left speed is very low it must drive backward
			if (lspeed < self.turning_reversing_speed):
				lspeed = (-1.)*self.minimum_speed
			# If the right speed is low it must drive the minimum speed
			elif (lspeed < self.minimum_speed):
				rspeed = self.minimum_speed/(1.+ratio)
				lspeed = self.minimum_speed
			return (lspeed,basic_speed)

	"""
	Method to calculate the sharpness of the turn
	INPUT:
		- left: points on the left edge
		- right: point on the right edge
	OUTPUT:
		- tuple with (left,right) sharpness
	"""
	def calculate_turn_sharpness(self,left,right):
		l = 0
		r = 0
		if len(left) > 0:
			pl = maximum(left,1)
			l = atan2((self.right_wheel[1] - pl[1]),float((self.right_wheel[0] -pl[0])))
		if len(right) > 0:
			pr = maximum(right,1)
			r = atan2((self.left_wheel[1] - pr[1]),float((pr[0]-self.left_wheel[0])))
		return l,r
	def calculate_expected_turning_frames(self):

		if self.next_direction == "left":
			s = self.split_sharpness[0]/self.split_sharpness[2]
			if s == 0:
				s = 1
			return min(15,7.5/s)
		elif self.next_direction == "right":
			s = self.split_sharpness[1]/self.split_sharpness[2]
			if s == 0:
				s =1
			return min(15,7.5/s)
		else:
			return 0
# Returns the x coordinate of the first point and the average
# x coordinate for all points
def mean_x(points):
    cog_x = 0
    for point in points:
        cog_x += point[0]
    cog_x = cog_x/len(points)
    return (cog_x, points[0][1])

def mean_y(points):
    cog_y = 0
    for point in points:
        cog_y += point[1]
    cog_y = cog_y/len(points)
    return (points[0][0], cog_y)


'''Method to classify an image.
 Possible results: 'normal_left','normal_right','normal_straight'
 'T-flat','T-right','T-left','crossroads' or None when no points are detected
 Intersections in the form of [left,top,right]
'''
def classify_image(left,top,right):
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


def maximum(lst,dim):
	m = 0
	r = None
	for item in lst:
		if item[dim]>m:
			m = item[dim]
			r = item
	return r
def sign(value):
	return 0 if value ==0 else (1 if value > 0 else -1)

def get_most_common_in_queue(layout_queue):
	nb_normal = 0
	nb_normal_left = 0
	nb_normal_right = 0
	nb_T_flat = 0
	nb_T_left = 0
	nb_T_right = 0
	nb_crossroads = 0
	for layout in layout_queue:
		if layout == "normal_straight":
			nb_normal += 1
		elif layout == "normal_left":
			nb_normal_left += 1
		elif layout == "normal_right":
			nb_normal_right += 1
		elif layout == "T_flat":
			nb_T_flat += 1
		elif layout == "T_left":
			nb_T_left += 1
		elif layout == "T_right":
			nb_T_right += 1
		elif layout == "crossroads":
			nb_crossroads += 1
		elif layout == None:
			pass
	numbers = [nb_normal, nb_normal_left,nb_normal_right, nb_T_flat, nb_T_left, nb_T_right, nb_crossroads]
	max_index = numbers.index(max(numbers))
	return ['normal','normal_left','normal_right','T_flat','T_left','T_right','crossroads'][max_index]


def find_layout(layout_queue):
    return get_most_common_in_queue(layout_queue)

def is_special(layout):
	if layout == None:
		return False
	else:
		return (layout.split('_')[0]!= 'normal')
def calculate_ratio(speed):
	if (speed[0] == 0 and speed[1] == 0):
		return 0
	elif (speed[0] == 0):
		return -1
	ratio = abs(speed[1]/speed[0])
	if ratio > 1:
		ratio = (-1)*(1.0 - 1.0/ratio)
	else:
		ratio = (1.0 - ratio)
	return ratio
leftengine = Engine('A')
rightengine = Engine('B')
sensor = DistanceSensor(17,4)
brickpi = IO_Thread([leftengine,rightengine],[sensor])
brickpi.on()

rt = Ratio((0,287),(480,287),None,None,sensor,False,['right','straight','left','right','straight','right','right','straight','left','left'])
while True:
	start = time.time()
	s = rt.get_speed()
	#print s
	leftengine.set_speed(s[0])
	rightengine.set_speed(s[1])
	end = time.time()
	if end-start < 0.075:
		time.sleep(0.075-(end-start))
