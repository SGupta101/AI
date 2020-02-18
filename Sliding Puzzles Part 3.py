import heapq
import time
import random
import sys
from collections import deque


def is_solvable(board, size):
    unordered_pairs = 0
    new_board = board.replace(".", "")
    if size % 2 != 0:
        for current in range(0, size * size - 1):
            for other in range(current):
                if new_board[current] < new_board[other]:
                    unordered_pairs += 1
        if unordered_pairs % 2 == 0:
            return True
        else:
            return False
    if size % 2 == 0:
        row = find_pos(board.find("."), size)[0]
        for current in range(0, size * size - 1):
            for other in range(current):
                if new_board[current] < new_board[other]:
                    unordered_pairs += 1
        if row % 2 == 0:
            if unordered_pairs % 2 != 0:
                return True
            return False
        else:
            if unordered_pairs % 2 == 0:
                return True
            return False


def find_index(row, column, size):
    index = size * row + column
    return index


def find_pos(index, size):
    row = int(index / size)
    column = index - row * size
    return [row, column]


def find_goal(b):
    goal = sorted(b)
    goal.pop(0)
    goal.append(".")
    goal_str = ""
    goal_str = goal_str.join(goal)
    return goal_str


def goal_test(b):
    if b == find_goal(b):
        return True
    else:
        return False


def get_children(x, s):
    boards = []
    period_index = x.find(".")
    period_row = find_pos(period_index, s)[0]
    period_column = find_pos(period_index, s)[1]
    if period_column < s - 1:
        lb = list(x)
        lb[period_index], lb[period_index + 1] = lb[period_index + 1], lb[period_index]
        boards.append(''.join(lb))
    if period_column > 0:
        lb = list(x)
        lb[period_index], lb[period_index - 1] = lb[period_index - 1], lb[period_index]
        boards.append(''.join(lb))
    if period_row < s - 1:
        lb = list(x)
        new_index = find_index(period_row + 1, period_column, s)
        lb[period_index], lb[new_index] = lb[new_index], lb[period_index]
        boards.append(''.join(lb))
    if period_row > 0:
        lb = list(x)
        new_index = find_index(period_row - 1, period_column, s)
        lb[period_index], lb[new_index] = lb[new_index], lb[period_index]
        boards.append(''.join(lb))
    return boards


def heuristic(board, s):
    goal = find_goal(board)
    count = 0
    for piece in board:
        goal_piece_index = goal.find(piece)
        piece_index = board.find(piece)
        if goal_piece_index != piece_index and piece != ".":
            goal_pos = find_pos(goal_piece_index, s)
            piece_pos = find_pos(piece_index, s)
            count += abs(goal_pos[0] - piece_pos[0]) + abs(goal_pos[1] - piece_pos[1])
    return count


def new_heuristic(board, s):
    goal = find_goal(board)
    count = 0
    row_conflicts = 0
    column_conflicts = 0
    for piece in board:
        goal_piece_index = goal.find(piece)
        piece_index = board.find(piece)
        if goal_piece_index != piece_index and piece != ".":
            goal_pos = find_pos(goal_piece_index, s)
            piece_pos = find_pos(piece_index, s)
            count += abs(goal_pos[0] - piece_pos[0]) + abs(goal_pos[1] - piece_pos[1])
    new_board = board
    for i in range(len(goal)):
        if find_pos(i, s)[0] != find_pos(board.find(goal[i]), s)[0] or goal[i] == ".":
            new_board = new_board.replace(goal[i], ".")
    for i in range(0, s):
        for k in range(0, s - 1):
            index = i * s + k
            if new_board[index] != "." and new_board[index + 1] != "." and new_board[index] > new_board[index + 1]:
                row_conflicts += 2
    new_board = board
    for i in range(len(board)):
        if find_pos(i, s)[1] != find_pos(board.find(goal[i]), s)[1]:
            new_board = new_board.replace(goal[i], ".")
    for i in range(0, s):
        pieces = []
        for k in range(0, s):
            pieces.append(board[i + s * k])
        for k in range(len(pieces) - 1):
            if pieces[k] != "." and pieces[k + 1] != "." and pieces[k] > pieces[k + 1]:
                column_conflicts += 2
    return count + row_conflicts + column_conflicts


