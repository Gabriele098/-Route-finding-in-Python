import logging
import csv

class LaneJunction:
    """
    This Junction for Lanes for DLL
    either a staion with one lane towards a station with more lanes
    or a station with multiple lanes towards a station to multiple lanes
    """

    def __init__(self):
        self.stations = []

    def add_station(self, station):
        """
                Adds next station
                """
        if isinstance(station, StationNode):
            self.stations.append(station)
        else:
            raise TypeError("Must be StationNode object")


class UnderGroundMapGraph:
    """
    Holds the Map of the Whole underground Map.
    """

    def __init__(self, name):
        self.name = name
        self.connections = set()
        self.next_stations = []
        self.prev_stations = []

    def add_connection(self, lane_name):
        self.connections.add(lane_name)

    def add_to_next_stations(self, station):
        """
        Adds next station
        """
        if isinstance(station, StationNode):
            self.next_stations.append(station)
            if not station.station :
                station.station = self  # ref back to station object
        else:
            raise TypeError("Must be StationNode object")

    def add_to_prev_stations(self, station):
        """
        Add station as previous station
        """
        if isinstance(station, StationNode):
            self.prev_stations.append(station)
        else:
            raise TypeError("Must be StationNode object")

    def __repr__(self):
        # all_lanes = " , ".join(set(list(self.next_stations.keys()) + list(self.prev_stations.keys())))
        all_lanes = ", ".join(self.connections)
        return f"Station: {self.name}" \
               f"\n\t\t-Connections:({all_lanes}) \n"


class StationNode:
    def __init__(self, name, u_map):
        self.name = name
        self.connections = []
        self.next_station = None
        self.prev_station = None
        self.station = None  # For string the ref to station Object

        self.timing_using_hashtable = {}  # if the next or previous station contain
        # junction, the timings are stored in the hash table

        # store counts of stations added, transform into junction lane
        self.prev_station_count = 0
        self.next_station_count = 0

        self.lane = u_map.lane_name
        self.u_map = u_map  # ref to original obj

    def get_station_by_name(self, name):
        """
        Searches next and previous and next for given name
        """
        for station in self.timing_using_hashtable.keys():
            if station.name == name:
                return station
        return None

    def add_next_sation(self, station, travel_time):
        """
        Adds next station
        """
        if isinstance(station, StationNode):
            self.next_station = station
            self.timing_using_hashtable[station] = travel_time
            return True
        else:
            raise TypeError("Must be StationNode object")

    def add_prev_sation(self, station, travel_time):
        """
        Add station as prev station
        """
        if isinstance(station, StationNode):
            self.prev_station = station
            self.timing_using_hashtable[station] = travel_time
            return True
        else:
            raise TypeError("Must be StationNode object")

    def __repr__(self):
        return f"<StationNode<{self.name}>>"


