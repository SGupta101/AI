import sys
import time


def check_test(puzzle, finished):
    for row in rows:
        num_instances = {}
        for symbol in symbol_set:
            num_instances[symbol] = 0
        num_periods = 0
        for index in row:
            if puzzle[index] == ".":
                num_periods += 1
            else:
                num_instances[puzzle[index]] += 1
        if finished:
            if num_periods > 0:
                print("too many periods")
                return False
            # print(num_instances.values())
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
            if puzzle[index] == ".":
                num_periods += 1
            else:
                num_instances[puzzle[index]] += 1
        if finished:
            if num_periods > 0:
                print("too many periods")
                return False
            # print(num_instances.values())
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
            if puzzle[index] == ".":
                num_periods += 1
            else:
                num_instances[puzzle[index]] += 1
        if finished:
            if num_periods > 0:
                print("too many periods")
                return False
            # print(num_instances.values())
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


def print_puzzle(s, puzzle, height, width):
    print("puzzle:", puzzle)
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


def test():
    a = [1, 2, 3]
    b = [4, 5, 6, 7]  # [5, 6]

    a.extend(b[1:3])  # [1, 2, 3, 5, 6]


def instances(puzzle):
    num_instances = {}
    for symbol in symbol_set:
        num_instances[symbol] = 0
    num_instances["."] = 0
    for piece in puzzle:
        num_instances[piece] += 1
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


def get_next_unassigned_var(state):
    return state.index(".")


def get_sorted_values(state, var, size):
    sorted_values = set()
    sorted_values.update(symbol_set)
    for neighbor in neighbors[var]:
        # n = my_puzzle[neighbor]
        n = state[neighbor]
        if n in sorted_values:
            sorted_values.remove(n)
    sorted_values = list(sorted_values)
    sorted_values.sort()
    return sorted_values


def csp_backtracking(state, size):
    if "." not in state:
        return state
    var = get_next_unassigned_var(state)
    possible_values = get_sorted_values(state, var, size)
    new_state = state.copy()
    for val in possible_values:
        new_state[var] = val
        result = csp_backtracking(new_state, size)
        if result is not None:
            return result
    return None


def forward_looking(board, state, index):
    new_board = board
    new_state = state
    if index is None:
        one_solution = []
        for key in new_board.keys():
            val = new_board[key]
            if len(val) == 1:
                one_solution.append(key)
                new_state[key] = val
    else:
        one_solution = [index]
    for one in one_solution:
        # print("one_index, one:", one, state[one])
        for neighbor in neighbors[one]:
            possibility = new_board[neighbor]
            # print("one_index, one, neighbor, possibility:", one, state[one], neighbor, possibility)
            constraint = new_state[one]
            if constraint in possibility:
                # print("constraint:", constraint)
                new_board[neighbor] = possibility.replace(constraint, "")
                possibility = new_board[neighbor]
                # print("board \n one_index, constraint, neighbor, possibility:", board, one, constraint, neighbor,
                #       possibility)
                if len(possibility) == 0:
                    return None
                if len(possibility) == 1:
                    new_state[neighbor] = possibility
                    one_solution.append(neighbor)
    return new_board, new_state


def get_most_constrained_var(board):
    most_constrained_index = 0
    num_possibilities = 1000
    for var in board:
        constraints = len(board[var])
        if 1 < constraints < num_possibilities:
            num_possibilities = constraints
            most_constrained_index = var
    return most_constrained_index


def csp_backtracking_with_forward_looking(board, state):
    if "." not in state:
        return state
    var = get_most_constrained_var(board)
    new_state = []
    for val in get_sorted_values(state, var, len(state)):
        new_state = state.copy()
        new_board = board.copy()
        new_state[var] = val
        new_board[var] = val
        board_and_state = forward_looking(new_board, new_state, var)
        if board_and_state is not None:
            checked_board = board_and_state[0]
            checked_state = board_and_state[1]
            # print("var, val:", var, val)
            # print("new_board:", new_board)
            # print("checked_board:", checked_board)
            result = csp_backtracking_with_forward_looking(checked_board, checked_state)
            if result is not None:
                return result
    return None


