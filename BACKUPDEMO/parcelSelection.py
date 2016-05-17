from sys import maxint
from findAllPaths import *
from pathFinding import *

def select_parcel(edges, vertices, position, parcels):
    chosenParcel = None
    for parcel in parcels:
        if parcel[1] == position[1]:
            return parcel
        parcel.append((find_all_paths(edges, vertices, parcel[1])).get(parcel[2]))
    for parcel in parcels:
        distanceTo = find_all_paths(edges, vertices, position[1])
        shortest_path = distanceTo.values()
        shortest_path_copy = distanceTo.values()
        distanceTo = distanceTo.items()
        #print 'distanceTo', distanceTo
        shortest_path.sort()
        shortest_path.pop(0)
        for x in range(len(shortest_path)):
            ind = shortest_path_copy.index(shortest_path[x])
            shortest_path[x] = shortest_path[x]*2.0
            for y in parcels:
                if parcel[1] == distanceTo[ind][0] and (chosenParcel == None or chosenParcel[-1] > (parcel[-1] + distanceTo[ind][1])):
                    chosenParcel = parcel
                    chosenParcel[-1] = chosenParcel[-1] + distanceTo[ind][1]
    if chosenParcel == None:
        return False
    return chosenParcel[0:3]

'''
map = {"vertices": [[1, {"origin": 3, "straight": 2, "left": 4}],[2, {"origin": 1, "straight": 3,"left": 4}],[3, {"origin": 2, "straight": 1, "left": 4}],[4, {"origin": 3, "straight": 1, "left": 2}]],"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5],[2, 3, 0.1],[3, 4, 0.7],[4, 2, 0.3],[4, 1, 0.8]]}

parcels = {"available-parcels": [[142, 1, 2],[145, 2, 3],[147, 2, 1],],"on-the-road-parcels": [[140,2, 4, "A-Team"]],"delivered-parcels": [[141, 1, 3, "B-Team"],[143, 3, 1, "B-Team"]]}

def get_edges():
        return map.get('edges')

def get_vertices():
        return map.get('vertices')

def generate_position():
        edges = get_edges()
        position = edges[random.randint(0,len(edges)-1)]
        return position

position = generate_position()
print(position)
a = select_parcel(get_edges(), get_vertices(), position, parcels.get('available-parcels'))
print a
'''
