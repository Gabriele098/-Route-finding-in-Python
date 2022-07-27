import logging
from collections import deque
from doubly_linked_list import LaneJunction

def get_path_two_station(from_s, to_s):
    next_and_prev_stations = from_s.next_stations + from_s.prev_stations
    found = []
    smallest_time = None
    for station in next_and_prev_stations:
        if station.name == to_s.name:
            found.append([station.get_station_by_name(from_s.name), station])

    if len(found) >= 2:
        # gets the lane with the shortest travel time
        shortest_time = min(found, key=lambda s: s[0].timing_using_hashtable[s[1]])
        return shortest_time
    else:
        return found[0]


def mydijkstra(graph, start, end):
    # Distances of each from the start node, distance from the start station is zero
    distance_from_start = {
        node: (float('inf') if node != start else 0) for node in graph
    }

    # unexplored nodes
    unvisited_nodes = list(set(graph.keys()))

    # set the predecessor for that node
    predecessors = {node: None for node in graph}
    predecessorsobj = {}
    for stn in graph.values():
        next_and_prev_stations = stn.next_stations + stn.prev_stations
        found = []
        for station in next_and_prev_stations:
            predecessorsobj[station] = None

    # predecessors = {}
    previous_lowest_node = None
    while unvisited_nodes:
        node_with_lowest_d = min(unvisited_nodes,
                                 key=lambda node: distance_from_start[node])

        unvisited_nodes.remove(node_with_lowest_d)

        current_station = graph[node_with_lowest_d]

        next_and_prev_stations = [[current_station.next_stations],
                                  [current_station.prev_stations]]

        for i in range(2):
            for node in next_and_prev_stations[i][0]:
                travel_time = None
                if i == 0:
                    # In order to get the time to next station you have travel
                    # to previous node to the current lane
                    lane_node = node.prev_station
                    if lane_node:
                        if isinstance(lane_node, LaneJunction):
                            for node_current_vertex in lane_node.stations:
                                if node_current_vertex.name == current_station.name:
                                    lane_node = node_current_vertex
                        travel_time = lane_node.timing_using_hashtable[node]

                if i == 1:
                    # In order to get the time to the previous station you have traveled
                    # to next node to the current lane
                    lane_node = node.next_station
                    if lane_node:
                        if isinstance(lane_node, LaneJunction):
                            for node_current_vertex in lane_node.stations:
                                if node_current_vertex.name == current_station.name:
                                    lane_node = node_current_vertex
                        travel_time = lane_node.timing_using_hashtable[node]

                if travel_time:
                    # check total distance is less than on one we have of all the nighbour nodes
                    if distance_from_start[node_with_lowest_d] + \
                            travel_time < distance_from_start[node.name]:
                        # update the distance with
                        # that shorter distance
                        distance_from_start[node.name] = distance_from_start[node_with_lowest_d] + \
                                               travel_time
                        predecessors[node.name] = node_with_lowest_d
                        previous_lowest_node = node

                else:
                    logging.debug(f"Missing Time  {node} {i} >>> FROM: {current_station}")
        if node_with_lowest_d == end:
            break

    # back tracking to print out the path from the end Node.
    path = deque()
    current_node = end
    while predecessors[current_node] is not None:
        path.appendleft(current_node)
        current_node = predecessors[current_node]

    path.appendleft(start)
    all_node_obj = []
    total_paths = len(path)
    for i in range(total_paths-1):
        if total_paths == total_paths-2:
            break
        all_node_obj.append(get_path_two_station(graph[path[i]], graph[path[i+1]]))

    return distance_from_start[end], all_node_obj
