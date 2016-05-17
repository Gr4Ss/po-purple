def update_edges_traffic(positions,own_position,edges,teamname):
      for pos in positions:
          if pos[0] != teamname and pos[1] != pos[2]:
              if pos[2] == own_position[0]:
                  edge = [x[2], x[1], get_edge_length([x[2], x[1]],edges)]
                  if edges.count(edge) != 0:
                      edges.remove(edge)
                      continue
          if pos[1] == own_position[0] and pos[1] != pos[2]:
              try:
                  i = edges.index([x[1], x[2],get_edge_length([x[1], x[2]], edges)])
                  edge = edges.pop(i)
                  edge[2] = edge[2]*2
                  edges.insert(i, edge)
              except:
                  pass
      return edges
def get_edge_length(edge, edges):
    for x in edges:
        if x[0] == edge[0] and x[1] == edge[1]:
            return x[2]
    return 0
