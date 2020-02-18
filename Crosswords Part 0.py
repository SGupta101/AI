import sys
import time


def fill_string(string, direction, row, col):  # fill crossword with this string
    index = find_index(row, col)
    current_index = index
    length_of_string = len(string)
    if direction == "H":
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


### main
my_size = sys.argv[1]
my_height = int(my_size.split("X")[0])
my_width = int(my_size.split("X")[1])
num_blocked_squares = int(sys.argv[2])
dictionary_file = sys.argv[3]
strings_of_chars = []
my_crossword_string = ""
my_crossword_list = []
for string_of_char in range(4, len(sys.argv)):
    strings_of_chars.append(sys.argv[string_of_char])

string_to_pos = {}

for string_of_char in strings_of_chars:  # string: H/v, row, col
    current_direction = string_of_char[0]
    split_other_attributes = string_of_char[1:].split("X")
    current_row = split_other_attributes[0]
    other_attributes = split_other_attributes[1]
    current_col = ""
    current_index = 0
    for attribute in other_attributes:
        if attribute.isalpha():
            break
        current_col += attribute
        current_index += 1
    current_string = other_attributes[current_index:]
    string_to_pos[current_string] = [current_direction, int(current_row), int(current_col)]

for character in range(0, my_height * my_width):  # fills crossword
    my_crossword_string += "-"

my_crossword_list = list(my_crossword_string)

for current_string in string_to_pos:  # add all the given strings to the crossword
    attributes = string_to_pos[current_string]
    fill_string(current_string, attributes[0], attributes[1], attributes[2])


print_puzzle(my_crossword_list)
