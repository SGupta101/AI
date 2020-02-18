import sys
import random


def count_characters(puzzle, c):
    countt = 0
    for p in puzzle:
        if p == c:
            countt += 1
    return countt


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


board1 = "???????????........??........??...@....??...@@...??...@o...??........??........??........???????????"
board2 = move(board1, '@', 34)
board3 = move(board2, 'o', 53)
board4 = move(board3, '@', 63)
board5 = move(board4, 'o', 73)
board6 = move(board5, '@', 72)
board7 = move(board6, 'o', 33)
board8 = move(board7, '@', 43)
board9 = move(board8, 'o', 35)
board10 = move(board9, '@', 66)
board11 = move(board10, 'o', 52)
board12 = move(board11, '@', 26)
board13 = move(board12, 'o', 81)
my_board = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"
count = 0
indexes = []
white_pass = False
black_pass = False
while "." in my_board:
    if black_pass and white_pass:
        break
    token_name = ""
    if count % 2 == 0:
        my_token = "@"
        token_name = "black"
    else:
        my_token = "o"
        token_name = "white"
    print_board(my_board)
    blacks = count_characters(my_board, "@")
    print("blacks:", blacks)
    whites = count_characters(my_board, "o")
    print("whites:", whites)
    valid_moves = possible_moves(my_board, my_token)
    if len(valid_moves) == 0:
        print("no valid moves")
        print("pass\n")
        indexes.append(-1)
        if my_token == "@":
            black_pass = True
        else:
            white_pass = True
    else:
        black_pass = False
        white_pass = False
        print(token_name, "possible moves:", valid_moves)
        choice = random.choice(valid_moves)
        print("choice:", choice, "\n")
        my_board = move(my_board, my_token, choice)
        indexes.append(choice)
    count += 1

print_board(my_board)
blacks = count_characters(my_board, "@")
print("blacks:", blacks)
whites = count_characters(my_board, "o")
print("whites:", whites)
white_percentage = count_characters(my_board, "o") / 64
black_percentage = count_characters(my_board, "@") / 64
print("percent black:", black_percentage)
print("percent white:", white_percentage)
print(indexes)
