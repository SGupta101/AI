import time
import sys
import heapq
from math import pi, acos, sin, cos
from tkinter import *

node_location = {}
with open("rrNodes.txt") as f:
    for line in f:
        arguments = line.strip().split(" ")
        node_location[arguments[0]] = [float(arguments[1]), float(arguments[2])]

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
    my_count = 0
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
                    my_count += 1
                    refresh(v[1], child, my_count)
                    if my_count == 200:
                        my_count = 0

    return None


def dijkstra(start, end):
    my_count = 0
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
                    my_count += 1
                    refresh_d(v[1], child, my_count)
                    if my_count == 2000:
                        my_count = 0


# print("Time to create data structure:", total_time)
#
# start_time = time.perf_counter()
# dist = dijkstra(my_first_city, my_second_city)
# end_time = time.perf_counter()
# total_time = end_time - start_time
# print(my_first_city, "to", my_second_city, "with Dijkstra:", dist, "in", total_time, "seconds")
#
# start_time = time.perf_counter()
# dist = a_star(my_first_city, my_second_city)
# end_time = time.perf_counter()
# total_time = end_time - start_time
# print(my_first_city, "to", my_second_city, "with A*:", dist, "in", total_time, "seconds")
max_x = 0
max_y = 0
min_x = 10000
min_y = 10000
for node in node_location:
    max_x = max(abs(node_location[node][1]), max_x)
    max_y = max(node_location[node][0], max_y)
    min_x = min(abs(node_location[node][1]), min_x)
    min_y = min(node_location[node][0], min_y)
x_scale = (max_x - min_x) / 1200
y_scale = (max_y - min_y) / 700

min_x = min_x / x_scale
min_y = min_y / y_scale


def scaled(x, y):
    new_x = (x / x_scale) + min_x
    new_x = 1200 - abs(new_x) + 50
    new_y = (y / y_scale) - min_y
    new_y = new_y + 50
    new_y = abs(new_y - 700) + 50
    return [new_x, new_y]


def refresh(first, second, count):
    fir = scaled(node_location[first][1], node_location[first][0])
    s = scaled(node_location[second][1], node_location[second][0])
    my_canvas.create_line(fir[0], fir[1], s[0], s[1],
                          width=2, fill="red")
    if count == 200:
        my_window.update_idletasks()
        my_window.update()


def refresh_d(first, second, count):
    fir = scaled(node_location[first][1], node_location[first][0])
    s = scaled(node_location[second][1], node_location[second][0])
    my_canvas.create_line(fir[0], fir[1], s[0], s[1],
                          width=2, fill="green")
    if count == 2000:
        my_window.update_idletasks()
        my_window.update()


my_window = Tk()
my_canvas = Canvas(my_window, width=1300, height=800, bg="white")
my_canvas.grid(row=0, column=0)
for node in junctions:
    for node2 in junctions[node].keys():
        first_xy = scaled(node_location[node][1], node_location[node][0])
        second_xy = scaled(node_location[node2][1], node_location[node2][0])
        my_canvas.create_line(first_xy[0], first_xy[1], second_xy[0], second_xy[1],
                              width=2, fill="black")

if len(sys.argv) > 3:
    my_first_city = sys.argv[1] + " " + sys.argv[2]
    my_second_city = sys.argv[3]
else:
    my_first_city = sys.argv[1]
    my_second_city = sys.argv[2]
my_window.update_idletasks()
my_window.update()
start_time = time.perf_counter()
a_star(my_first_city, my_second_city)
for node in junctions:
    for node2 in junctions[node].keys():
        first_xy = scaled(node_location[node][1], node_location[node][0])
        second_xy = scaled(node_location[node2][1], node_location[node2][0])
        my_canvas.create_line(first_xy[0], first_xy[1], second_xy[0], second_xy[1],
                              width=2, fill="black")
dijkstra(my_first_city, my_second_city)
end_time = time.perf_counter()
total_time = end_time - start_time
time.sleep(20)
print(total_time)