class Node:
    state = ""
    depth = 0
    ancestors = set()
    path = ""
    f = 0

    def __init__(self, s, d=0, a=None, p="", total=0):
        if a is None:
            a = set()
        self.state = s
        self.depth = d
        self.ancestors = a
        self.path = p
        self.f = total

    def print_node(self):
        print(self.state, self.depth)

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __hash__(self):
        return hash(self.f)


def a_star_originalm(board, s, m):
    d = {}
    closed = set()
    start_node = Node(board)
    d[start_node.state] = start_node
    start_node.f = heuristic(board, s)
    fringe = [start_node]
    heapq.heapify(fringe)
    while len(fringe) > 0:
        v = heapq.heappop(fringe)
        if goal_test(v.state):
            return v.depth
        if v.state not in closed:
            closed.add(v)
            children = get_children(v.state, s)
            for child in children:
                c = d.get(child)
                if c is None or c.depth > v.depth:
                    c = Node(child)
                    d[child] = c
                    c.depth = v.depth + 1
                    c.f = m * c.depth + heuristic(c.state, s)
                    heapq.heappush(fringe, c)

    return None

# # This is for part A
# with open(sys.argv[1]) as f:j
#     for line in f:
#         arguments = line.split(" ")
#         my_size = int(arguments[0].strip())
#         my_board = arguments[1].strip()
#         print("board:", my_board)
#         i = 1
#         while i > 0:
#             print("m:", i)
#             start = time.perf_counter()
#             my_depth = a_star_original(my_board, my_size, i)
#             end = time.perf_counter()
#             total_time = end - start
#             # print("m:", i,)
#             print("time:", total_time)
#             print("depth:", my_depth)
#             i -= .1
#         i = 1
#         while i < 6:
#             print("m:", i)
#             start = time.perf_counter()
#             my_depth = a_star_original(my_board, my_size, i)
#             end = time.perf_counter()
#             total_time = end - start
#             # print("m:", i,)
#             print("time:", total_time)
#             print("depth:", my_depth)
#             i += 1


# # This is for part B
# class NodeB:
#     state = ""
#     depth = 0
#     ancestors = set()
#     path = ""
#     f = 0
#
#     def __init__(self, s, d=0, a=None, p="", total=0):
#         if a is None:
#             a = set()
#         self.state = s
#         self.depth = d
#         self.ancestors = a
#         self.path = p
#         self.f = total
#         self.rand = random.randint(1, 100)
#
#     def print_node(self):
#         print(self.state, self.depth)
#
#     def __eq__(self, other):
#         if self.f == other.f:
#             return self.rand == other.rand
#         else:
#             return True
#
#     def __lt__(self, other):
#         if self.f == other.f:
#             return self.rand < other.rand
#         else:
#             return self.f < other.f
#
#     def __gt__(self, other):
#         if self.f == other.f:
#             return self.rand > other.rand
#         else:
#             return self.f > other.f
#
#     def __hash__(self):
#         return hash(self.f) + hash(self.rand)
#
#
# def find_path(visited, current):
#     pathway = [current]
#     while visited[current] != '':
#         current = visited[current]
#         pathway.append(current)
#     pathway.reverse()
#     return pathway
#
#
# def a_star(board, s, m):
#     d = {}
#     visited = dict()
#     closed = set()
#     start_node = NodeB(board)
#     d[start_node.state] = start_node
#     start_node.f = heuristic(board, s)
#     fringe = [start_node]
#     heapq.heapify(fringe)
#     visited[board] = ''
#     while len(fringe) > 0:
#         v = heapq.heappop(fringe)
#         if goal_test(v.state):
#             return find_path(visited, v.state)
#         if v.state not in closed:
#             closed.add(v)
#             children = get_children(v.state, s)
#             for child in children:
#                 c = d.get(child)
#                 if c is None or c.depth > v.depth:
#                     c = NodeB(child)
#                     d[child] = c
#                     c.depth = v.depth + 1
#                     c.f = m * c.depth + heuristic(c.state, s)
#                     heapq.heappush(fringe, c)
#                     visited[child] = v.state
#
#     return None
#
#
# print("original:", a_star_original("JMGBILDFK.EONHCA", 4, 0.4))
# print("board:", "JMGBILDFK.EONHCA","m:", 0.4)
# for i in range(20):
#     paths = a_star("JMGBILDFK.EONHCA", 4, 0.4)
#     print("path length:", len(paths) - 1)
#     print("path:", paths)

