from collections import deque
import time
import sys
import heapq
from math import pi, acos, sin, cos

node_location = {}
with open("rrNodes.txt") as f:
    for line in f:
        arguments = line.strip().split(" ")
        node_location[arguments[0]] = [arguments[1], arguments[2]]

majorcity_id = {}
with open("rrNodeCity.txt") as f:
    for l in f:
        line = l.strip()
        space_index = line.find(" ")
        majorcity_id[line[space_index + 1:len(line)].strip()] = line[0:space_index].strip()


def calcd(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions
    if y1 == y2 and x1 == x2:
        return 0

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    r = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * r


# dist = calcd(39.830480, -86.126170, 39.830480, -86.126170)
# print(dist)
start_time = time.perf_counter()
junctions = {}
with open("rrEdges.txt") as f:
    for line in f:
        arguments = line.strip().split(" ")
        first_city = arguments[0]
        second_city = arguments[1]
        distance = calcd((node_location[first_city])[0], (node_location[first_city])[1],
                         (node_location[second_city])[0],
                         (node_location[second_city])[1])
        if first_city in junctions.keys():
            (junctions[first_city])[second_city] = distance
        else:
            junctions[first_city] = {second_city: distance}
        if second_city in junctions.keys():
            (junctions[second_city])[first_city] = distance
        else:
            junctions[second_city] = {first_city: distance}
end_time = time.perf_counter()
total_time = end_time - start_time


def heuristic(train1, train2):
    return calcd(node_location[train1][0], node_location[train1][1], node_location[train2][0], node_location[train2][1])


def goal(train1, train2):
    if train1 == train2:
        return True
    return False


def get_children(train):
    children = list(junctions[train].keys())
    return children


def a_star(start, end):
    end_id = majorcity_id[end]
    start_id = majorcity_id[start]
    d = {}
    closed = set()
    d[start_id] = (0, start_id, 0)
    fringe = [(0, start_id, 0)]
    heapq.heapify(fringe)
    while len(fringe) > 0:
        v = heapq.heappop(fringe)
        if goal(v[1], end_id):
            return v[2]
        if v[1] not in closed:
            closed.add(v[1])
            children = get_children(v[1])
            for child in children:
                c = d.get(child)
                if c is None or c[2] > v[2]:
                    c = tuple()
                    depth = v[2] + (junctions[v[1]])[child]
                    c = (depth + heuristic(child, end_id), child, depth)
                    d[child] = c
                    heapq.heappush(fringe, c)

    return None


def dijkstra(start, end):
    end_id = majorcity_id[end]
    start_id = majorcity_id[start]
    d = {}
    closed = set()
    d[start_id] = (0, start_id)
    fringe = [(0, start_id)]
    heapq.heapify(fringe)
    while len(fringe) > 0:
        v = heapq.heappop(fringe)
        if goal(v[1], end_id):
            return v[0]
        if v[1] not in closed:
            closed.add(v[1])
            children = get_children(v[1])
            for child in children:
                c = d.get(child)
                if c is None or c[0] > v[0]:
                    c = tuple()
                    depth = v[0] + (junctions[v[1]])[child]
                    c = (depth, child)
                    d[child] = c
                    heapq.heappush(fringe, c)


if len(sys.argv) > 3:
    my_first_city = sys.argv[1] + " " + sys.argv[2]
    my_second_city = sys.argv[3]
else:
    my_first_city = sys.argv[1]
    my_second_city = sys.argv[2]

print("Time to create data structure:", total_time)

start_time = time.perf_counter()
dist = dijkstra(my_first_city, my_second_city)
end_time = time.perf_counter()
total_time = end_time - start_time
print(my_first_city, "to", my_second_city, "with Dijkstra:", dist, "in", total_time, "seconds")

start_time = time.perf_counter()
dist = a_star(my_first_city, my_second_city)
end_time = time.perf_counter()
total_time = end_time - start_time
print(my_first_city, "to", my_second_city, "with A*:", dist, "in", total_time, "seconds")