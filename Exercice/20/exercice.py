import os
from utils import Vector2
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")
Length = len(scans[2])
Height = len(scans) - 2


def instantiate_map(input):
    points = []
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == "#":
                points.append((x, y))
    map = {}
    for y in range(-51, Height + 51):
        for x in range(-51, Length + 51):
            tuple = (x, y)
            if tuple in points:
                map[tuple] = "#"
            else:
                map[tuple] = "."
    return map


def get_adjacent(key):
    # haut en bas, gauche a droite
    for y in range(key[1] - 1, key[1] + 2):
        for x in range(key[0] - 1, key[0] + 2):
            yield (x, y)


def get_values(adjacent, map, default):
    values = []
    for coord in adjacent:
        if map.get(coord, default) == ".":
            values.append(0)
        else:
            values.append(1)
    return values




def simulate(map, enhancement_algo, cycle):

    for cycle in range(cycle):
        print(cycle)
        default_value = "."
        if cycle % 2 == 0:
            default_value = "."
        else:
            default_value = "#"

        new_map = {}
        for key in map.keys():
            adjacent = list(get_adjacent(key))
            octet = get_values(adjacent, map, default_value)
            signe = enhancement_algo[utils.BinToDec(octet)]
            new_map[key] = signe
        map = new_map
    return map




if __name__ == "__main__":
    enhancement_algo = scans[0]
    map = instantiate_map(scans[2:])
    map = simulate(map, enhancement_algo, 50)

    print(sum([1 for value in map.values() if value == "#"]))

