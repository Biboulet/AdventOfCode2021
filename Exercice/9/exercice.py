import os
import utils
import math

scans = utils.read_file(os.getcwd() + "\\input.txt")
length = len(scans[0])
height = len(scans)


class Point:
    def __init__(self, a, b):
        self.value = a
        self.index = b


class Bassin:
    def __init__(self, points):
        self.points_who_composed = points


def get_adgacent(index, points, length, height):
    # up
    if 0 <= index <= length - 1:
        yield Point(9,0)
    else:
        yield points[index - length]
    # down
    if length * (height - 1) <= index <= length * height:
        yield Point(9,0)
    else:
        yield points[index + length]
    # right
    if index % length == length - 1:
        yield Point(9,0)
    else:
        yield points[index + 1]
    # left
    if index % length == 0:
        yield Point(9,0)
    else:
        yield points[index - 1]


def get_low_points(points):
    low_points = []

    for current_point in points:
        num = current_point.value
        up, down, right, left = get_adgacent(current_point.index, points, length, height)
        if num < up.value and num < down.value and num < right.value and num < left.value:
            low_points.append(current_point)

    return low_points


def get_bassin(point, all_points, bassin):
    ajacent = list(get_adgacent(point.index, all_points, length, height))
    for adj in ajacent:
        if adj.value < 9:
            if adj not in bassin.points_who_composed:
                bassin.points_who_composed.append(adj)
                get_bassin(adj, all_points, bassin)
    return bassin


def get_all_bassins(index_low_points, points):
    bassins_list = []

    for low_point in index_low_points:

        current_bassin = Bassin([low_point])
        current_bassin = get_bassin(low_point, points, current_bassin)
        if current_bassin not in bassins_list:
            bassins_list.append(current_bassin)
    return bassins_list


def get_higesht_bassin(bassins):
    higest = []
    for i in range(3):
        bigest_bassins = bassins[0]
        for bassin in bassins:
            if len(bigest_bassins.points_who_composed) < len(bassin.points_who_composed):
                bigest_bassins = bassin
        higest.append(len(bigest_bassins.points_who_composed))
        bassins.remove(bigest_bassins)

    return math.prod(higest)


def get_points(scans):
    points = []
    for index_line, line in enumerate(scans):
        for index_number, number in enumerate(line):
            index = index_line * length + index_number
            value = int(number)
            points.append(Point(value, index))

    return points


if __name__ == "__main__":
    points = get_points(scans)
    index_low_points = get_low_points(points)
    bassins = get_all_bassins(index_low_points, points)
    print(get_higesht_bassin(bassins))
