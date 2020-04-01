import sys
import time


def contains_period(board):
    for k in board.keys():
        if len(board[k]) > 1:
            return True
    return False


def check_test(board, finished):
    for row in rows:
        num_instances = {}
        for symbol in symbol_set:
            num_instances[symbol] = 0
        num_periods = 0
        for index in row:
            if len(board[index]) > 1:
                num_periods += 1
            else:
                num_instances[board[index]] += 1
        if finished:
            if num_periods > 0:
                print("too many periods")
                return False
            for value in num_instances.values():
                if value != 1:
                    return False
        else:
            for value in num_instances.values():
                if value > 1:
                    return False
    for column in columns:
        num_instances = {}
        for symbol in symbol_set:
            num_instances[symbol] = 0
        num_periods = 0
        for index in column:
            if len(board[index]) > 1:
                num_periods += 1
            else:
                num_instances[board[index]] += 1
        if finished:
            if num_periods > 0:
                print("too many periods")
                return False
            for value in num_instances.values():
                if value != 1:
                    return False
        else:
            for value in num_instances.values():
                if value > 1:
                    return False
    for block in blocks:
        num_instances = {}
        for symbol in symbol_set:
            num_instances[symbol] = 0
        num_periods = 0
        for index in block:
            if len(board[index]) > 1:
                num_periods += 1
            else:
                num_instances[board[index]] += 1
        if finished:
            if num_periods > 0:
                print("too many periods")
                return False
            for value in num_instances.values():
                if value != 1:
                    return False
        else:
            for value in num_instances.values():
                if value > 1:
                    return False
    return True


def find_pos(index, s):
    this_row = int(index / s)
    this_column = index - this_row * s
    return [this_row, this_column]


def find_index(this_row, this_column, s):
    index = s * this_row + this_column
    return index


