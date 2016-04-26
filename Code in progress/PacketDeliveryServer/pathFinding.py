from sys import maxint

def find_path(vertices, edges, current, target):
    unvisited = {node[0]: maxint for node in vertices}
    visited = {}
    shortestPath = {}
    currentDistance = 0
    unvisited[current] = currentDistance
    if target not in unvisited:
        return None
    if current == target:
        return [current,target]

    while True:
        if current == target:
            path = [target]
            print 'short, ', shortestPath , ', target: ', target
            node = shortestPath[target]
            while True:
                path.insert(0, node)
                if node in shortestPath:
                    node = shortestPath[node]
                else:
                    break
            return path

        for x in range(len(edges) - 1, -1, -1):
            if edges[x][0] == current:
                neighbour = edges[x][1]
                distance = edges[x][2]
                if neighbour in unvisited:
                    newDistance = currentDistance + distance
                    if unvisited[neighbour] > newDistance:
                        unvisited[neighbour] = newDistance
                        shortestPath[neighbour] = current
                edges.pop(x)
        visited[current] = currentDistance
        del unvisited[current]
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]

