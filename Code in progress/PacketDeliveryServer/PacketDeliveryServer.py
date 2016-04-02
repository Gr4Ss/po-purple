from findAllPaths import *
from parcelSelection import *
from pathFinding import *
# ------------------IMPORT sockets ------------------------
import os,sys,inspect
#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../RESTServer")
from restclient import *

class PacketDeliveryServer:
    def __init__(self,start_position):
        self.restclient = RestClient("http://localhost:9000")
        self.map = self.restclient.get_map()
        #self.map = {"vertices": [[1, {"origin": 3, "straight": 2, "left": 4}],[2, {"origin": 1, "straight": 3,"left": 4}],[3, {"origin": 2, "straight": 1, "left": 4}],[4, {"origin": 3, "straight": 1, "left": 2}]],"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5],[2, 3, 0.1],[3, 4, 0.7],[4, 2, 0.3],[4, 1, 0.8]]}
        self.current_position = start_position
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
    def to_left_right_straight(self,node,From,To):
        # Example of vertices
        # {"vertices": [[1, {"origin": 3, "straight": 2, "left": 4}],
        #[2, {"origin": 1, "straight": 3,"left": 4}],
        #[3, {"origin": 2, "straight": 1, "left": 4}],
        # [4, {"origin": 3, "straight": 1, "left": 2}]],
        #"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5], ... ]}
        # First of all loop through the vertices to find the right data
        directions = ["origin","right","straight","left"]
        for vertice in self.map["vertices"]:
            if vertice[0] == node:
                node_data = vertice[1]
        for key in node_data:
            if node_data[key] == From:
                from_point = directions.index(key)
            elif node_data[key] == To:
                end_point = directions.index(key)
        return directions[(end_point-from_point)%len(directions)]
test = PacketDeliveryServer((1,2))
print test.to_left_right_straight(4,1,2),'right'
print test.to_left_right_straight(1,4,2),'left'
print test.to_left_right_straight(2,3,1),'straight'
print test.to_left_right_straight(2,3,4),'right'
