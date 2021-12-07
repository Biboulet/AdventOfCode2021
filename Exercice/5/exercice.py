import os
import utils
from utils import Vector2

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Line:
    def __init__(self, _a, _b):
        self.max = _a
        self.min = _b

        if self.min.x == self.max.x:
            if _a.y > _b.y:
                self.max = _a
                self.min = _b
            else:
                self.max = _b
                self.min = _a
        else:
            if _a.x > _b.x:
                self.max = _a
                self.min = _b
            else:
                self.max = _b
                self.min = _a

    def intersect(self, otherLine):

        if self.is_vertical() and otherLine.is_vertical():
            is_inter = otherLine.min.x == self.min.x and (otherLine.min.x <)
            coord_shared =
            return
        if self.is_vertical() and not otherLine.is_vertical():
            return self.min.y > otherLine.min.y > self.max.y and otherLine.min.x > self.min.x > otherLine.max.x, 1

        if not self.is_vertical() and otherLine.is_vertical():
            return self.min.x > otherLine.min.x > self.max.x and otherLine.min.y > self.min.y > otherLine.max.y, 1
        else:


    def is_vertical(self):
        return self.min.x == self.max.x


def instantiate_lines(scans):
    lines = []
    for line in scans:
        args = line.split("->")
        a = Vector2(int(args[0].split(",")[0]), int(args[0].split(",")[1]))
        b = Vector2(int(args[1].split(",")[0]), int(args[1].split(",")[1]))

        if a.x != b.x and a.y != b.y:
            continue
        lines.append(Line(a, b))

    return lines


def get_num_of_intersect(lines):
    intersect_count = 0
    #ce qui ont déja été line 1 et qui ont interagit avec tt le monde
    already_interact_with_all = []

    for line1 in lines:
        for line2 in lines:

            if line1 == line2:
                continue
            if line2 in already_interact_with_all:
                continue

            is_intersect, intersections_count = line1.intersect(line2)
            if is_intersect:
                intersect_count += intersections_count

    return intersect_count


if __name__ == "__main__":
    lines = instantiate_lines(scans)
    print(get_num_of_intersect(lines))
