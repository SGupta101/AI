import sys
import random
import time


class Strategy():
    # implement all the required methods on your own
    def best_strategy(self, board, player, best_move, running):
        time.sleep(1)
        if running.value:
            num_periods = count_characters(board, ".")
            if num_periods == 25:
                value = play(board, player, "e")
            else:
                value = play(board, player, "m")
            best_move.value = value


def count_characters(puzzle, c):
    countt = 0
    for p in puzzle:
        if p == c:
            countt += 1
    return countt


def early(puzzle):  # mobility
    my_moves = possible_moves(puzzle, "@")
    other_moves = possible_moves(puzzle, "o")
    return len(my_moves) - len(other_moves)


def mid(puzzle):  # position
    weight_heuristic = 0
    for cell in weight_matrix:
        if puzzle[cell] == "@":
            weight_heuristic += weight_matrix[cell]
        elif puzzle[cell] == "o":
            weight_heuristic -= weight_matrix[cell]
    return weight_heuristic


def late(puzzle):
    return None


def who_wins(puzzle):
    num_blacks = 0
    num_whites = 0
    for piece in puzzle:
        if puzzle[piece] == "@":
            num_blacks += 1
        elif puzzle[piece] == "o":
            num_whites += 1
    if num_blacks > num_whites:
        return "@"
    elif num_blacks < num_whites:
        return "o"
    else:
        return None


max_depth = 5


def get_max(puzzle, alpha, beta, depth, heuristic):
    current_possible_moves = possible_moves(puzzle, "@")
    if heuristic == "e":
        if depth == 0:
            return early(puzzle)
    else:
        return mid(puzzle)
    best_value = -1000
    for current_move in current_possible_moves:
        new_board = move(puzzle, "@", current_move)
        value = get_min(new_board, alpha, beta, depth - 1, heuristic)
        best_value = max(best_value, value)
        alpha = max(best_value, alpha)
        if alpha >= beta:
            break
    return best_value


def get_min(puzzle, alpha, beta, depth, heuristic):
    current_possible_moves = possible_moves(puzzle, "o")
    if heuristic == "e":
        if depth == 0:
            return early(puzzle)
    else:
        return mid(puzzle)
    best_value = 1000
    for current_move in current_possible_moves:
        new_board = move(puzzle, "o", current_move)
        value = get_max(new_board, alpha, beta, depth - 1, heuristic)
        best_value = min(best_value, value)
        beta = min(best_value, beta)
        if alpha >= beta:
            break
    return best_value


def find_index(row, column):
    index = 10 * row + column
    return index


def find_pos(index):
    row = int(index / 10)
    column = index - row * 10
    return [row, column]


def print_board(board):
    for i in range(11):
        print(board[i * 10:i * 10 + 10])


def change(board, row, col, token):
    index = find_index(row, col)
    board[index] = token


def play(puzzle, token, heuristic):
    moves = possible_moves(puzzle, token)
    index_to_value = {}
    if token == "@":
        for current_move in moves:
            # print("puzzle", move)
            new_board = move(puzzle, token, current_move)
            this_min = get_min(new_board, -1000, 1000, max_depth, heuristic)
            index_to_value[current_move] = this_min
        max_min = -10000
        max_min_index = None
        for index in index_to_value.keys():
            val = index_to_value[index]
            if val > max_min:
                max_min = val
                max_min_index = index
            # print("moveX", move, "min", this_min)
    if token == "o":
        for current_move in moves:
            new_board = move(puzzle, token, current_move)
            this_max = get_max(new_board, -1000, 1000, max_depth, heuristic)
            index_to_value[current_move] = this_max
        max_min = 10000
        max_min_index = None
        for index in index_to_value.keys():
            val = index_to_value[index]
            if val < max_min:
                max_min = val
                max_min_index = index
    return max_min_index


def possible_moves(board, token):
    possible = set()
    opposite_tokens = []
    if token == "@":
        opposite_token = "o"
    else:
        opposite_token = "@"
    for p in range(0, len(board)):
        if board[p] == opposite_token:
            opposite_tokens.append(p)
    for t in opposite_tokens:
        pos = find_pos(t)
        row = pos[0]
        col = pos[1]
        if row != 0 and 1 and 8 and 9:
            top_index = find_index(row - 1, col)
            if board[top_index] == token:
                for i in range(row + 1, 10):
                    current_index = find_index(i, col)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
            bottom_index = find_index(row + 1, col)
            if board[bottom_index] == token:
                for i in range(row - 1, 0, -1):
                    current_index = find_index(i, col)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
            # top and bottom
        if col != 0 and 1 and 8 and 9:
            right_index = find_index(row, col + 1)
            if board[right_index] == token:
                for i in range(col - 1, 0, -1):
                    current_index = find_index(row, i)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
            left_index = find_index(row, col - 1)
            if board[left_index] == token:
                for i in range(col + 1, 10):
                    current_index = find_index(row, i)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
            # left and right
        if row != 0 and 1 and 8 and 9 and col != 0 and 1 and 8 and 9:
            up_left_index = find_index(row - 1, col - 1)
            if board[up_left_index] == token:
                current_index = find_index(row + 1, col + 1)
                while board[current_index] != "?":
                    current_pos = find_pos(current_index)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
                    current_index = find_index(current_pos[0] + 1, current_pos[1] + 1)
            down_right_index = find_index(row + 1, col + 1)
            if board[down_right_index] == token:
                current_index = find_index(row - 1, col - 1)
                while board[current_index] != "?":
                    current_pos = find_pos(current_index)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
                    current_index = find_index(current_pos[0] - 1, current_pos[1] - 1)
            up_right_index = find_index(row - 1, col + 1)
            if board[up_right_index] == token:
                current_index = find_index(row + 1, col - 1)
                while board[current_index] != "?":
                    current_pos = find_pos(current_index)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
                    current_index = find_index(current_pos[0] + 1, current_pos[1] - 1)
            down_left_index = find_index(row + 1, col - 1)
            if board[down_left_index] == token:
                current_index = find_index(row - 1, col + 1)
                while board[current_index] != "?":
                    current_pos = find_pos(current_index)
                    if board[current_index] == token:
                        break
                    if board[current_index] == ".":
                        possible.add(current_index)
                        break
                    current_index = find_index(current_pos[0] - 1, current_pos[1] + 1)
    possible_list = []
    for p in possible:
        possible_list.append(p)
    return sorted(possible_list)


