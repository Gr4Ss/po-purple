from findAllPaths import *
from parcelSelection import *
from pathFinding import *
from updateEdgesTraffic import *
# ------------------IMPORT sockets ------------------------
import os,sys,inspect
#first change the cwd to the script path
from restclient import *

class Packet_Delivery_Server:
    def __init__(self,start_position):
        self.teamname = 'Paars'
        self.restclient = RestClient("http://192.168.2.21:5000",self.teamname)
        self.restclient.add_team()
        self.map = self.restclient.get_map()
        #self.map = {"vertices": [[1, {"origin": 3, "straight": 2, "left": 4}],[2, {"origin": 1, "straight": 3,"left": 4}],[3, {"origin": 2, "straight": 1, "left": 4}],[4, {"origin": 3, "straight": 1, "left": 2}]],"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5],[2, 3, 0.1],[3, 4, 0.7],[4, 2, 0.3],[4, 1, 0.8]]}
        self.real_edges_lenght = generate_real_edges(self.map)
        self.current_position = start_position
        self.current_parcel = None
        self.parcel_picked_up = False
        self.split_from = None
        self.status = "Normal driving from %s to %s"%(self.current_position[0],self.current_position[0])
        self.socket = None

    def set_socket(self,socket):
        self.socket = socket
        self.socket.connect()
    '''
    Return the edges of the map
    '''
    def get_edges(self):
        return list(self.map.get('edges'))
    '''
    Return the vertices of the map
    '''
    def get_vertices(self):
        return list(self.map.get('vertices'))
    '''
        Method to send data to the webserver
    '''
    def send_data(self):
        data = {'Type':'Status','Position': self.current_position, 'Status':self.status, 'Parcel':self.current_parcel}
        if self.socket != None:
            if not self.socket.connected:
                self.socket.connect()
            self.socket.send_data(data)

    '''
    Method to update position of the car.
    Sends new position to rest server and update it locally
    '''
    def update_position(self,position):
        # Update at restserver
        self.restclient.update_position(int(position[0]),int(position[1]))
        # Update locally
        self.current_position = [int(position[0]),int(position[1])]
    '''
    Method to update the lenght of an edge. This is used as an estimate for the speed on a edge.
    '''
    def update_edge_length(self,edge,lenght):
        if edge in self.real_edges_lenght.keys():
            # For each edge we keep a list of distance so we can take the median
            self.real_edges_lenght[edge].append(lenght)
    '''
    Method that return the estimate of the distance of an edge.
    '''
    def get_edge_lenght(self,edge):
        # Determine the length of the edge
        lenght = len(self.real_edges_lenght[edge])
        # Get a sorted copy
        copy = sorted(self.real_edges_lenght[edge])
        # if no element return None
        if lenght == 0:
            return None
        # If even return the mean of the 2 middle elements of the sorted version
        elif lenght%2 == 0:
            return (copy[lenght/2 - 1] + copy[lenght/2])*0.5
        # If odd return the middle element of the sorted version
        else:
            return copy[lenght/2]
    '''
    Method called when the car is standing at a split. Return the
    direction (left,right,straight) that the car must turn at the
    split. The lenght input parameter lenght can be used to pass
    the lenght of the edge droven since the last call of at_split
    '''
    def at_split(self,lenght=None):
        # Update the length of the current edge
        if lenght != None:
            self.update_edge_length(self.current_position,lenght)
        # If the car has no parcel determine new one
        if self.current_position[0] == self.current_position[1]:
            self.current_position = (self.split_from,self.current_position[1])
        if self.current_parcel == None:
            self.new_parcel()
            if self.current_position[1] == self.current_parcel[1]:
                self.parcel_picked_up = True
                target = self.current_parcel[2]
            else:
                target = self.current_parcel[1]
            self.status = "New parcel selected. Driving to %s"%target
        # If we have a goal package but didn't pick it up
        elif self.parcel_picked_up == False and self.current_position[1] != self.current_parcel[1]:
            target = self.current_parcel[1]
            self.status = "Parcel not yet picked up. Driving to %s"%target
        elif self.parcel_picked_up == False:
            self.parcel_picked_up = True
            target = self.current_parcel[2]
            self.status = "Parcel picked up. Driving to %s"%target
        # A parcel is picked up, driving to target
        elif self.parcel_picked_up == True and self.current_position[1] != self.current_parcel[2]:
            target = self.current_parcel[2]
            self.status = "Parcel picked up. Driving to %s"%target
        else:
            self.deliver_parcel()
            self.new_parcel()
            if self.current_position[1] != self.current_parcel[1]:
                target = self.current_parcel[1]
                self.status = "Parcel delivered, new parcel selected. Now driving to %s"%target
            else:
                self.parcel_picked_up = True
                target  = self.current_parcel[2]
                self.status = "Parcel delivered, new parcel already picked up. Now driving to %s"%target
        self.split_from = self.current_position[0]
        self.update_position((self.current_position[1],self.current_position[1]))
        self.send_data()
        print self.new_direction(self.split_from,self.current_position[1],target)
        return self.new_direction(self.split_from,self.current_position[1],target)
    '''
        Method to call when the car has turned around.
    '''
    def turned_around(self):
        self.status = "Turned around now driving from %s to %s"%(self.current_position[1],self.current_position[0])
        # New position found by swapping the position elements
        self.update_position((self.current_position[1],self.current_position[0]))
        self.send_data()
    '''
        Method to check if the car can turn around given its current position
    '''
    def can_turn_around(self):
        # Return True if there there is an edge in the opposite direction
        for edge in self.get_edges():
            if edge[0] == self.current_position[1] and edge[1] == self.current_position[0]:
                return True
        return False
    '''
        Method to call when the car has turned at a split
    '''
    def turned(self,direction):
        new_target = self.to_node_number(self.current_position[1],self.split_from,direction)
        self.update_position((self.current_position[1],new_target))
        self.status = "Successfully turned. Now driving from %s to %s"%(self.current_position[0],self.current_position[1])
        self.send_data()
        return self.get_edge_lenght(self.current_position)
    '''
        Method that returns the new direction (left,right,straight) at a split
        frm : node where comming from
        current: node at which we must turned
        target: target node
    '''
    def new_direction(self,frm,current,target):

        positions = self.restclient.get_positions()
        edges = update_edges_traffic(positions,self.current_position,self.get_edges(),self.teamname)
        print self.get_vertices(),edges,current,target
        path = find_path(self.get_vertices(),edges,int(current),int(target))
        print path
        # You are comming from self.current_position[0] at node self.current_position[1] and to path[0]
        return self.to_left_right_straight(current,frm,path[1])
    '''
        Method to get new parcel
    '''
    def new_parcel(self):
        succes = False
        while not succes:
            available_parcels = self.restclient.get_parcels().get('available-parcels')
            positions = self.restclient.get_positions()
            print positions
            edges = update_edges_traffic(positions,self.current_position,self.get_edges(),self.teamname)
            parcel = select_parcel(edges, self.get_vertices(), self.current_position, available_parcels)
            if parcel != False:
                succes = self.restclient.claim_parcel(parcel[0])
            else:
                print "ERROR: Couldn't claim parcel"
        self.current_parcel = parcel
    '''
        Method to deliver parcels
    '''
    def deliver_parcel(self):
        self.restclient.deliver_parcel(self.current_parcel[0])
        self.current_parcel = None
        self.parcel_picked_up = False
    '''
        Method to get info about vertices
    '''
    def get_data_node(self,node):
        for vertice in self.get_vertices():
            print vertice[0],node
            if vertice[0] == node:
                return vertice[1]
        return None

    '''
    Method return 'left', 'right' or 'straight' if you are on the intersect at a given node
    and you are comming from a node and going to a given node.
    None is returned if the given combination is not possible
    eg.    |(1)|
           |   |
           |   |
    --------   ---------
    (3)     (4)       (5)
    ---------------------
    In this example the intersect is 4, and you are coming from 5 and you want to go to 1
    then right is returned/
    '''
    def to_left_right_straight(self,node,frm,to):
        # Example of vertices
        # {"vertices": [[1, {"origin": 3, "straight": 2, "left": 4}],
        #[2, {"origin": 1, "straight": 3,"left": 4}],
        #[3, {"origin": 2, "straight": 1, "left": 4}],
        # [4, {"origin": 3, "straight": 1, "left": 2}]],
        #"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5], ... ]}
        # You are already there no need for turning
        if node == to:
            return None

        directions = ["origin","right","straight","left"]
        node_data = self.get_data_node(node)
        for key in node_data:
            if int(node_data[key]) == int(frm):
                from_point = directions.index(key)
            if int(node_data[key]) == int(to):
                end_point = directions.index(key)
        return directions[(end_point-from_point)%len(directions)]
    def to_node_number(self,node,frm,to):
        directions = ["origin","right","straight","left"]
        node_data = self.get_data_node(node)
        for key,value in node_data.iteritems():
            if value == frm:
                from_direction = directions.index(key)
                break
        to_direction = (from_direction+directions.index(to))%len(directions)
        return node_data[directions[to_direction]]
def  generate_real_edges(mapje):
    edges = mapje["edges"]
    result = dict()
    for edge in edges:
        result[(edge[0],edge[1])] = []
    return result
