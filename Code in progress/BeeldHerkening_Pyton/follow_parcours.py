#import os,sys,inspect
from math import *
import PID
import distanceDetection as dist_detec

#first change the cwd to the script pathf
#scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
#os.chdir(scriptPath)
#append the relative location you want to import from
#sys.path.append("../BeeldHerkening_Lua")
from lua_python_bridge import *
from PacketDeliveryServer import *

#-----------END IMPORTS------------------

DEBUG = False
'''
'''
class Ratio:
	def __init__(self,PositionLeftWheel,PositionRightWheel,engine_left,engine_right,left_lamp,right_lamp,distance_sensor,packet_delivery=False,directions=[]):
		self.distance_sensor = distance_sensor
		# Storing the position of the left wheel
		self.left_wheel = PositionLeftWheel
		# Storing the position of the right wheel
		self.right_wheel = PositionRightWheel
		# If packet delivery flag is set the server will not follow the directions listed in
		# direction list but instead use data from the packet delivery server to choose it next direction
		self.packet_delivery = packet_delivery
		self.packet_delivery_server = Packet_Delivery_Server((1,2))
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
		# Variable storing how many normal are seen after a split to check that we can go to normal state
		self.back_on_track_count = 0
		# Parameters to edit
		# Variable storing the number of images that must be normal after a split
		# turn to determine if we are  on track
		self.back_on_track_threshold = 3
		self.estimate = None
		self.estimate_PID = PID.PID(20,0.2,0.3,0.5)
		self.normal_PID = PID.PID(0.9,0.1,0.05,0)
		self.left_engine = engine_left
		self.right_engine = engine_right
		self.left_lamp = left_lamp
		self.right_lamp = right_lamp
		self.recognize_direction_boundary = 0.35
		# Variable storing the minimum speed
		self.minimum_speed = 70
		# Variable storing the maximum speed
		self.maximum_speed = 115
		self.turning_speed = 110
		self.turning_reversing_speed = 0.65*70
		self.turning_reversing_speed_2 = 0.7*70
		self.next_direction = None
		self.reversing_count = 0
		self.reversing_limit = 10
		self.block_count = 0
		self.block_limit = 10
		self.socket = None
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
		self.back_on_track_count = 0
		self.reversing_count = 0
		self.block_count = 0
		self.normal_PID.reset()
	def start_packet_delivery_mode(self):
		self.packet_delivery = True
	def stop_packet_delivery_mode(self):
		self.packet_delivery = False
	def update_position(self,position):
		self.packet_delivery_server.update_position(position)
	def set_socket(self,socket):
		self.socket = socket
		self.packet_delivery_server.set_socket(socket)
	def send_data(self,data):
		data = {'Type':'parcoursUpdate','data':data}
		if self.socket != None:
			if not self.socket.connected:
				self.socket.connect()
			self.socket.send_data(data)

	'''
	Method to append a direction to direction list.
	The given parameter may be a single direction or a list of directions.
	'''
	def append_directions(self,directions):
		if hasattr(directions,'__iter__'):
			for d in directions:
				if d in self.valid_directions:
					self.direction_list.append(d)
		elif directions in self.valid_directions:
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
			if (self.block_count >= self.block_limit):
				if not self.packet_delivery or self.packet_delivery_server.can_turn_around():
					self.driving_state = 'reversing'
					self.block_count = 0
					print 'TO REVERSING STATE'
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
			if current_layout == None or current_layout == 'normal_straight':
				r,sr = self.get_normal_ratio(left,top,right,current_layout)
				self.last_ratio = r
				if DEBUG:
					print 'ratio',r,' speed ratio', sr,
				bs = max(self.minimum_speed,min(sr*self.minimum_speed,self.maximum_speed))
				if DEBUG:
					print ' basic speed', bs
				return self.to_speed(r,bs)
			else:
				print 'To split detection'
				self.driving_state = 'split_detection'
				return (-self.minimum_speed,-self.minimum_speed)
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
			elif self.split_check_phase < 5:
				self.split_check_layout.append(current_layout)
				self.split_check_phase += 1
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
					self.normal_PID.reset()
					self.estimate = None
					self.driving_state = 'normal_turning'
					self.split_layout = split_layout
					print 'To normal turning'
				else:

					self.split_layout = split_layout
					if not self.packet_delivery:

						if len(self.direction_list) >0:
							self.driving_state = 'split_turning'
							print ' To split turning'
							self.next_direction = self.direction_list[0]
							if self.next_direction == 'left':
								self.left_lamp.set_on()
							elif self.next_direction == 'right':
								self.right_lamp.set_on()
						else:
							print 'No more directions'
							return ('Done','Done')
					else:
						direction = self.packet_delivery_server.at_split()
						if direction == 'origin':
							self.driving_state = 'reversing'
							print 'To reversing state'
						else:
							self.driving_state = 'split_turning'
							print ' To split turning'
							self.next_direction = direction
							if self.next_direction == 'left':
								self.left_lamp.set_on()
							elif self.next_direction == 'right':
								self.right_lamp.set_on()
				return (-self.minimum_speed,-self.minimum_speed)
		elif self.driving_state == 'normal_turning':
			if current_layout == None:
				self.back_on_track_count += 0.3
			elif current_layout == "normal_straight":
				self.back_on_track_count += 1
			else:
				self.back_on_track_count = 0
			if self.back_on_track():
				print 'Correctly turned!'
				# Return back to the normal state
				self.normal_PID.reset()
				self.driving_state = 'normal'
				self.back_on_track_count = 0
				r,sr = self.get_normal_ratio(left,top,right,current_layout)
				self.last_ratio = r
				if DEBUG:
					print 'ratio: ',r,' speed ratio: ',sr
				bs = max(self.minimum_speed,min(sr*self.minimum_speed,self.maximum_speed))
				return self.to_speed(r,sr)
			else:
				r = self.get_normal_turning_ratio(left,top,right,current_layout)
				self.last_ratio = r
				print 'ratio: ',r
				return self.to_speed(r,self.turning_speed,True)
		elif self.driving_state == 'reversing':
			print self.reversing_count
			if self.reversing_count >= self.reversing_limit:
				if current_layout == "normal_straight":
					self.driving_state = 'normal'
					self.reversing_count = 0
					if self.packet_delivery:
						self.packet_delivery_server.turned_around()
					r,sr = self.get_normal_ratio(left,top,right,current_layout)
					self.last_ratio = r
					return self.to_speed(r,self.maximum_speed)
				else:
					self.reversing_count += 1
					return (-self.minimum_speed,self.minimum_speed)

			else:
				self.reversing_count += 1
				return (-self.minimum_speed,self.minimum_speed)
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
			if self.back_on_track():
				self.left_lamp.set_off()
				self.right_lamp.set_off()
				self.normal_PID.reset()
				last_direction = self.recognize_direction()
				if self.packet_delivery:
					print 'Turned to ',last_direction
					distance = self.packet_delivery_server.turned(last_direction)
					self.estimate = distance
					if distance != None:
						self.estimate_PID.reset()
						self.left_engine.reset_count()
						self.right_engine.reset_count()

				else:
					if last_direction == self.next_direction:
						print 'turned correctly to the ' + last_direction
						if self.next_direction == 'straight':
							self.send_data('straight')
						else:
							self.send_data('turned')
						self.direction_list.pop(0)
					else:
						print 'turned incorrectly to the '+ last_direction +' !'
				# Return back to the normal state
				self.driving_state = 'normal'
				self.split_ratio = [0,0]
				self.back_on_track_count = 0
				r,sr = self.get_normal_ratio(left,top,right,current_layout,False)
				bs = max(self.minimum_speed,min(sr*self.minimum_speed,self.maximum_speed))
				self.last_ratio = r
				return self.to_speed(r,bs)

			else:
				ratio = self.get_split_ratio(left,top,right,current_layout,self.next_direction)
				self.split_ratio[0] += ratio
				self.split_ratio[1] += 1
				self.last_ratio = ratio
				return self.to_speed(ratio,self.turning_speed,True)

	def get_normal_ratio(self,left,top,right,current_layout,PID=False):
		if current_layout == None:
			if self.last_ratio != 0:
				return self.last_ratio,log(2./abs(self.last_ratio)**2,10)
			else:
				return self.last_ratio,1
		elif current_layout == 'normal_straight':
			ratio = self.to_ratio(mean_x(top))
			if DEBUG:
				print 'Original ratio: ',ratio
			if PID:
				ratio = self.normal_PID.value(ratio,1.)
				if DEBUG:
					print ' PID ratio: ',ratio
			if ratio != 0:
				speed_ratio = log(3./abs(ratio)**2,10)
				return ratio,speed_ratio
			else:
				return ratio,1
		elif current_layout == 'normal_left':
			ratio = self.to_ratio(mean_y(left))
			return ratio,1
		elif current_layout == 'normal_right':
			ratio = self.to_ratio(mean_y(right))
			return ratio,1
		else:
			raise Exception('POM')

	def get_normal_turning_ratio(self,left,top,right,current_layout):
		if current_layout == None:
			return self.last_ratio
		elif current_layout == 'normal_straight':
			ratio = self.to_ratio(mean_x(top))
			return ratio
		elif self.split_layout == 'normal_left':
			if current_layout in ['normal_left','T_left','crossroads','T_flat']:
				ratio = self.to_ratio(mean_y(left))
				return ratio
			else:
				return self.last_ratio
		elif self.split_layout == 'normal_right':
			if current_layout in ['normal_right','T_right','crossroads','T_flat']:
				ratio = self.to_ratio(mean_y(right))
				return ratio
			else:
				return self.last_ratio

	def get_split_ratio(self,left,top,right,layout,next_direction):
		if layout == None or (not is_special(layout)):
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
	def to_speed(self,ratio,basic_speed,split = False):
		# If ratio is bigger then one than left must drive a bigger distance then right
		if ratio >= 0:
			lspeed = basic_speed
			rspeed = (1.-ratio)*basic_speed
			# If the right speed is very low it must drive backward

			if (rspeed < self.turning_reversing_speed) and split:
				rspeed = (-1.)*self.minimum_speed
			elif (rspeed < self.turning_reversing_speed_2) and not split:
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
			if (lspeed < self.turning_reversing_speed) and split:
				lspeed = (-1.)*self.minimum_speed
			elif (lspeed < self.turning_reversing_speed_2 and not split):
				lspeed = (-1.)*self.minimum_speed
			# If the right speed is low it must drive the minimum speed
			elif (lspeed < self.minimum_speed):
				rspeed = self.minimum_speed/(1.+ratio)
				lspeed = self.minimum_speed
			return (lspeed,rspeed)

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