# # This is for part C
# def a_star_c(board, s, m):
#     d = {}
#     closed = set()
#     start_node = Node(board)
#     d[start_node.state] = start_node
#     start_node.f = new_heuristic(board, s)
#     fringe = [start_node]
#     heapq.heapify(fringe)
#     while len(fringe) > 0:
#         v = heapq.heappop(fringe)
#         if goal_test(v.state):
#             return v.depth
#         if v.state not in closed:
#             closed.add(v)
#             children = get_children(v.state, s)
#             for child in children:
#                 c = d.get(child)
#                 if c is None or c.depth > v.depth:
#                     c = Node(child)
#                     d[child] = c
#                     c.depth = v.depth + 1
#                     c.f = m * c.depth + new_heuristic(c.state, s)
#                     heapq.heappush(fringe, c)
#
#     return None
#
#
# with open(sys.argv[1]) as f:
#     for line in f:
#         arguments = line.split(" ")
#         my_size = int(arguments[0].strip())
#         my_board = arguments[1].strip()
#         print("board:", my_board)
#         start = time.perf_counter()
#         my_depth = a_star_original(my_board, my_size, 1)
#         end = time.perf_counter()
#         total_time = end - start
#         print("original depth:", my_depth, "original time:", total_time)
#         start = time.perf_counter()
#         my_depth = a_star_c(my_board, my_size, 1)
#         end = time.perf_counter()
#         total_time = end - start
#         print("new depth:", my_depth, "new time:", total_time)


# This is for part G
# def a_star_original(board, s):
#     d = {}
#     closed = set()
#     start_node = Node(board)
#     d[start_node.state] = start_node
#     start_node.f = heuristic(board, s)
#     fringe = [start_node]
#     heapq.heapify(fringe)
#     while len(fringe) > 0:
#         v = heapq.heappop(fringe)
#         if goal_test(v.state):
#             return v.depth
#         if v.state not in closed:
#             closed.add(v)
#             children = get_children(v.state, s)
#             for child in children:
#                 c = d.get(child)
#                 if c is None or c.depth > v.depth:
#                     c = Node(child)
#                     d[child] = c
#                     c.depth = v.depth + 1
#                     c.f = c.depth + heuristic(c.state, s)
#                     heapq.heappush(fringe, c)
#
#     return None
#
#
# def a_star_buckets(board, s):
#     d = {}
#     closed = set()
#     start_node = Node(board)
#     d[start_node.state] = start_node
#     start_node.f = heuristic(board, s)
#     dq = deque()
#     dq.append(start_node)
#     fringe = {start_node.f: dq}
#     while len(fringe) > 0:
#         smallest_key = min(fringe.keys())
#         v = (fringe[smallest_key]).popleft()
#         if len(fringe[smallest_key]) == 0:
#             del fringe[smallest_key]
#         if goal_test(v.state):
#             return v.depth
#         if v.state not in closed:
#             closed.add(v)
#             children = get_children(v.state, s)
#             for child in children:
#                 c = d.get(child)
#                 if c is None or c.depth > v.depth:
#                     c = Node(child)
#                     d[child] = c
#                     c.depth = v.depth + 1
#                     c.f = c.depth + heuristic(c.state, s)
#                     if c.f in fringe.keys():
#                         fringe[c.f].append(c)
#                     else:
#                         dq = deque()
#                         dq.append(c)
#                         fringe[c.f] = dq
#     return None
#
#
# with open(sys.argv[1]) as f:
#     line_number = 0
#     for line in f:
#         arguments = line.split(" ")
#         my_size = int(arguments[0].strip())
#         my_board = arguments[1].strip()
#         my_character = arguments[2].strip()
#         # print(my_size, my_board, my_character)
#         if not is_solvable(my_board, my_size):
#             start = time.perf_counter()
#             is_solvable(my_board, my_size)
#             end = time.perf_counter()
#             total_time = end - start
#             print("Line", line_number, ":", my_board, ", no solution determined in", total_time, "seconds")
#         else:
#             path = 0
#             if my_character == "A":
#                 start = time.perf_counter()
#                 path = a_star_original(my_board, my_size)
#                 end = time.perf_counter()
#                 total_time = end - start
#                 print("Line", line_number, ":", my_board, ", A* -", path, "moves found in", total_time, "seconds")
#
#                 start = time.perf_counter()
#                 path = a_star_buckets(my_board, my_size)
#                 end = time.perf_counter()
#                 total_time = end - start
#                 print("Line", line_number, ":", my_board, ", A* buckets -", path, "moves found in", total_time,
#                       "seconds")
#         line_number += 1
