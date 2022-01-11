import os
from  utils import Vector2
import utils


scans = utils.read_file(os.getcwd() + "\\input.txt")

class Instruction:
    def __init__(self, direction, value):
        self.direction = direction
        self.value = value

def instantiate_map(scans):
    points = []
    instructions = []
    for line in scans:
        if not line.startswith("fold"):
            args = line.split(",")
            points.append(Vector2(int(args[0]), int(args[1])))

        elif line.startswith("fold"):
            args = line.split()[2].split("=")
            instructions.append(Instruction(args[0], int(args[1])))

    return points, instructions


def remove_duplicates(map):
    Dict = {}
    for point in map:
        Dict[str(point)] = 1

    a = sum(Dict.values())
    return map


def fold_map(map, instructions):
    for current_instruction in instructions:
        fold_value = current_instruction.value
        is_vertical = current_instruction.direction == "x"

        for point in map:
            if is_vertical:
                if point.x > fold_value:
                    point.x = fold_value - (point.x - fold_value)
            else:
                if point. y > fold_value:
                    point.y = fold_value - (point.y - fold_value)
    map = remove_duplicates(map)
    return map


def graph(points):
    max_x = max(point.x for point in points)
    max_y = max(point.y for point in points)

    for y in range(max_y+1):
        line = ""
        for x in range(max_x+1):
            if Vector2(x,y) in points:
                line += "#"
            else:
                line += "."
        print(line)


if __name__ == "__main__":
    map, instructions = instantiate_map(scans)
    map = fold_map(map, instructions)
    graph(map)
    print(len(map))