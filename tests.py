def try_func(board):
    board.append(5)
    return board


current_list = [2, 3, 4]
before_list = current_list
current_list = try_func(current_list)
print(before_list)
print(current_list)
