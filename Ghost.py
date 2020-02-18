import sys
import time


def goal_test(curr_word, player): #if word is complete and it is the opponent's turn, that's good for the player
    if curr_word in list_of_words:
        if player == "opponent":
            return -1
        if player == "player":
            return 1
    return 0


def get_possible_moves(curr_word):
    list_of_possible_words = dict_values.get(curr_word)
    storage = []
    for i in list_of_possible_words:
        if i[0] not in storage:
            storage.append(i[0])
    return storage


def maxx(board, alpha, beta):
    y = goal_test(board, "player")
    if y != 0:
        return y
    possible = get_possible_moves(board)
    best_value = -1000
    for i in possible:
        new_word = board + i
        value = mini(new_word, alpha, beta)
        best_value = max(best_value, value)
        alpha = max(best_value, alpha)
        if alpha >= beta:
            break
    return best_value


def mini(board, alpha, beta):
    y = goal_test(board, "opponent")
    best_value = 1000
    if y != 0:
        #print(y)
        return y
    possible = get_possible_moves(board)
    for i in possible:
        new_word = board + i
        value = maxx(new_word, alpha, beta)
        best_value = min(best_value, value)
        beta = min(best_value, beta)
        if alpha >= beta:
            break
    return best_value


def play(puzzle):
    moves = get_possible_moves(puzzle)
    index_to_value = {}
    for move in moves:
        new_word = puzzle + move
        #print("new_word:", new_word)
        this_min = mini(new_word, -1000, 1000)
        index_to_value[move] = this_min
    possible_characters = []
    for index in index_to_value.keys():
        val = index_to_value[index]
        if val == 1:
            possible_characters.append(index)
        # print("moveX", move, "min", this_min)
    return possible_characters


start_time = time.perf_counter()
min_length = int(sys.argv[2])
list_of_words = []
dict_values = {}
with open(sys.argv[1]) as f:
    for line in f:
        word = line.strip().lower()
        if word.isalpha() and len(word) >= min_length:
            list_of_words.append(word)
for w in list_of_words:
    list_w = list(w)
    for l in range(len(w)):
        key_w_list = w[:l]
        key_w = "".join(key_w_list)
        if key_w not in dict_values.keys():
            dict_values[key_w] = set()
        val_w_list = w[l:]
        val_w = "".join(val_w_list)
        dict_values[key_w].add(val_w)
if len(sys.argv) == 4:
    game_in_progress = sys.argv[3].lower().strip()
    result = play(game_in_progress)
else:
    result = play("")
end_time = time.perf_counter()
total_time = end_time - start_time
if len(result) == 0:
    print("The next player will lose!")
else:
    print("next player will win with any of these letters:", sorted(result))
print(total_time)