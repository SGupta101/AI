from collections import deque
import time
import sys

def one_letter_away(word1, word2):
    if word1 == word2:
        return False
    first = False
    for index in range(len(word1)):
        letter1 = word1[index]
        letter2 = word2[index]
        if letter1 != letter2:
            if first:
                return False
            first = True
    return first


def get_children(word, word_num):
    c = set()
    for i in range(word_num + 1, len(dictionary)):
        word2 = dictionary[i]
        if one_letter_away(word, word2):
            c.add(word2)
    return c


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
            c = connected_words[v]
            for child in c:
                if child not in visited:
                    fringe.append(child)
                    visited[child] = v
    return None


dictionary = []
connected_words = {}
with open(sys.argv[1]) as f:
    for line in f:
        dictionary.append(line.strip().lower())
        connected_words[line.strip().lower()] = set()

start_time = time.perf_counter()
my_word_num = 0

for w in dictionary:
    children = get_children(w, my_word_num)
    for my_child in children:
        connected_words[w].add(my_child)
        connected_words[my_child].add(w)
    my_word_num += 1

end_time = time.perf_counter()
total_time = end_time - start_time
print("Time to create the data structure was:", total_time)
print("There are", len(dictionary), "words in this dict.")
i = 0
with open(sys.argv[2]) as f:
    for line in f:
        words_list = line.strip().split(" ")
        s = words_list[0]
        e = words_list[1]
        path = bfs(s, e)
        end_time = time.perf_counter()
        print("Line:", i)
        if path is None:
            print("No solution!")
        else:
            print("Length is:", len(path))
            for p in path:
                print(p)
        i += 1
total_time = end_time - start_time
print("Time to solve all of these puzzles was:", total_time)