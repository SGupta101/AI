import sys
import time


def state_equal_board(state, board):
    for ind in range(len(state)):
        if state[ind] != "." and state[ind] != board[ind]:
            return False
    return True


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


def forward_looking(board, state, list_indexes):
    if not state_equal_board(state, board):
        print_puzzle(N, "".join(state), subblock_height, subblock_width)
        print("line 176")
        input()
    print_puzzle(N, "".join(state), subblock_height, subblock_width)
    print("line 176")
    if list_indexes is None:
        one_solution = []
        for key in board.keys():
            val = board[key]
            if len(val) == 1:
                one_solution.append(key)
                state[key] = val
                print_puzzle(N, "".join(state), subblock_height, subblock_width)
                print("line 188")
    else:
        one_solution = []
        for index in list_indexes:
            one_solution.append(index)
    for one in one_solution:
        # print("one_index, one:", one, state[one])
        for neighbor in neighbors[one]:
            possibility = board[neighbor]
            # print("one_index, one, neighbor, possibility:", one, state[one], neighbor, possibility)
            constraint = state[one]
            if constraint in possibility:
                # print("constraint:", constraint)
                possibility = possibility.replace(constraint, "")
                # print("board \n one_index, constraint, neighbor, possibility:", board, one, constraint, neighbor,
                #       possibility)
                if len(possibility) == 0:
                    return None
                board[neighbor] = possibility
                if len(possibility) == 1:
                    state[neighbor] = possibility
                    one_solution.append(neighbor)
                    if not state_equal_board(state, board):
                        print_puzzle(N, "".join(state), subblock_height, subblock_width)
                        print("line 210")
                        input()
                    print_puzzle(N, "".join(state), subblock_height, subblock_width)
                    print(board)
                    print("line 213")
    return board, state


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
        board_and_state = forward_looking(new_board, new_state, [var])
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
    if not check_test(state, None):
        print_puzzle(N, "".join(state), subblock_height, subblock_width)
        print("line 242")
        input()
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
            if not check_test(state, None):
                print_puzzle(N, "".join(checked_state), subblock_height, subblock_width)
                print("line 259")
                input()
            # print("var, val:", var, val)
            # print("new_board:", new_board)
            # print("checked_board:", checked_board)
            result = csp_backtracking_with_cp(checked_board, checked_state)
            if result is not None:
                return result
    return None


def constraint_propagation(board, state):
    if not state_equal_board(state, board):
        print_puzzle(N, "".join(state), subblock_height, subblock_width)
        print("line 273")
        input()
    print_puzzle(N, "".join(state), subblock_height, subblock_width)
    print(board)
    print("line 290")
    # print("csp")
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
                        state[index_num] = piece
                        board[index_num] = piece
                        changes.add(index_num)
                        current_changes.add(piece)
                        if not state_equal_board(state, board):
                            print_puzzle(N, "".join(state), subblock_height, subblock_width)
                            print(board)
                            print("piece to index:", piece_to_index)
                            print("line 316")
                            input()

                    print_puzzle(N, "".join(state), subblock_height, subblock_width)
                    print(board)
                    print("piece to index:", piece_to_index)
                    print("line 321")
                    # if piece in assign_vals:
                    #     board_and_state = forward_looking(board, state, None)
                    #     if board_and_state is not None:
                    #         board = board_and_state[0]
                    #         state = board_and_state[1]
                    #     else:
                    #         return None
                    # assign_vals.add(piece)
                    change = True
    # print("state after cp:", new_state)
    print("changes:", changes)
    if not state_equal_board(state, board):
        print_puzzle(N, "".join(state), subblock_height, subblock_width)
        print("line 336")
        input()
        print("board before:", board)
    board_and_state = forward_looking(board, state, changes)
    if board_and_state is not None:
        if not state_equal_board(board_and_state[1], board_and_state[0]):
            print_puzzle(N, "".join(board_and_state[1]), subblock_height, subblock_width)
            print("line 342")
            input()
        # print("state after csp and fl:", new_state)
        print("change:", change)
        board = board_and_state[0]
        state = board_and_state[1]
    return board, state


def csp_backtracking_with_fl_and_cp(board, state):
    if not state_equal_board(state, board):
        print_puzzle(N, "".join(state), subblock_height, subblock_width)
        print("line 412")
        input()
    if "." not in state:
        return state
    var = get_most_constrained_var(board)
    for val in get_sorted_values(state, var, len(state)):
        new_state = state.copy()
        new_board = board.copy()
        new_state[var] = val
        new_board[var] = val
        if not state_equal_board(new_state, new_board):
            print_puzzle(N, "".join(new_state), subblock_height, subblock_width)
            print("line 427")
            input()
        board_and_state = forward_looking(new_board, new_state, [var])
        if board_and_state is not None:
            checked_board = board_and_state[0]
            checked_state = board_and_state[1]
            if not state_equal_board(checked_state, checked_board):
                print_puzzle(N, "".join(checked_state), subblock_height, subblock_width)
                print("line 435")
                input()
            board_and_state = constraint_propagation(checked_board, checked_state)
            if board_and_state is not None:
                checked_board = board_and_state[0]
                checked_state = board_and_state[1]
                if not state_equal_board(checked_state, checked_board):
                    print_puzzle(N, "".join(checked_state), subblock_height, subblock_width)
                    print("line 443")
                    input()
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
for i in range(1, 2):
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
            for space in range(len(my_puzzle_list)):
                if my_puzzle_list[space] != ".":
                    # my_possibilities[space] = ''.join([my_puzzle_list[space]])
                    my_possibilities[space] = my_puzzle_list[space]
                else:
                    my_possibilities[space] = "".join(get_sorted_values(my_puzzle_list, space, N))
            # print(my_possibilities)
            my_state = list(my_puzzle)
            my_board_and_state = forward_looking(my_possibilities, list(my_puzzle), None)
            if my_board_and_state is None:
                my_checked_board = None
                my_checked_state = None
            else:
                my_checked_board = my_board_and_state[0]
                my_checked_state = my_board_and_state[1]
            # print("b:", my_checked_board)
            # print("s:", my_checked_state)
            if my_board_and_state is not None and "." not in my_checked_state:
                # print("forward looking:")
                finished_puzzle = my_checked_state
            else:
                # print("needs csp")
                if my_board_and_state is None:
                    # print(my_possibilities)
                    finished_puzzle = csp_backtracking_with_fl_and_cp(my_possibilities, my_state)
                else:
                    # print(my_checked_board)
                    finished_puzzle = csp_backtracking_with_fl_and_cp(my_checked_board, my_checked_state)
                if finished_puzzle is None:
                    print("None")
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
