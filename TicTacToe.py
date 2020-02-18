import sys
from collections import deque


def find_index(row, column, size):
    index = size * row + column
    return index


def find_pos(index, size):
    row = int(index / size)
    column = index - row * size
    return [row, column]


def print_puzzle(puzzle):
    output_puzzle = ""
    for row in range(0, 9, 3):
        for column in range(row, row + 3):
            output_puzzle += puzzle[column]
        output_puzzle += "\n"
    print(output_puzzle)


def game_over(puzzle):
    o_wins = False
    x_wins = False
    if puzzle[0] == puzzle[1] == puzzle[2]:
        val = puzzle[0]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[3] == puzzle[4] == puzzle[5]:
        val = puzzle[3]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[6] == puzzle[7] == puzzle[8]:
        val = puzzle[6]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[0] == puzzle[3] == puzzle[6]:
        val = puzzle[0]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[1] == puzzle[4] == puzzle[7]:
        val = puzzle[1]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[2] == puzzle[5] == puzzle[8]:
        val = puzzle[2]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[0] == puzzle[4] == puzzle[8]:
        val = puzzle[0]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if puzzle[2] == puzzle[4] == puzzle[6]:
        val = puzzle[2]
        if val == "O":
            o_wins = True
        if val == "X":
            x_wins = True
    if o_wins:
        return -1
    elif x_wins:
        return 1
    elif "." not in puzzle:
        return 0
    else:
        return None


def count_characters(puzzle, c):
    countt = 0
    for p in puzzle:
        if p == c:
            countt += 1
    return countt


def get_num_games():
    puzzle = "........."
    fringe = deque(get_possible_moves(puzzle, "X"))
    count = 0
    num_times = 0
    final_boards = set()
    while len(fringe) > 0:
        current = fringe.popleft()
        if game_over(current) is None:
            if count_characters(current, ".") % 2 == 0:
                new_possible_vals = get_possible_moves(current, "O")
            else:
                new_possible_vals = get_possible_moves(current, "X")
            for val in new_possible_vals:
                fringe.append(val)
        else:
            final_boards.add(current)
            count += 1
    for board in final_boards:
        if game_over(board) == 1 and count_characters(board, ".") == 0:
            # print(board)
            num_times += 1
    return num_times
    # return count


def get_max(puzzle):
    game_over_val = game_over(puzzle)
    if game_over_val is not None:
        return game_over_val
    possible_moves = get_possible_moves(puzzle, "X")
    values = []
    for move in possible_moves.keys():
        this_min = get_min(move)
        values.append(this_min)
    return max(values)


def get_min(puzzle):
    game_over_val = game_over(puzzle)
    if game_over_val is not None:
        return game_over_val
    possible_moves = get_possible_moves(puzzle, "O")
    values = []
    for move in possible_moves.keys():
        this_max = get_max(move)
        # if puzzle == "XO.X.....":
        #   print("move", move, this_max)
        values.append(this_max)
    return min(values)


def get_possible_moves(puzzle, turn):
    remaining_moves = {}
    list_puzzle = list(puzzle)
    for i in range(0, len(puzzle)):
        if list_puzzle[i] == ".":
            current_list = list_puzzle.copy()
            current_list[i] = turn
            remaining_moves[("".join(current_list))] = i
    return remaining_moves


def play(puzzle, turn):
    if turn == my_computer:
        moves = get_possible_moves(puzzle, turn)
        index_to_value = {}
        if my_computer == "X":
            for move in moves.keys():
                # print("puzzle", move)
                this_min = get_min(move)
                index_to_value[moves[move]] = this_min
            max_min = -3
            max_min_index = -1
            for index in index_to_value.keys():
                val = index_to_value[index]
                if val > max_min:
                    max_min = val
                    max_min_index = index
                # print("moveX", move, "min", this_min)
        if my_computer == "O":
            for move in moves.keys():
                index_to_value[moves[move]] = get_max(move)
            max_min = 3
            max_min_index = -1
            for index in index_to_value.keys():
                val = index_to_value[index]
                if val < max_min:
                    max_min = val
                    max_min_index = index
        for index in index_to_value.keys():
            val = index_to_value[index]
            result = ""
            if val == -1:
                if my_computer == "O":
                    result = "win"
                if my_computer == "X":
                    result = "loss"
            if val == 0:
                result = "tie"
            if val == 1:
                if my_computer == "O":
                    result = "loss"
                if my_computer == "X":
                    result = "win"
            print("Moving at", index, "results in a", result)
        print("\n")
        print("I choose space", max_min_index, "\n")
        return max_min_index
    if turn == my_player:
        indexes = []
        for i in range(0, len(puzzle)):
            if puzzle[i] == ".":
                indexes.append(i)
        print("You can move to any one of these space:", indexes)
        player_choice = int(input("Your choice? "))
        print("\n")
        return player_choice

start_time = time.perf_counter()
my_puzzle = sys.argv[1]
my_puzzle_list = list(my_puzzle)
print("Current board:")
print_puzzle(my_puzzle)
empty = False
if count_characters(my_puzzle, ".") == 9:
    empty = True
if empty:
    my_computer = input("Should I be X or O? ")
    print("\n")
    if my_computer == "X":
        my_player = "O"
    else:
        my_player = "X"
else:
    if count_characters(my_puzzle, ".") % 2 == 0:
        my_computer = "O"
        my_player = "X"
    else:
        my_computer = "X"
        my_player = "O"

if empty:
    count = 1
else:
    if my_computer == "O":
        count = 2
    else:
        count = 1
game_state = game_over(my_puzzle)
while game_state is None:
    if count % 2 == 1:
        current_index = play(my_puzzle, "X")
        my_puzzle_list[current_index] = "X"
    else:
        current_index = play(my_puzzle, "O")
        my_puzzle_list[current_index] = "O"
    my_puzzle = "".join(my_puzzle_list)
    print("current board:")
    print_puzzle(my_puzzle)
    count += 1
    game_state = game_over(my_puzzle)
if game_state == 1:
    if my_computer == "X":
        print("I win")
    else:
        print("You win")
if game_state == 0:
    print("We tied")
if game_state == -1:
    if my_computer == "O":
        print("I win")
    else:
        print("You win")
