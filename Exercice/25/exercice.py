import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")
Height = len(scans)
Length = len(scans[0])


def right_char(index):
    if index % Length == Length - 1:
        return index - (Length - 1)
    return index + 1


def down_char(index):
    if Length*Height - Length <= index < Length*Height:
        return index % Length
    return index + Length


def move_left(map):
    new_map = map.copy()
    have_moved = False
    for index, char in enumerate(map):
        if char == ">":
            right_char_index = right_char(index)
            if map[right_char_index] == ".":
                have_moved = True
                new_map[index] = "."
                new_map[right_char_index] = ">"

    return new_map, have_moved


def move_down(map):
    new_map = map.copy()
    have_moved = False
    for index, char in enumerate(map):
        if char == "v":
            down_char_index = down_char(index)
            if map[down_char_index] == ".":
                have_moved = True
                new_map[index] = "."
                new_map[down_char_index] = "v"

    return new_map, have_moved


def draw(map, i):
    _str = "cycle = " + str(i+1)

    for i, char in enumerate(map):
        if i % Length == 0:
            _str += "\n"
        _str+=char
    print(_str)


def solve(map):
    can_move = True
    cycle = 0
    while can_move:
        map, movedleft = move_left(map)
        map, moveddown = move_down(map)
        can_move = movedleft or moveddown
        cycle += 1
    return cycle


if __name__ == "__main__":
    map = [char for line in scans for char in line]
    print(solve(map))
