import sys
import time


def fill_string(string, direction, row, col):  # fill crossword with this string
    index = find_index(row, col)
    current_index = index
    length_of_string = len(string)
    if direction == "h":
        for c in range(length_of_string):
            my_crossword_list[current_index] = string[c]
            current_index += 1
    else:
        for c in range(length_of_string):
            my_crossword_list[current_index] = string[c]
            current_index += my_width


def find_index(row, column):
    index = my_width * row + column
    return index


def find_pos(index):
    row = int(index / my_width)
    column = index - row * my_width
    return [row, column]


def print_puzzle(puzzle):
    pretty_puzzle = ""
    for row in range(0, my_height):
        for column in range(0, my_width):
            index = find_index(row, column)
            pretty_puzzle += puzzle[index] + " "
        pretty_puzzle += "\n"
    print(pretty_puzzle)


def get_possible_vars(state):
    indexes = []
    for cell in range(len(state)):
        if state[cell] == "-":
            indexes.append(cell)
    return indexes

def valid_index(index):
    if index >= my_height * my_width:
        return False
    if index < 0:
        return False
    return True


def csp_backtracking(board, block_indexes):
    if board.count("#") == num_blocked_squares:
        return board
    values = get_possible_vars(board)
    for val in values:
        new_board = board.copy()
        new_block_indexes = block_indexes.copy()
        new_block_indexes.add(val)
        new_board[val] = "#"
        new_board_and_indexes = implied_blocks(new_board, new_block_indexes)
        if new_board_and_indexes is not None:
            new_board_implied = new_board_and_indexes[0]
            new_indexes_implied = new_board_and_indexes[1]
            if new_board_implied.count("#") <= num_blocked_squares and check_connected(new_board):
                result = csp_backtracking(new_board_implied, new_indexes_implied)
                return result
    # print("var:", var)
    # print(new_block_indexes)
    # print_puzzle(new_board)



def implied_blocks(board, block_indexes):
    change = True
    new_board = board
    new_indexes = block_indexes
    before_indexes = block_indexes.copy()
    num_letters_before = 0
    for cell in board:
        if cell.isalpha():
            num_letters_before += 1
    while change:
        new_board_and_indexes = blocks_next_to(new_board, new_indexes)
        new_board = new_board_and_indexes[0]
        new_indexes = new_board_and_indexes[1]
        new_board_and_indexes = make_symmetric(new_board, new_indexes)
        new_board = new_board_and_indexes[0]
        new_indexes = new_board_and_indexes[1]
        if new_indexes == before_indexes:
            change = False
        before_indexes = new_indexes.copy()
    num_letters_after = 0
    for cell in board:
        if cell.isalpha():
            num_letters_after += 1
    if num_letters_before == num_letters_after:
        return new_board, new_indexes
    else:
        return None


def blocks_next_to(board, block_indexes):  # places blocks where no legal word can be made
    added_block_indexes = set()
    for index in block_indexes:
        index_row_and_column = find_pos(index)
        index_row = index_row_and_column[0]
        index_col = index_row_and_column[1]
        new_index = index + 1
        if valid_index(new_index) and not board[new_index].isalpha() and find_pos(new_index)[1] == my_width - 1:
            board[new_index] = "#"
            added_block_indexes.add(new_index)
            # print("a", new_index)
        new_index = index + 2
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if column == my_width - 1 or row == index_row and board[new_index] == "#":
                new_block_index = index + 1
                board[new_block_index] = "#"
                board[new_block_index + 1] = "#"
                added_block_indexes.add(new_block_index)
                added_block_indexes.add(new_block_index + 1)
                # print("b", new_block_index)
                # print("c", new_block_index + 1)
        new_index = index + 3
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if row == index_row and board[new_index] == "#":
                new_block_index = index + 1
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("d", new_block_index)
                new_block_index = index + 2
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("e", new_block_index)
        new_index = index - 1
        if valid_index(new_index):
            if find_pos(new_index)[1] == 0:
                board[new_index] = "#"
                added_block_indexes.add(new_index)
                # print("f", new_index)
        new_index = index - 2
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if column == 0 or row == index_row and board[new_index] == "#":
                new_block_index = index - 1
                board[new_block_index] = "#"
                board[new_block_index - 1] = "#"
                added_block_indexes.add(new_block_index)
                added_block_indexes.add(new_block_index - 1)
                # print("g", new_block_index)
                # print("h", new_block_index-1)
        new_index = index - 3
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if row == index_row and board[new_index] == "#":
                new_block_index = index - 1
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("i", new_block_index)
                new_block_index = index - 2
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("j", new_block_index)
        new_index = index + my_width
        if valid_index(new_index):
            if find_pos(new_index)[0] == my_height - 1:
                board[new_index] = "#"
                added_block_indexes.add(new_index)
                # print("k", new_index)
        new_index = index + (my_width * 2)
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if row == my_height - 1 or column == index_col and board[new_index] == "#":
                new_block_index = index + my_width
                board[new_block_index] = "#"
                board[new_block_index + my_width] = "#"
                added_block_indexes.add(new_block_index)
                added_block_indexes.add(new_block_index + my_width)
                # print("l", new_block_index)
                # print("m", new_block_index + my_width)
        new_index = index + (my_width * 3)
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if column == index_col and board[new_index] == "#":
                new_block_index = index + my_width
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("n", new_block_index)
                new_block_index = index + (my_width * 2)
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("o", new_block_index)
        new_index = index - my_width
        if valid_index(new_index):
            if find_pos(new_index)[0] == 0:
                board[new_index] = "#"
                added_block_indexes.add(new_index)
                # print("p", new_index)
        new_index = index - (my_width * 2)
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if row == 0 or column == index_col and board[new_index] == "#":
                new_block_index = index - my_width
                board[new_block_index] = "#"
                board[new_block_index - my_width] = "#"
                added_block_indexes.add(new_block_index)
                added_block_indexes.add(new_block_index - my_width)
                # print("q", new_block_index)
                # print("r", new_block_index - (my_width*2))
        new_index = index - (my_width * 3)
        new_index_row_and_col = find_pos(new_index)
        column = new_index_row_and_col[1]
        row = new_index_row_and_col[0]
        if valid_index(new_index):
            if column == index_col and board[new_index] == "#":
                new_block_index = index - my_width
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("s", new_block_index)
                new_block_index = index - (my_width * 2)
                board[new_block_index] = "#"
                added_block_indexes.add(new_block_index)
                # print("t", new_block_index)
    return board, block_indexes.union(added_block_indexes)


