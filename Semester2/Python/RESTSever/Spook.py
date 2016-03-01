from restclient.py import all
from time import sleep
import random
from pathFinding.py import all
#root = serveradres

def generate_vehicle(teamname, speed):
    vehicle = Vehicle(root, teamname, speed)
    #while not vehicle.add_team():
	#sleep(0.1)
    vehicle.register()
    vehicle.drive()
    return vehicle

class Vehicle(RestClient):
    def __init__(self, root, teamname, speed):
        super(Vehicle, self).__init__(root, teamname)
	self.__speed = speed
	self.__parcelStatus == False

    def get_edges(self):
        roadMap = self.get_map()
        return roadMap.get('edges')

    def get_vertices(self):
        roadMap = self.get_map()
        return roadMap.get('vertices')

    def get_speed(self):
	return self.__speed    

    def generate_position(self):
        edges = self.get_edges()
        position = edges[random.randint(0,len(edges)-1)]
        return position

    def get_position(self):
        positions = (self.get_positions()).get('positions')
        for x in positions:
	    if x[0] == self.get_teamname():
	        return [x[1],x[2]]

    def choose_parcel(self):
        parcels = self.get_parcels()
        position = self.get_position()
        for x in parcels.get('on-the-road-parcels'):
            if x[3] == self.get_teamname():
	        return x
	for x in parcels.get('available-parcels'):
	    if x[2] == position[1]:
	        self.claim_parcel(x[0])
	        return x
	target = (parcels.get('available-parcels'))[-1]
	self.claim_parcel(target[0])
	return target
    
    def get_edge_length(self, edge):
	edges = self.get_edges
	for x in edges:
	    if x[0] == edge[0] and x[1] == edge[1]:
		return x[2]
	return 0

    def get_parcel_status(self):
	return self.__parcelStatus

    def inv_parcel_status(self):
	self.__parcelStatus = (self.__parcelStatus == False)
	pass

    '''def check_delivery(self):
        parcel = self.choose_parcel()
	if (parcel [1] in self.__lastVertices) and (parcel [2] in self.__lastVertices):
            x = self.deliver_parcel(parcel[0])
	    self.__lastVertices = list()
	    return x == 'OK'
    '''
    
    def confirm_delivery(self):
	parcel = self.choose_parcel()
	self.deliver_parcel(parcel[0])
	pass

    def pushposition(self,position):
	if type(position) != list:
	    self.update_position(position,position)
	else:
	    self.update_position(position[0],position[1])
        return 'OK'

    def register(self):
	while True:
	    if self.add_team(): break
        position = self.generate_position()
	self.pushposition(position)
	parcel = self.choose_parcel()
	return 'OK'

    def update_edges_traffic(self):
	positions = (self.get_positions()).get('positions')
	position = self.get_position()
	edges = self.get_edges()
	for x in positions:
	    if x[0] != self.get_teamname():
		if x[2] == position[0]:
		    edge = [x[2], x[1], self.get_edge_length([x[2], x[1]])]
		    if edges.count(edge) != 0:
		        edges.remove(edge)
		if x[1] == position[0]:
		    i = edges.index([x[1], x[2], self.get_edge_length([x[2], x[1]])])
		    edge = edges.pop(i)
		    edge[2] = edge[2]*2
		    edges.insert(i, edge)
	return edges
    
    def drive(self):
	while True
    	    parcel = self.choose_parcel()
	    position = self.get_position()
	    length = self.get_edge_length(position)
	    if self.get_parcel_status():
	        target = parcel[1]
    	    else:
	        target = parcel[2]
	    time.sleep(length/self.get_speed())
	    self.pushposition(position[1])
	    if position[1] == target:
    	        if self.get_parcel_status():
	            self.inv_parcel_status()
	            self.confirm_delivery()
	        else if not self.get_parcel_status():
		    self.inv_parcel_status()
	        continue
	    path = find_path(self.get_vertices(), self.update_edges_traffic(), position[1], target)
	    self.pushposition(path[0],path[1])
{
"available-parcels": [
[142, 1, 2],
[145, 2, 3],
[147, 2, 1],
],
"on-the-road-parcels": [
[140, 2, 4, "A-Team"]
],
"delivered-parcels": [
[141, 1, 3, "B-Team"],
[143, 3, 1, "B-Team"]
]
}

{
"positions": [
["A-Team", 1, 2],
["B-Team", 3, 3]
]
}
'''


