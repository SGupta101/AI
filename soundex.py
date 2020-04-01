def soundex(name):
    list_name = list(name)
    new_name = []
    for letter in list_name:
        new_name.append(letter)
    for i in range(1, len(list_name)):
        letter = new_name[i]
        if letter in ["a", "e", "i", "o", "u", "y"]:
            new_name[i] = 0
    letters_one = ["b", "f", "p", "v"]
    letters_two = ["c", "g", "j", "k", "q", "s", "x", "z"]
    letters_three = ["d", "t"]
    letters_four = ["l"]
    letters_five = ["m", "n"]
    letters_six = ["r"]
    for i in range(1, len(list_name)):
        letter = new_name[i]
        if letter in letters_one:
            new_name[i] = 1
        elif letter in letters_two:
            new_name[i] = 2
        elif letter in letters_three:
            new_name[i] = 3
        elif letter in letters_four:
            new_name[i] = 4
        elif letter in letters_five:
            new_name[i] = 5
        elif letter in letters_six:
            new_name[i] = 6
    i = 0
    for curr_char in new_name:
        str_curr_char = str(curr_char)
        if not str_curr_char.isalpha():
            for k in range(i, len(new_name)):
                if new_name[k] == curr_char:
                    new_name[k] = 0
            else:
                break
        i += 1
    new_name_two = []
    for curr_char in new_name:
        if curr_char != 0:
            new_name_two.append(curr_char)
    prev_char = new_name_two[0]
    for i in range(1, len(new_name_two) - 1):
        if new_name_two[i] in ["h", "w"]:
            if prev_char == new_name_two[i + 1]:
                new_name_two[i + 1] = 0
            new_name_two[i] = 0
        prev_char = new_name_two[i]
    new_name = []
    for curr_char in new_name_two:
        if curr_char != 0:
            new_name.append(curr_char)
    new_name_str = "".join(new_name)
    numbers = sum(c.isdigit() for c in new_name_str)
    new_name_two = []
    num_numbers = 0
    if numbers >= 4:
        for curr_char in new_name:
            str_curr_char = str(curr_char)
            if not str_curr_char.isalpha():
                num_numbers += 1
            if num_numbers == 4:
                break
            new_name_two.append(curr_char)
    if numbers < 3:
        needed_numbers = 3 - numbers
        for k in range(needed_numbers):
            new_name_two.append(0)
    return "".join(new_name_two)


print(soundex("Robert"))
