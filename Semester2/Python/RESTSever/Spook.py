import restclient.py
from time import sleep
from random import randint
#root = serveradres

def generate_vehicle(teamname, speed):
    vehicle = RestClient(root, teamname)
    while not vehicle.add_team():
	sleep(0.1)
    return vehicle

class Vehicle(RestClient):
    def __init__(self, root, teamname):
        super(Vehicle, self).__init__(root, teamname)
        self.__lastVertices = list()

    def get_edges(self):
        roadMap = self.get_map()
        return roadMap.get('edges')
	
    def get_vertices(self):
        roadMap = self.get_map()
        return roadMap.get('vertices')

    def generate_position(self):
        edges = self.get_edges()
        position = edges[randint(0,len(edges)-1)]
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

    def check_delivery(self):
        parcel = self.choose_parcel()
	if (parcel [1] in self.__lastVertices) and (parcel [2] in self.__lastVertices):
            x = self.deliver_parcel(parcel[0])
	    self.__lastVertices = list()
	    return x == 'OK'

    def pushposition():
	## self.update_position implementeren!
	## self.__lastVertices.append(currentNode)

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
