import math

def generate_adjacent_building_sets(city_matrix):
    building_sets = []
    visited = set()
    for i in range(0,len(city_matrix)):
        for j in range(0,len(city_matrix[0])):
            if city_matrix[i][j] == '#' and (i, j) not in visited:
                adjacent_buildings = {(i, j)}
                visited.add((i, j))
                queue = [(i, j)]
                while queue:
                    x, y = queue.pop(0)
                    for dx, dy in  [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(city_matrix) and 0 <= ny < len(city_matrix[0]) and city_matrix[nx][ny] == '#' and (nx, ny) not in visited:
                            adjacent_buildings.add((nx, ny))
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                building_sets.append(adjacent_buildings)
    return building_sets

def bridge_distance(p1, p2):
    if p1[0] == p2[0]:
        # Points are in the same row
        length = abs(p1[1] - p2[1])-1
    elif p1[1] == p2[1]:
        # Points are in the same column
        length = abs(p1[0] - p2[0])
    else:
        # Points are not in the same row or column
        length = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) - 2
    return length

def find_distances(set1, set2):
    distances = []
    for p1 in set1:
        for p2 in set2:
            # exclude points in the same row or column or neighboring rows/columns
            if (p1[0] == p2[0] or p1[1] == p2[1] or abs(p1[0]-p2[0]) == 1 or abs(p1[1]-p2[1]) == 1):
                distances.append((p1, p2, bridge_distance(p1, p2)))
    return distances

def bridges(building_sets):
    bridges = []
    for i in range(len(building_sets)):
        for j in range(i+1, len(building_sets)):
            distances = find_distances(building_sets[i], building_sets[j])
            if distances:
                bridges.extend(distances)
    return bridges

def is_closed_curve(edges, start_node, current_node, visited, parent):
    visited.add(current_node)
    for edge in edges:
        if current_node in edge:
            neighbor = edge[0] if edge[0] != current_node else edge[1]
            if neighbor == start_node and neighbor != parent:
                return True
            if neighbor not in visited:
                if is_closed_curve(edges, start_node, neighbor, visited, current_node):
                    return True
    return False

def minimum_spanning_tree(building_sets, bridges):
    edges = []
    # create a set for each building set
    sets = [set(building_set) for building_set in building_sets]
    # sort the bridges by length
    bridges = sorted(bridges, key=lambda x: x[2])
    for bridge in bridges:
        start_building_set, end_building_set, length = bridge
        # find the sets that contain the start and end building
        for index, building_set in enumerate(sets):
            if start_building_set in building_set:
                start_index = index
            if end_building_set in building_set:
                end_index = index
        # if the start and end building are in different sets
        if start_index != end_index:
            # add the bridge to the edges list
            edges.append(bridge)
            # merge the sets
            sets[start_index] = sets[start_index].union(sets[end_index])
            sets.pop(end_index)
            # if all sets have been merged, stop searching for bridges
            if len(sets) == 1:
                break
    return edges


def output_result(city_num, adj_bldgs , conectd_bldgs):
    print("City {}".format(city_num))
    if len(conectd_bldgs) == 0:
        if len(adj_bldgs) == 1:
            print("\nNo bridges are needed.")
        else:
            print("\nNo bridges are possible.")
            print("\n{} disconnected groups.".format(len(adj_bldgs)))
    else:
        if len(conectd_bldgs) == 1:
            bridge = "bridge"
        else:
            bridge = "bridges"
            bridge_length = sum(brd[2] for brd in conectd_bldgs)
            print("\n{} {} of total length {}".format(len(conectd_bldgs) , bridge, bridge_length))
            disconnected_grps=len(adj_bldgs)-len(conectd_bldgs)-1
            if disconnected_grps != 0 :
              print("{} disconnected groups".format( len(adj_bldgs)-len(conectd_bldgs) ))


def main():
  import numpy as np
  cities=[]
  while(True):
    print("enter rows and coloumns:")
    r, c = map(int, input().split())
    if(r | c == 0 ):
      break
    city=np.zeros((r,c),str)
    for i in range (r):
      city[i]=[i for i in input()]
    cities.append(city)

  for i in range(len(cities)):
        adj_bldg= generate_adjacent_building_sets(cities[i])
        brdg= bridges(adj_bldg)
        conectd_bldg=minimum_spanning_tree(adj_bldg,brdg)
        print(len(conectd_bldg))
        output_result(i+1 , adj_bldg , conectd_bldg)

main()