def csp_backtracking_with_cp(board, state):
    if "." not in state:
        return state
    var = get_most_constrained_var(board)
    new_state = []
    for val in get_sorted_values(state, var, len(state)):
        new_state = state.copy()
        new_board = board.copy()
        new_state[var] = val
        new_board[var] = val
        board_and_state = constraint_propagation(new_board, new_state)
        if board_and_state is not None:
            checked_board = board_and_state[0]
            checked_state = board_and_state[1]
            # print("var, val:", var, val)
            # print("new_board:", new_board)
            # print("checked_board:", checked_board)
            result = csp_backtracking_with_cp(checked_board, checked_state)
            if result is not None:
                return result
    return None


def constraint_propagation(board, state):
    # print("csp")
    change = False
    assign_vals = set()
    all_indiv = [rows, columns, blocks]
    for indivs in all_indiv:
        for indiv in indivs:
            piece_to_index = {}
            for index in indiv:
                for val in board[index]:
                    if val not in piece_to_index.keys():
                        piece_to_index[val] = []
                    piece_to_index[val].append(index)
            for piece in piece_to_index.keys():
                index = piece_to_index[piece]
                if len(index) == 0:
                    return None
                if len(index) == 1:
                    index_num = index[0]
                    state[index_num] = piece
                    board[index_num] = piece
                    if piece in assign_vals:
                        board_and_state = forward_looking(board, state, None)
                        if board_and_state is not None:
                            board = board_and_state[0]
                            state = board_and_state[1]
                        else:
                            return None
                    assign_vals.add(piece)
                    change = True
    # print("state after cp:", new_state)
    # if change:
    #     board_and_state = forward_looking(board, state, None)
    #     if board_and_state is not None:
    #         # print("state after csp and fl:", new_state)
    #         return board_and_state
    return board, state


def constraint_propagation_constrained(board, state):
    periods_to_row = {}
    for row in rows:
        num_periods = 0
        for index in row:
            if state[index] == ".":
                num_periods += 1
        if num_periods not in periods_to_row.keys():
            periods_to_row[num_periods] = []
        periods_to_row[num_periods].append(row)
    periods_to_column = {}
    for col in columns:
        num_periods = 0
        for index in col:
            if state[index] == ".":
                num_periods += 1
        if num_periods not in periods_to_column.keys():
            periods_to_column[num_periods] = []
        periods_to_column[num_periods].append(col)
    periods_to_block = {}
    for block in blocks:
        num_periods = 0
        for index in block:
            if state[index] == ".":
                num_periods += 1
        if num_periods not in periods_to_block.keys():
            periods_to_block[num_periods] = []
        periods_to_block[num_periods].append(block)
    # print("csp")
    change = False
    assign_vals = set()
    all_indiv = [sorted(periods_to_row.keys()), sorted(periods_to_column.keys()), sorted(periods_to_block.keys())]
    count = 1
    for indivs in all_indiv:
        for indiv in indivs:
            if count == 1:
                constrained_indivs = []
                for row in periods_to_row[indiv]:
                    constrained_indivs.append(row)
            if count == 2:
                constrained_indivs = []
                for col in periods_to_column[indiv]:
                    constrained_indivs.append(col)
            if count == 3:
                constrained_indivs = []
                for b in periods_to_block[indiv]:
                    constrained_indivs.append(b)
            piece_to_index = {}
            for constrained_indiv in constrained_indivs:
                for index in constrained_indiv:
                    for val in board[index]:
                        if val not in piece_to_index.keys():
                            piece_to_index[val] = [index]
                        else:
                            piece_to_index[val].append(index)
                for piece in piece_to_index.keys():
                    index = piece_to_index[piece]
                    if len(index) == 0:
                        return None
                    if len(index) == 1:
                        index_num = index[0]
                        state[index_num] = piece
                        board[index_num] = piece
                        # if piece in assign_vals:
                        #     board_and_state = forward_looking(board, state, None)
                        #     if board_and_state is not None:
                        #         board = board_and_state[0]
                        #         state = board_and_state[1]
                        #     else:
                        #         return None
                        # assign_vals.add(piece)
                        for neighbor in neighbors[index_num]:
                            if piece in board[neighbor]:
                                board[neighbor].replace(piece, "")
                        change = True
        count += 1
    ###### print("state after cp:", new_state)
    # if change:
    #     board_and_state = forward_looking(board, state, None)
    #     if board_and_state is not None:
    #         # print("state after csp and fl:", new_state)
    #         return board_and_state
    # return board, state


