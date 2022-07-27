import csv

def read_csv(name):
    content = None
    with open(name, "r", encoding="utf-8-sig") as f:
        content = list(csv.DictReader(f))
    return content


all_station = read_csv("Stations.csv")
stations = []
for station in all_station:
    stations.append(station["Station"])

stations.sort()
all_stations = set(stations)

