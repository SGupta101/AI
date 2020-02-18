import time
import sys
import heapq
from collections import deque


def find_index(row, column, size):
    index = size * row + column
    return index


def find_pos(index, size):
    row = int(index / size)
    column = index - row * size
    return [row, column]


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


def find_path(visited, current):
    pathway = [current]
    while visited[current] != '':
        current = visited[current]
        pathway.append(current)
    pathway.reverse()
    return pathway


def bfs(b, s):
    fringe = deque()
    visited = dict()
    fringe.append(b)
    visited[b] = ''
    while len(fringe) > 0:
        v = fringe.popleft()
        if goal_test(v):
            return len(find_path(visited, v)) - 1
        else:
            children = get_children(v, s)
            for child in children:
                if child not in visited:
                    fringe.append(child)
                    visited[child] = v


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


def kdfs(my_node, k, s, d):
    fringe = [my_node]
    while len(fringe) > 0:
        v = fringe.pop()
        if v.depth == k and goal_test(v.state):
            return v
        if v.depth < k:
            children = get_children(v.state, s)
            for child in children:
                if child not in v.ancestors:
                    c = d.get(child)
                    if c is None or c.depth > v.depth:
                        c = Node(child)
                        d[child] = c
                        c.depth = v.depth + 1
                        fringe.append(c)
                    c.ancestors = c.ancestors.union(v.ancestors)
                    c.ancestors.add(c)

    return None


def iddfs(board, s):
    result = None
    k = 0
    my_node = Node(board)
    my_node.ancestors = set(my_node.state)
    my_dict = {my_node.state: my_node}
    while result is None:
        result = kdfs(my_node, k, s, my_dict)
        k += 1
    return result.depth


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


def a_star(board, s):
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
                    c.f = c.depth + heuristic(c.state, s)
                    heapq.heappush(fringe, c)

    return None


with open(sys.argv[1]) as f:
    line_number = 0
    for line in f:
        arguments = line.split(" ")
        my_size = int(arguments[0].strip())
        my_board = arguments[1].strip()
        my_character = arguments[2].strip()
        # print(my_size, my_board, my_character)
        if not is_solvable(my_board, my_size):
            start = time.perf_counter()
            is_solvable(my_board, my_size)
            end = time.perf_counter()
            total_time = end - start
            print("Line", line_number, ":", my_board, ", no solution determined in", total_time, "seconds")
        else:
            path = 0
            if my_character == "B":
                start = time.perf_counter()
                path = bfs(my_board, my_size)
                end = time.perf_counter()
                total_time = end - start
                print("Line", line_number, ":", my_board, ", BFS -", path, "moves found in", total_time, "seconds")
            if my_character == "I":
                start = time.perf_counter()
                path = iddfs(my_board, my_size)
                end = time.perf_counter()
                total_time = end - start
                print("Line", line_number, ":", my_board, ", ID-DFS -", path, "moves found in", total_time, "seconds")
            if my_character == "A":
                start = time.perf_counter()
                path = a_star(my_board, my_size)
                end = time.perf_counter()
                total_time = end - start
                print("Line", line_number, ":", my_board, ", A* -", path, "moves found in", total_time, "seconds")
            if my_character == "!":
                start = time.perf_counter()
                path = bfs(my_board, my_size)
                end = time.perf_counter()
                total_time = end - start
                print("Line", line_number, ":", my_board, ", BFS -", path, "moves found in", total_time, "seconds")
                start = time.perf_counter()
                path = a_star(my_board, my_size)
                end = time.perf_counter()
                total_time = end - start
                print("Line", line_number, ":", my_board, ", ID-DFS -", path, "moves found in", total_time, "seconds")
                start = time.perf_counter()
                path = a_star(my_board, my_size)
                end = time.perf_counter()
                total_time = end - start
                print("Line", line_number, ":", my_board, ", A* -", path, "moves found in", total_time, "seconds")

        line_number += 1