def move(board, token, index):
    list_board = list(board)
    if token == "@":
        opposite_token = "o"
    else:
        opposite_token = "@"
    pos = find_pos(index)
    row = pos[0]
    col = pos[1]
    changes = set()
    if row != 0 and 1:
        current_index = find_index(row - 1, col)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0] - 1, current_pos[1])
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # top
    if row != 8 and 9:
        current_index = find_index(row + 1, col)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0] + 1, current_pos[1])
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # bottom
    if col != 8 and 9:
        current_index = find_index(row, col + 1)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0], current_pos[1] + 1)
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # right
    if col != 0 and 1:
        current_index = find_index(row, col - 1)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0], current_pos[1] - 1)
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # left
    if col != 0 and 1 and row != 0 and 1:
        current_index = find_index(row - 1, col - 1)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0] - 1, current_pos[1] - 1)
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # right up diagonal
    if col != 8 and 9 and row != 8 and 9:
        current_index = find_index(row + 1, col + 1)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0] + 1, current_pos[1] + 1)
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # down left diagonal
    if col != 8 and 9 and row != 0 and 1:
        current_index = find_index(row - 1, col + 1)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0] - 1, current_pos[1] + 1)
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # up left diagonal
    if col != 0 and 1 and row != 8 and 9:
        current_index = find_index(row + 1, col - 1)
        indexes = []
        while board[current_index] == opposite_token:
            current_pos = find_pos(current_index)
            indexes.append(current_index)
            current_index = find_index(current_pos[0] + 1, current_pos[1] - 1)
        if board[current_index] == token:
            for i in indexes:
                changes.add(i)
        # down right diagonal
    changes.add(index)
    for c in changes:
        list_board[c] = token
    return "".join(list_board)


weight_matrix = {}
for i in range(0, 99):
    weight_matrix[i] = 0
corner = 100
corner_next = -20
corner_diagonal = -20
next_next = 20
diagonal_next = 0

weight_matrix[11] = corner
weight_matrix[81] = corner
weight_matrix[18] = corner
weight_matrix[88] = corner
weight_matrix[21] = corner_next
weight_matrix[22] = corner_diagonal
weight_matrix[12] = corner_next
weight_matrix[71] = corner_next
weight_matrix[72] = corner_diagonal
weight_matrix[82] = corner_next
weight_matrix[17] = corner_next
weight_matrix[27] = corner_diagonal
weight_matrix[28] = corner_next
weight_matrix[87] = corner_next
weight_matrix[77] = corner_diagonal
weight_matrix[78] = corner_next
weight_matrix[31] = next_next
weight_matrix[13] = next_next
weight_matrix[33] = diagonal_next
weight_matrix[61] = next_next
weight_matrix[63] = diagonal_next
weight_matrix[83] = next_next
weight_matrix[16] = next_next
weight_matrix[36] = diagonal_next
weight_matrix[38] = next_next
weight_matrix[86] = next_next
weight_matrix[66] = diagonal_next
weight_matrix[68] = next_next
weight_matrix[13] = next_next
weight_matrix[14] = next_next
weight_matrix[15] = next_next
weight_matrix[16] = next_next
weight_matrix[31] = next_next
weight_matrix[41] = next_next
weight_matrix[51] = next_next
weight_matrix[61] = next_next
weight_matrix[83] = next_next
weight_matrix[84] = next_next
weight_matrix[85] = next_next
weight_matrix[86] = next_next
weight_matrix[68] = next_next
weight_matrix[58] = next_next
weight_matrix[48] = next_next
weight_matrix[38] = next_next

print_board(list(weight_matrix.values()))

# my_board = "???????????.....o..??...@o@..??..ooo@o.??..ooo@..??..ooo...??........??........??........???????????"
# print_board(my_board)
# num_periods = count_characters(my_board, ".")
# if num_periods == 25:
#     print("e")
#     value = play(my_board, "@", "e")
# else:
#     print("m")
#     value = play(my_board, "@", "m")
# print(value)