def make_symmetric(board, block_indexes):
    added_block_indexes = set()
    for index in block_indexes:
        new_index = len(board) - ((-index - 1) * -1)
        board[new_index] = "#"
        added_block_indexes.add(new_index)
    return board, block_indexes.union(added_block_indexes)


def check_connected(
        board):  # use area fill, if the whole board is not made up of # and the replaced character, then everything is not connected
    area_fill_board = board.copy()
    index_of_space = area_fill_board.index("-")
    row_and_col = find_pos(index_of_space)
    area_fill_two(area_fill_board, row_and_col[0], row_and_col[1], "-")
    if "-" in area_fill_board:
        return False
    return True


def area_fill_two(board, r, c, ch):
    # print("r:", r, "c:", c, "board:", board)
    if r < 0 or r >= my_height:
        return
    if c < 0 or c >= my_width:
        return
    index = find_index(r, c)
    value = board[index]
    if value == "*" or value == "#" or value.isalpha():
        return
    if value == ch:
        board[index] = "*"
    area_fill_two(board, r + 1, c, ch)
    area_fill_two(board, r - 1, c, ch)
    area_fill_two(board, r, c + 1, ch)
    area_fill_two(board, r, c - 1, ch)


def area_fill(board, r, c, ch):
    # print("r:", r, "c:", c, "board:", board)
    if r < 0 or r >= my_height:
        return
    if c < 0 or c >= my_width:
        return
    index = find_index(r, c)
    replace_char = board[index]
    if board[index] == ch:
        replace_char = "*"
    if board[index] == " ":
        return
    board[index] = " "
    area_fill(board, r - 1, c, ch)
    area_fill(board, r + 1, c, ch)
    area_fill(board, r, c - 1, ch)
    area_fill(board, r, c + 1, ch)
    board[index] = replace_char


### main
my_size = sys.argv[1].lower()
my_height = int(my_size.split("x")[0])
my_width = int(my_size.split("x")[1])
num_blocked_squares = int(sys.argv[2])
dictionary_file = sys.argv[3]
strings_of_chars = []
my_crossword_string = ""
my_crossword_list = []
for string_of_char in range(4, len(sys.argv)):
    strings_of_chars.append(sys.argv[string_of_char].lower())

string_to_pos = {}
my_block_indexes = set()
for string_of_char in strings_of_chars:  # string: H/v, row, col
    current_direction = string_of_char[0]
    split_other_attributes = string_of_char[1:].split("x")
    current_row = split_other_attributes[0]
    other_attributes = split_other_attributes[1]
    current_col = ""
    current_index = 0
    for attribute in other_attributes:
        if attribute.isalpha() or attribute == "#":
            break
        current_col += attribute
        current_index += 1
    current_string = other_attributes[current_index:]
    string_to_pos[(int(current_row), int(current_col), current_direction)] = current_string

all_blocks = False
if len(strings_of_chars) == 0 and num_blocked_squares == my_height * my_width:
    for character in range(0, my_height * my_width):  # fills crossword
        my_crossword_string += "#"
        my_block_indexes.add(character)
    print(my_crossword_string)


else:
    for character in range(0, my_height * my_width):  # fills crossword
        my_crossword_string += "-"

    my_crossword_list = list(my_crossword_string)

    for current_pos in string_to_pos:  # add all the given strings to the crossword
        current_string = string_to_pos[current_pos]
        current_row = current_pos[0]
        current_col = current_pos[1]
        current_direction = current_pos[2]
        index = find_index(current_row, current_col)
        for piece in current_string:
            if piece == "#":
                my_block_indexes.add(index)
            index += 1
        fill_string(current_string, current_direction, current_row, current_col)

    if (my_height*my_width) % 2 == 1 and num_blocked_squares % 2 == 1:  # checks whether num_blocks is odd/even and places block at center based on that
        index_of_middle = find_index(int(my_height / 2), int(my_width / 2))
        my_crossword_list[index_of_middle] = "#"
        my_block_indexes.add(index_of_middle)

    final_crossword = csp_backtracking(my_crossword_list, my_block_indexes)
    print("".join(final_crossword))

