from collections import deque
import time
import sys

def find_path(visited, current):
    pathway = [current]
    while visited[current] != '':
        current = visited[current]
        pathway.append(current)
    pathway.reverse()
    return pathway


def bfs(start, end):
    fringe = deque()
    visited = dict()
    fringe.append(start)
    visited[start] = ''
    while len(fringe) > 0:
        v = fringe.popleft()
        if v == end:
            return find_path(visited, v)
        else:
            c = final_connected[v]
            for child in c:
                if child not in visited:
                    fringe.append(child)
                    visited[child] = v
    return None


dictionary = []

with open(sys.argv[1]) as f:
    for line in f:
        dictionary.append(line.strip().lower())

start_time = time.perf_counter()
my_word_num = 0
connected_words = {}
for w in dictionary:
    list_w = list(w)
    for l in range(len(w)):
        index_l = l
        before_l = list_w[index_l]
        list_w[index_l] = "."
        new_w = "".join(list_w)
        if new_w not in connected_words.keys():
            connected_words[new_w] = set()
        connected_words[new_w].add(w)
        list_w[index_l] = before_l

final_connected = {}
for key in connected_words.keys():
    values = connected_words[key]
    for value in connected_words[key]:
        if final_connected.get(value) is None:
            final_connected[value] = set()
        final_connected[value].update(values)
        final_connected[value].remove(value)
end_time = time.perf_counter()
total_time = end_time - start_time
print("Time to create the data structure was:", total_time)
print("There are", len(dictionary), "words in this dict.")
i = 0
start_time_solve = time.perf_counter()
everything = ""
with open(sys.argv[2]) as f:
    for line in f:
        words_list = line.strip().split(" ")
        s = words_list[0]
        e = words_list[1]
        path = bfs(s, e)
        everything += "Line: " + str(i) + "\n"
        if path is None:
            everything += "No solution!" + "\n"
        else:
            everything += "Length is: " + str(len(path)) + "\n"
            for p in path:
                everything += p + "\n"
        i += 1
        everything += "\n"
    end_time_solve = time.perf_counter()
total_time_solve = end_time_solve - start_time_solve
print(everything)
print("Time to solve all of these puzzles was:", total_time_solve)
print("Time to create the data structure plus time to solve these puzzles was:", total_time+total_time_solve)