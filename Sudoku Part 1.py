import sys


def find_pos(index, s):
    this_row = int(index / s)
    this_column = index - this_row * s
    return [this_row, this_column]


def find_index(this_row, this_column, s):
    index = s * this_row + this_column
    return index


def find_block(rowcol, height, width):
    return [rowcol[0] // height, rowcol[1] // width]


def print_puzzle(s, puzzle, height, width):
    matrix = ""
    for row in range(0, s):
        for column in range(s * row, s * row + s):
            matrix += puzzle[column]
            if column != s - 1:
                matrix += " "
            if column != s and (column + 1) % width == 0:
                matrix += "| "
        if row != s - 1:
            matrix += "\n"
            if (row + 1) % height == 0:
                for i in range(0, s):
                    if i != 0 and (i + 1) % width == 0:
                        matrix += "-   "
                    else:
                        matrix += "- "
                matrix += "\n"
    print(matrix)


def instances(puzzle):
    num_instances = {}
    for symbol in symbol_set:
        num_instances[symbol] = 0
    num_instances["."] = 0
    for piece in puzzle:
        n = num_instances[piece]
        num_instances[piece] = n + 1
    return num_instances


def get_symbol_set(size):
    sorted_values = set()
    abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    if size > 9:
        for j in range(1, 10):
            sorted_values.add(str(j))
        for j in range(0, size - 9):
            sorted_values.add(abc[j])
    else:
        for j in range(1, size + 1):
            sorted_values.add(str(j))
    return sorted_values


def get_next_unassigned_var(state):
    return state.index(".")


def get_sorted_values(state, var, size):
    sorted_values = set()
    for symbol in symbol_set:
        sorted_values.add(symbol)
    for neighbor in neighbors[var]:
        # n = my_puzzle[neighbor]
        n = state[neighbor]
        if n in sorted_values:
            sorted_values.remove(n)
    sorted_values = list(sorted_values)
    sorted_values.sort()
    return sorted_values


def backtracking(state, size):
    if "." not in state:
        return state
    var = get_next_unassigned_var(state)
    possible_values = get_sorted_values(state, var, size)
    new_state = []
    for k in range(len(state)):
        new_state.append(state[k])
    for val in possible_values:
        new_state[var] = val
        result = backtracking(new_state, size)
        if result is not None:
            return result
    return None


# my_puzzle = "...976532.5.123478.3.854169948265317275341896163798245391682754587439621426517983"
# print_puzzle(9, my_puzzle, 3, 3)
counter = 0
with open(sys.argv[1]) as f:
    for line in f:
        my_puzzle = line.strip()
        N = int(len(my_puzzle) ** (1 / 2))
        sqr_N = N ** (1 / 2)
        subblock_height = 0
        subblock_width = 0
        if sqr_N == int(sqr_N):
            subblock_height = int(sqr_N)
            subblock_width = int(sqr_N)
        else:
            subblock_height = []
            for i in range(1, N+1):
                factor = i
                if int(N / i) == N / i:
                    if i < N ** (1 / 2):
                        subblock_height.append(i)
                    else:
                        subblock_width = i
                        break
            subblock_height = subblock_height[len(subblock_height) - 1]
        rows = []
        columns = []
        blocks = []
        for i in range(0, subblock_height):
            for j in range(0, subblock_width):
                blocks.append([])

        for i in range(0, N):
            my_row = set()
            my_column = set()
            for r in range(N * i, N * i + N):
                my_row.add(r)
            for c in range(i, len(my_puzzle), N):
                my_column.add(c)
            rows.append(my_row)
            columns.append(my_column)

        for w in range(0, N, subblock_width):
            for h in range(w, N * N, N * subblock_height):
                block = set()
                for y in range(h, h + N * (subblock_height - 1) + 1, N):
                    for x in range(y, y + subblock_width):
                        # print(width, height, y, x, my_puzzle[x])
                        block.add(x)
                blocks.append(block)
        # print(blocks)

        neighbors = {}
        # print("rows", rows)
        # print("cols", columns)
        # print("blocks", blocks)
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
            for block in blocks:
                if i in block:
                    for b in block:
                        neighbors[i].add(b)
            neighbors[i].remove(i)
        symbol_set = get_symbol_set(N)
        finished_puzzle = backtracking(list(my_puzzle), 9)
        if finished_puzzle is None:
            print("None")
        finished_string = ""
        for p in finished_puzzle:
            finished_string += p
        # print_puzzle(N, finished_string, subblock_height, subblock_width)
        num_symbols = instances(finished_string)
        isCorrect = True
        for sy in num_symbols.keys():
            num = num_symbols[sy]
            if sy != "." and num != N:
                isCorrect = False
        # print(isCorrect)
        # print_puzzle(N, finished_string, subblock_height, subblock_width)
        # print(isCorrect)
        print(finished_string)