def csp_backtracking_with_fl_and_cp(board, state):
    if "." not in state:
        return state
    var = get_most_constrained_var(board)
    new_state = []
    for val in get_sorted_values(state, var, len(state)):
        new_state = state.copy()
        new_board = board.copy()
        new_state[var] = val
        new_board[var] = val
        board_and_state = forward_looking(new_board, new_state, var)
        if board_and_state is not None:
            checked_board = board_and_state[0]
            checked_state = board_and_state[1]
            board_and_state = constraint_propagation(checked_board, checked_state)
            if board_and_state is not None:
                checked_board = board_and_state[0]
                checked_state = board_and_state[1]
                # print("state:", state)
                # print("new state", new_state)
                # print("checked state:", checked_state)
                # print("var, val:", var, val)
                # print("new_board:", new_board)
                # print("checked_board:", checked_board)
                result = csp_backtracking_with_fl_and_cp(checked_board, checked_state)
                if result is not None:
                    return result
    return None


# my_puzzle = "...976532.5.123478.3.854169948265317275341896163798245391682754587439621426517983"
# print_puzzle(9, my_puzzle, 3, 3)
ever_false = False
all_time = 0
counter = 0
start_time = time.perf_counter()
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
            for i in range(1, N + 1):
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
        # get neighbors
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
        my_puzzle_list = list(my_puzzle)
        print(my_puzzle)
        # part 2
        my_possibilities = {}
        # print_puzzle(N, my_puzzle, subblock_height, subblock_width)
        # for space in range(len(my_puzzle_list)):
        #     if my_puzzle_list[space] != ".":
        #         # my_possibilities[space] = ''.join([my_puzzle_list[space]])
        #         my_possibilities[space] = my_puzzle_list[space]
        #     else:
        #         my_possibilities[space] = "".join(get_sorted_values(my_puzzle_list, space, N))
        for i in range(0, N*N):
            my_possibilities[i] = "1234"
        my_possibilities[0] = "1"
        my_possibilities[1] = "12"
        my_possibilities[2] = "123"
        my_possibilities[3] = "1234"
        # print(my_possibilities)
        my_state = list(my_puzzle)
        my_board_and_state = forward_looking(my_possibilities, list(my_puzzle), None)
        finished_puzzle = my_board_and_state[1]
        # if my_board_and_state is None:
        #     my_checked_board = None
        #     my_checked_state = None
        # else:
        #     my_checked_board = my_board_and_state[0]
        #     my_checked_state = my_board_and_state[1]
        # # print("b:", my_checked_board)
        # # print("s:", my_checked_state)
        # if my_board_and_state is not None and "." not in my_checked_state:
        #     # print("forward looking:")
        #     finished_puzzle = my_checked_state
        # else:
        #     # print("needs csp")
        #     if my_board_and_state is None:
        #         # print(my_possibilities)
        #         finished_puzzle = constraint_propagation(my_possibilities, my_state)[1]
        #         #finished_puzzle = csp_backtracking_with_cp(my_possibilities, my_state)
        #     else:
        #         # print(my_checked_board)
        #         finished_puzzle = constraint_propagation(my_checked_board, my_checked_state)[1]
        #         # finished_puzzle = csp_backtracking_with_cp(my_checked_board, my_checked_state)
        #     if finished_puzzle is None:
        #         print("None")
        finished_string = ""
        for p in finished_puzzle:
            finished_string += p
        num_symbols = instances(finished_string)
        isCorrect = True
        for sy in num_symbols.keys():
            num = num_symbols[sy]
            if sy != "." and num != N:
                isCorrect = False
        # print("\n", "\n", "\n")
        # print_puzzle(N, my_puzzle, subblock_height, subblock_width)
        print_puzzle(N, finished_string, subblock_height, subblock_width)
        print(check_test(finished_string, True))
        if not check_test(finished_puzzle, True):
            ever_false = finished_string
        print("\n")
end = time.perf_counter()
total_time = end - start_time
all_time += total_time
print("this is wrong")
if not ever_false:
    print("never")
else:
    print_puzzle(N, ever_false, subblock_height, subblock_width)
print(all_time)
