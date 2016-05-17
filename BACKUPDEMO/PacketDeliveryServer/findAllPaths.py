import random
from sys import maxint
# Return distance to all nodes using Dijkstra's algorithm
def find_all_paths(edges, vertices, current):
    unvisited = {node[0]: maxint for node in vertices}
    visited = {}
    currentDistance = 0
    unvisited[current] = currentDistance
    while True:
        for x in range(len(edges) - 1, -1, -1):
            if edges[x][0] == current:
                neighbour = edges[x][1]
                distance = edges[x][2]
                if neighbour not in unvisited: continue
                newDistance = currentDistance + distance
                if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                    unvisited[neighbour] = newDistance
        visited[current] = currentDistance
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]
    return(visited)
'''
map = {"vertices": [[1, {"origin": 3, "straight": 2, "left": 4}],[2, {"origin": 1, "straight": 3,"left": 4}],[3, {"origin": 2, "straight": 1, "left": 4}],[4, {"origin": 3, "straight": 1, "left": 2}]],"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5],[2, 3, 0.1],[3, 4, 0.7],[4, 2, 0.3],[4, 1, 0.8]]}

def get_edges():
        return map.get('edges')

def get_vertices():
        return map.get('vertices')

def generate_position():
        vertices = get_vertices()
        position = vertices[random.randint(0,len(vertices)-1)]
        return position[0]

current = generate_position()
target = generate_position()
print(current, target)
print(find_all_paths(get_edges(), get_vertices(), current))
'''
