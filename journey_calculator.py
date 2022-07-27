from dijkstra import mydijkstra
from doubly_linked_list import UnderGroundMapGraph, DoubleLinkedLondonTrainLane, LaneJunction
import csv
import logging

class Journey(object):
    def __init__(self, station_from, station_to, time):
        self.station_from = station_from
        self.station_to = station_to
        self.time = time

    def read_csv(self, name):
        content = None
        with open(name, 'r', encoding='utf-8-sig') as f:
            content = list(csv.DictReader(f))
        return content

    def print_journey(self, journey):
        total_travel_time = 0
        total_nodes = len(journey)

        # Arrays that contain information about the journey route
        # and the summary of it, which will be used put data in the table in GUI part
        journey_route = []
        changes = []

        for i in range(total_nodes):
            lane_node = journey[i]
            lane_node_from = journey[i][0]
            lane_node_to = journey[i][1]
            travel_time = lane_node[0].timing_using_hashtable[lane_node[1]]
            total_travel_time += (travel_time + 1)  # adding 1 minute at each station(stop)
            if i == 0:
                journey_route.append([lane_node_to.lane, lane_node[0].name, 'Start', [0, 'min']])
                journey_route.append([lane_node_from.lane, lane_node_to.name, [travel_time, 'min'],
                                      [total_travel_time, 'min']])
            else:
                journey_route.append([lane_node_from.lane, lane_node_to.name, [travel_time, 'min'],
                                      [total_travel_time, 'min']])
            if i == total_nodes-1:
                journey_route.append([lane_node_to.lane, lane_node_to.name, 'End', [total_travel_time, 'min']])

        for i, j in enumerate(journey[:-1]):
            if i >= 0:
                if journey[i+1][0] != journey[i][1]:
                    changes.append(["In " + journey[i+1][0].name, "Change to " + journey[i+1][1].lane + " line"])
        return journey_route, total_travel_time, changes


    def station_graph(self):
        all_station = self.read_csv("Stations.csv")
        station_timings = self.read_csv("StationWithTimings.csv")
        station_graph_map = {}  # stores data of the whole underground map
        lane_DLL = {}  # stores data of each lane

        for station in all_station:  # Reading all the station and turning Double Linked Object
            lane = station["Lane"]
            if station["Lane"] not in lane_DLL:
                station_name = station["Station"]
                lane_DLL[lane] = DoubleLinkedLondonTrainLane(lane)
            lane_DLL[lane].append_station(station["Station"])

        # splitting the data of StationWithTimings.csv using headers for each column
        # e.g. Lane  StationFrom  StationTo  Time
        for st_timing in station_timings:  # adding the timings to the station
            lane = st_timing['Lane']
            station_from = st_timing['StationFrom']
            station_to = st_timing['StationTo']
            travel_time = float(st_timing['Time'])

            if lane == 'Bakerloo':
                if 9 <= self.time < 16 or 19 <= self.time <= 23:
                    travel_time /= 2

            # if data exist
            if station_from and station_to and travel_time and st_timing['Lane']:
                lane_DLL[lane].make_bidirectional_connection(station_from,
                                                             station_to, travel_time)
            else:
                logging.debug(f"Missing Info from: {station_from} "
                              f"TO: {station_to} TIMING: {travel_time} LANE: {station['Lane']}")

        # Turning DLL into Graph map with bidirectional using DLL for each lane
        for lane, dll in lane_DLL.items():
            for station in dll.all_stations:
                station_name = station.name
                next_station = station.next_station
                prev_station = station.prev_station

                station_in_graph = station_graph_map.get(station_name, None)
                if not station_in_graph:
                    station_graph_map[station_name] = UnderGroundMapGraph(
                        station_name)
                    station_in_graph = station_graph_map[station_name]

                if next_station:
                    if isinstance(next_station, LaneJunction):
                        [station_in_graph.add_to_next_stations(s) for s in next_station.stations]
                    else:
                        station_in_graph.add_to_next_stations(
                            next_station)
                if prev_station:
                    if isinstance(prev_station, LaneJunction):
                        [station_in_graph.add_to_prev_stations(s) for s in prev_station.stations]
                    else:
                        station_in_graph.add_to_prev_stations(
                            prev_station)
                station_in_graph.connections.add(lane)

        return station_graph_map

    def calculate_journey(self):
        station_graph_map = self.station_graph()
        journeys = [[self.station_from, self.station_to]]
        summary = []
        for from_s, to_s in journeys:
            summary.append(['Start station', from_s])
            summary.append(['Destination', to_s])
            total_timing, traveling_nodes = mydijkstra(station_graph_map, from_s, to_s)
            route, total_time, changes = self.print_journey(traveling_nodes)
            changes.append(['Total timing', [total_time, 'min']])
            changes.append(['Total time without\nwaiting(min)', [total_timing, 'min']])

        return route, summary, changes

