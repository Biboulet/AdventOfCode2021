import os
import utils
import re
import itertools
scans = utils.read_file(os.getcwd() + "\\input.txt")


def add(base_number, number):
    return "[" + base_number + "," + number + "]"


# return the index of the first and last char of the deepest pair
def get_deepest_pair(string):
    depth = 0
    deepest = 0
    pair_start = None
    for i, char in enumerate(string):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1

        if depth > 4:
            if deepest < depth:
                deepest = depth
                pair_start = i

    return pair_start, string.find("]", pair_start)


# return the index of the first digit in the number which has more than 2 digit
def get_closest_splitable(string):
    splitable = re.search(r'\d\d', string)
    if splitable is not None:
        return splitable.start()
    return None


#tuple avec le début et la fin
def find_right_index(base_number, index):
    start_index = None
    end_index = None

    for i, char in enumerate(base_number[index:]):
        if char.isdigit():
            start_index = i +index
            end_index = re.search(r"\D", base_number[i+index:]).start() + index + i
            break

    return start_index, end_index

def remplace_rightmost(base_number, end_index, b):
    right_index = find_right_index(base_number, end_index)
    if right_index[0] is None:
        return base_number
    num = b + int(base_number[right_index[0]:right_index[1]])
    return base_number[:right_index[0]] + str(num) + base_number[right_index[1]:]



def find_left_index(base_number, index):
    start_index = end_index = None
    i = index - 1
    while i > 0:
        char = base_number[i]
        if char.isdigit():

            if start_index is not None:
                start_index = i
                return start_index, end_index+1
            start_index = end_index = i
        else:
            if start_index is not None:
                return start_index, end_index+1

        i-=1
    return None, None


def remplace_leftmost(base_number, start_index, a):
    left_index = find_left_index(base_number, start_index)
    if left_index[0] is None:
        return base_number
    num = a + int(base_number[left_index[0]:left_index[1]])
    return base_number[:left_index[0]] + str(num) + base_number[left_index[1]:]


def remove_deepest_pair(base_number, deepest_pair_index):
    return base_number[:deepest_pair_index[0]] + "0" + base_number[deepest_pair_index[1]+1:]


def get_as_splited(param):
    if param % 2 == 0:
        return "[" + str(param // 2) + "," + str(param // 2) + "]"
    else:
        return "[" + str(param // 2) + "," + str((param // 2) + 1) + "]"


# TODO:ne gère pas les nombres a 3 chiffres
def reduce(base_number):
    deepest_pair_index = get_deepest_pair(base_number)
    closest_splitable_index = get_closest_splitable(base_number)

    while deepest_pair_index[0] is not None or closest_splitable_index is not None:

        # exploding
        if deepest_pair_index[0] is not None:

            pair = base_number[deepest_pair_index[0]:deepest_pair_index[1]+1]
            args = pair.split(",")

            a = int(args[0][1:])
            b = int(args[1][:-1])

            base_number = remplace_rightmost(base_number, deepest_pair_index[1], b)
            base_number = remove_deepest_pair(base_number, deepest_pair_index)
            base_number = remplace_leftmost(base_number, deepest_pair_index[0], a)
        else:

            num = int(base_number[closest_splitable_index:closest_splitable_index + 2])
            base_number = base_number[:closest_splitable_index] + get_as_splited(num) + base_number[
                                                                                        closest_splitable_index + 2:]

        closest_splitable_index = get_closest_splitable(base_number)
        deepest_pair_index = get_deepest_pair(base_number)

    return base_number


def add_numbers(scans):
    base_number = scans[0]
    for number in scans[1:]:
        base_number = add(base_number, number)
        base_number = reduce(base_number)

    return base_number


def magnetude(num):
    if len(num) == 1:
        return int(num)
    if len(num) == 5:
        return int(num[1]) * 3 + int(num[3]) * 2

    a = ""
    b = ""
    depth = 0
    is_first_part = True
    for char in num[1:-1]:
        if depth == 0 and char == ",":
            is_first_part = False
            continue

        if is_first_part:
            a += char
        else:
            b += char

        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1

    return 3 * magnetude(a) + 2 * magnetude(b)


def find_best_combinations(scans):
    combinations = itertools.permutations(scans,2)
    largest_magnetude = 0
    for combination in combinations:
        sum = add_numbers(combination)
        current_magnetude = magnetude(sum)
        if current_magnetude > largest_magnetude:
            largest_magnetude = current_magnetude
    return largest_magnetude

if __name__ == "__main__":
    print(find_best_combinations(scans))