def find_block(rowcol, height, width):
    return [rowcol[0] // height, rowcol[1] // width]


def board_to_puzzle(board):
    puzzle = ""
    for key in board.keys():
        val = board[key]
        if len(val) > 1:
            puzzle += "."
        else:
            puzzle += val
    return puzzle


def print_puzzle(s, board):
    # puzzle = board_to_puzzle(board)
    puzzle = board
    matrix = ""
    for row in range(0, s):
        for column in range(s * row, s * row + s):
            matrix += puzzle[column]
            if column != s - 1:
                matrix += " "
        if row != s - 1:
            matrix += "\n"
    print(matrix)


def instances(board):
    num_instances = {}
    for symbol in symbol_set:
        num_instances[symbol] = 0
    num_instances["."] = 0
    for k in range(len(board.keys())):
        val = board[k]
        if len(val) > 1:
            num_instances["."] += 1
        else:
            num_instances[val] += 1
    return num_instances


def get_symbol_set(size):
    sorted_values = set()
    abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    if size > 9:
        for k in range(1, 10):
            sorted_values.add(str(k))
        sorted_values.update(set(abc[0:size - 9]))
    else:
        for k in range(1, size + 1):
            sorted_values.add(str(k))
    return sorted_values


def get_next_unassigned_var(board):
    for k in range(len(board.keys())):
        if len(board[k]) > 1:
            return k


def get_sorted_values(board, var):
    sorted_values = set()
    sorted_values.update(symbol_set)
    for neighbor in neighbors[var]:
        n = board[neighbor]
        if n in sorted_values:
            sorted_values.remove(n)
    sorted_values = list(sorted_values)
    sorted_values.sort()
    return sorted_values


def check_math_periods(board):
    for letter in letter_to_cell.keys():
        value = letter_to_cell[letter]
        indexes = value[0]
        digit = value[1]
        arithmetic_clue = value[2]
        final_number = 0
        k = 0
        period = False
        if arithmetic_clue == "+":
            for index in indexes:
                number_string = board[index]
                number = int(number_string)
                if len(number_string) == 1:
                    if k == 0:
                        final_number = number
                    else:
                        final_number += number
                    k += 1
                else:
                    period = True
        elif arithmetic_clue == "-":
            for index in indexes:
                number_string = board[index]
                number = int(number_string)
                if len(number_string) == 1:
                    if k == 0:
                        final_number = number
                    else:
                        final_number -= number
                    k += 1
                else:
                    period = True
        elif arithmetic_clue == "/":
            list_indexes = []
            for index in indexes:
                list_indexes.append(index)
            num_one_string = board[list_indexes[0]]
            num_two_string = board[list_indexes[1]]
            if len(num_one_string) == 1 and len(num_two_string) == 1:
                num_one = int(num_one_string)
                num_two = int(num_two_string)
                final_number = num_one / num_two
                if final_number != digit:
                    final_number = num_two / num_one
            else:
                period = True
        elif arithmetic_clue == "X":
            for index in indexes:
                number_string = board[index]
                number = int(number_string)
                if len(number_string) == 1:
                    if k == 0:
                        final_number = number
                    else:
                        final_number *= number
                    k += 1
                else:
                    period = True
        if period is False and abs(final_number) != digit:
            return False
    return True


def check_math(board):
    for letter in letter_to_cell.keys():
        value = letter_to_cell[letter]
        indexes = value[0]
        digit = value[1]
        arithmetic_clue = value[2]
        final_number = 0
        k = 0
        if arithmetic_clue == "+":
            for index in indexes:
                number_string = board[index]
                number = int(number_string)
                if k == 0:
                    final_number = number
                else:
                    final_number += number
                k += 1
        elif arithmetic_clue == "-":
            for index in indexes:
                number_string = board[index]
                number = int(number_string)
                if k == 0:
                    final_number = number
                else:
                    final_number -= number
                k += 1
        elif arithmetic_clue == "/":
            list_indexes = []
            for index in indexes:
                list_indexes.append(index)
            num_one_string = board[list_indexes[0]]
            num_two_string = board[list_indexes[1]]
            num_one = int(num_one_string)
            num_two = int(num_two_string)
            final_number = num_one / num_two
            if final_number != digit:
                final_number = num_two / num_one
        elif arithmetic_clue == "X":
            for index in indexes:
                number_string = board[index]
                number = int(number_string)
                if k == 0:
                    final_number = number
                else:
                    final_number *= number
                k += 1
        if abs(final_number) != digit:
            return False
    return True


def csp_backtracking(board):
    if not check_math_periods(board):
        return None
    if not contains_period(board) and check_math(board):
        return board
    var = get_next_unassigned_var(board)
    possible_values = get_sorted_values(board, var)
    new_board = board.copy()
    for val in possible_values:
        new_board[var] = val
        result = csp_backtracking(new_board)
        if result is not None:
            return result
    return None


def forward_looking(board, list_indexes):
    if list_indexes is None:
        one_solution = []
        for key in board.keys():
            val = board[key]
            if len(val) == 1:
                one_solution.append(key)
    else:
        one_solution = []
        for index in list_indexes:
            one_solution.append(index)
    for one in one_solution:
        for neighbor in neighbors[one]:
            possibility = board[neighbor]
            constraint = board[one]
            if constraint in possibility:
                possibility = possibility.replace(constraint, "")
                if len(possibility) == 0:
                    return None
                board[neighbor] = possibility
                if len(possibility) == 1:
                    one_solution.append(neighbor)
    return board


def get_most_constrained_var(board):
    most_constrained_index = 0
    num_possibilities = 1000
    for var in board:
        constraints = len(board[var])
        if 1 < constraints < num_possibilities:
            num_possibilities = constraints
            most_constrained_index = var
    return most_constrained_index


def csp_backtracking_with_forward_looking(board):
    if not contains_period(board):
        return board
    var = get_most_constrained_var(board)
    for val in get_sorted_values(board, var):
        new_board = board.copy()
        new_board[var] = val
        checked_board = forward_looking(new_board, [var])
        if checked_board is not None:
            result = csp_backtracking_with_forward_looking(checked_board)
            if result is not None:
                return result
    return None


def csp_backtracking_with_cp(board):
    if not contains_period(board):
        return board
    var = get_most_constrained_var(board)
    for val in get_sorted_values(board, len(board.keys())):
        new_board = board.copy()
        new_board[var] = val
        board = constraint_propagation(new_board)
        if board is not None:
            checked_board = board
            result = csp_backtracking_with_cp(checked_board)
            if result is not None:
                return result
    return None


def constraint_propagation(board):
    changes = set()
    change = False
    assign_vals = set()
    all_indiv = [rows, columns, blocks]
    for indivs in all_indiv:
        for indiv in indivs:
            current_changes = set()
            piece_to_index = {}
            for index in indiv:
                for val in board[index]:
                    if val not in piece_to_index.keys():
                        piece_to_index[val] = []
                    piece_to_index[val].append(index)
            for piece in piece_to_index.keys():
                if piece not in current_changes:
                    index = piece_to_index[piece]
                    if len(index) == 0:
                        return None
                    if len(index) == 1:
                        index_num = index[0]
                        board[index_num] = piece
                        changes.add(index_num)
                        current_changes.add(piece)
    board = forward_looking(board, changes)
    if board is not None:
        board = board
    return board


def csp_backtracking_with_fl_and_cp(board):
    if not check_math_periods(board):
        return None
    if not contains_period(board) and check_math(board):
        return board
    var = get_most_constrained_var(board)
    for val in get_sorted_values(board, var):
        new_board = board.copy()
        new_board[var] = val
        forward_board = forward_looking(new_board, [var])
        if forward_board is not None:
            constraint_board = constraint_propagation(forward_board)
            if constraint_board is not None:
                result = csp_backtracking_with_fl_and_cp(constraint_board)
                if result is not None:
                    return result
    return None


ever_false = False
all_time = 0
all_boards = []
letter_to_cell = {}
cell_to_letter = {}
first_text_file_info = []
with open(sys.argv[1]) as f:
    for line in f:
        first_text_file_info.append(line.strip().upper())
text_file_info = [first_text_file_info[0]]
print(first_text_file_info)
for i in range(1, len(first_text_file_info)):
    current_info = first_text_file_info[i]
    if " " not in current_info:
        break
    text_file_info.append(current_info)

# ever_false = False
# all_time = 0
# all_boards = []
# letter_to_cell = {}
# cell_to_letter = {}
# text_file_info = []
# with open(sys.argv[1]) as f:
#     for line in f:
#         text_file_info.append(line.strip().upper())


my_puzzle_letters = text_file_info[0]
N = int(len(my_puzzle_letters) ** (1 / 2))
sqr_N = N ** (1 / 2)
my_puzzle = ""
for letter_index in range(len(my_puzzle_letters)):
    my_letter = my_puzzle_letters[letter_index]
    cell_to_letter[letter_index] = my_letter
    if my_letter not in letter_to_cell.keys():
        letter_to_cell[my_letter] = [set(), 0, ""]
    letter_to_cell[my_letter][0].add(letter_index)
    my_puzzle += "."
for info_index in range(1, len(text_file_info)):
    info = text_file_info[info_index].strip()
    info_list = list(info)
    info_length = len(info_list)
    my_letter = info_list[0]
    my_digit = ""
    for character_index in range(2, info_length):
        character = info_list[character_index]
        if character == " ":
            break
        my_digit += character
    my_arithmetic_clue = info_list[info_length - 1]
    letter_to_cell[my_letter][1] = int(my_digit)
    letter_to_cell[my_letter][2] = my_arithmetic_clue

rows = []
columns = []
blocks = []

for i in range(0, N):
    my_row = set()
    my_column = set()
    for r in range(N * i, N * i + N):
        my_row.add(r)
    for c in range(i, len(my_puzzle), N):
        my_column.add(c)
    rows.append(my_row)
    columns.append(my_column)

# print(cell_to_letter)
# print(letter_to_cell)
neighbors = {}
for i in range(0, len(my_puzzle)):
    neighbors[i] = set()
    for my_row in rows:
        if i in my_row:
            for r in my_row:
                neighbors[i].add(r)
    for my_column in columns:
        if i in my_column:
            for c in my_column:
                neighbors[i].add(c)
    neighbors[i].remove(i)
symbol_set = get_symbol_set(N)
my_puzzle_list = list(my_puzzle)
# print(my_puzzle)
# part 2
# print_puzzle(N, my_puzzle_letters)
# print("\n")
my_possibilities = {}
for space in range(len(my_puzzle_list)):
    if my_puzzle_list[space] != ".":
        my_possibilities[space] = my_puzzle_list[space]
    else:
        my_possibilities[space] = "".join(get_sorted_values(my_puzzle_list, space))

# my_possibilities[0] = "8"
# my_possibilities[6] = "3"
# my_possibilities[3] = "5"
# my_possibilities[9] = "5"
# my_possibilities[4] = "1"
# my_possibilities[5] = "2"
# my_possibilities[11] = "1"
# my_possibilities[7] = "2"
# my_possibilities[8] = "1"
# print(my_possibilities)
# print(check_math_periods(my_possibilities))

finished_board = csp_backtracking_with_fl_and_cp(my_possibilities)
print_puzzle(N, my_puzzle_letters)
print("\n")
print_puzzle(N, board_to_puzzle(finished_board))
print("\n")
print(check_math_periods(finished_board))
print(letter_to_cell)