class DoubleLinkedLondonTrainLane:
    def __init__(self, name):
        # these handy to keep track start and end of the map
        self.first_node = None
        self.last_node = None
        self.len = 0  # total number of stations
        self.lane_name = name

        # This this reduce the search time to linear search
        self.all_stations = []

    def add_next_station_to_station(self, station_name, next_station_name, travel_time):
        """
        Adds a next station to a station
        Args:
            station_name (str): station Name
            next_station_name (str): Traveling to station
            travel_time (int): travel time
        Raises:
            LookupError: when station is not found in the DLL
        """
        cur_staion = self.get_the_station(station_name)
        next_station = self.get_the_station(next_station_name)
        if not cur_staion or not next_station:
            logging.debug(
                f"{next_station_name if not cur_staion else cur_staion} is not found in list- Add it to the list")
        else:
            cur_staion.next_station = next_station  # seting the next station obj
            cur_staion.timing_using_hashtable[next_station] = float(travel_time)

    def add_prev_station(self, station_name, prev_station_name, travel_time):
        """
        Adds a previous station to a station
        Args:
            station_name (str): station Name
            next_station_name (str): Traveling to station
            travel_time (int): travel time
        Raises:
            LookupError: when station is not found in the DLL
        """
        cur_staion = self.get_the_station(station_name)
        prev_station = self.get_the_station(prev_station_name)
        if not cur_staion or not prev_station:
            logging.debug(
                f"{prev_station_name if not cur_staion else cur_staion} is not found in list- Add it to the list")
        else:
            cur_staion.prev_station = prev_station  # seting the prev station obj
            cur_staion.timing_using_hashtable[prev_station] = float(travel_time)

    def append_station(self, name):
        node = StationNode(name, self)  # creates a new station
        # node.prev_station = self.last_node
        self.all_stations.append(node)
        self.last_node = node  # any new station added as the fist station
        if self.first_node is None:  # Updates the first node to the current list
            self.first_node = node
        self.len += 1
        return node

    def make_bidirectional_connection(self, station_from, station_to, travel_time):
        """[summary]
            eg station_from <=> Stratford station_to <=>  West Ham
            station_from ([type]): [description]
            station_to ([type]): [description]
            travel_time ([type]): [description]
        """

        # The station is not in the DLL then add it
        from_station_node = self.get_the_station(station_from)
        station_to_node = self.get_the_station(station_to)

        # Create nodes if not exist
        if not from_station_node:
            from_station_node = self.append_station(station_from)
        if not station_to_node:
            station_to_node = self.append_station(station_to)

        if from_station_node.next_station_count >= 1 or station_to_node.prev_station_count >= 1:
            if from_station_node.next_station_count >= 1:
                if not isinstance(from_station_node.next_station, LaneJunction):
                    # create new junction
                    junctions = LaneJunction()
                    junctions.add_station(from_station_node.next_station)  # previously added node

                    from_station_node.add_next_sation(station_to_node, float(travel_time))  # new node
                    junctions.add_station(from_station_node.next_station)

                    # assign junction
                    from_station_node.next_station = junctions
                else:
                    # append the to the station
                    from_station_node.next_station.add_station(station_to_node)
                    from_station_node.timing_using_hashtable[station_to_node] = float(travel_time)
            else:
                from_station_node.add_next_sation(station_to_node, float(travel_time))

            if station_to_node.prev_station_count >= 1:
                if not isinstance(station_to_node.prev_station, LaneJunction):
                    # create new juncton
                    junctions = LaneJunction()
                    junctions.add_station(station_to_node.prev_station)  # previously added node

                    station_to_node.add_prev_sation(from_station_node, float(travel_time))  # new node
                    junctions.add_station(station_to_node.prev_station)

                    # assign junction
                    station_to_node.prev_station = junctions
                else:
                    # append the to the station
                    station_to_node.prev_station.add_station(from_station_node)
                    station_to_node.timing_using_hashtable[from_station_node] = float(travel_time)
            else:
                station_to_node.add_prev_sation(from_station_node, float(travel_time))

        else:
            from_station_node.add_next_sation(station_to_node, float(travel_time))
            station_to_node.add_prev_sation(from_station_node, float(travel_time))

        from_station_node.next_station_count += 1  # add the count
        station_to_node.prev_station_count += 1

    def get_the_station(self, name):
        # Finds the station from the map by going through the list
        if name:
            for station in self.all_stations:
                if station.name == name:
                    return station

            return None  # It's Not in the doubly linked list

    def check_station_exist(self, name):
        """
        Checks if station already in the linked list
        Returns:
            Bool: True/False
        """
        if name:
            curr = self.first_node
            for j in range(self.len):
                if curr.name == name:
                    return True
                curr = curr.next_station
        return False


    def __repr__(self):
        # [ j.name  for j in range(self.len)
        # pass
        return f'Lane: {self.lane_name}\n\t\tNumber of stations: {self.len}\n\t\t' \
               f'First station: {self.first_node}\n\t\tLast station: {self.last_node}\n'



    """
    Execute the section below to test the doubly-linked-list,
    which will print every single lane with its stations, 
    first station and last station
    """

'''
def read_csv(name):
    content = None
    with open(name, "r", encoding="utf-8-sig") as f:
        content = list(csv.DictReader(f))
    return content

# testing the Doubly linked class
if __name__ == "__main__":
    all_station = read_csv("Stations.csv")
    lane_dll = {}

    for station in all_station:
        lane = station["Lane"]
        if station["Lane"] not in lane_dll:
            station_name = station["Station"]
            lane_dll[lane] = DoubleLinkedLondonTrainLane(lane)
        lane_dll[lane].append_station(station["Station"])
    print(lane_dll)
'''
