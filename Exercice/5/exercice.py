import os
import utils
import math
from utils import Vector2

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Line:
    def __init__(self, _a, _b):
        self.a = _a
        self.b = _b

        self.cases = self.get_cases()

    def get_cases(self):
        cases = []
        # vertical
        if self.a.x == self.b.x:
            min, max = self.get_min_and_max(self.a, self.b)

            for i in range(min.y, max.y + 1):
                cases.append(Vector2(self.a.x, i))

        # horizontal
        elif self.a.y == self.b.y:
            min, max = self.get_min_and_max(self.a, self.b)

            for i in range(min.x, max.x + 1):
                cases.append(Vector2(i, self.a.y))
        # diagonal
        #gauche haut vers bas droite (+ en + de x et y)
        elif (self.a.x < self.b.x and self.a.y < self.b.y) or (self.a.x > self.b.x and self.a.y > self.b.y):
            min, max = self.get_min_and_max(self.a, self.b)

            for i in range(1 + max.x - min.x):
               cases.append(Vector2(min.x + i, min.y + i))

        else:
            min, max = self.get_min_and_max(self.a, self.b)

            for i in range(1 + max.x - min.x):
               cases.append(Vector2(min.x + i, min.y - i))


        return cases

    def get_min_and_max(self, a, b):
        if a.x == b.x:
            if a.y < b.y:
                return a, b
            else:
                return b, a

        if self.a.y == self.b.y:
            if a.x < b.x:
                return a, b
            else:
                return b, a

        if (self.a.x < self.b.x and self.a.y < self.b.y) or (self.a.x > self.b.x and self.a.y > self.b.y):
            if self.a.x < self.b.x and self.a.y < self.b.y:
                return a, b
            else:
                return b, a
        else:
            if self.a.y > self.b.y:
                return a, b
            else:
                return b, a

    def commun_cases(self, other):
        return [case for case in self.cases if case in other.cases]


def instantiate_lines(scans):
    lines = []
    for line in scans:
        args = line.split("->")
        a = Vector2(int(args[0].split(",")[0]), int(args[0].split(",")[1]))
        b = Vector2(int(args[1].split(",")[0]), int(args[1].split(",")[1]))

        lines.append(Line(a,b))

    return lines


def get_num_of_intersect(lines):
    intersections = []
    intercated_with_all = []

    i = 0
    for line1 in lines:
        print(i)
        for line2 in lines:

            if line1 == line2:
                continue

            if line2 in intercated_with_all:
                continue

            commun_cases = line1.commun_cases(line2)
            [intersections.append(case) for case in commun_cases if case not in intersections]

        intercated_with_all.append(line1)
        i += 1
    return len(intersections)

if __name__ == "__main__":
    lines = instantiate_lines(scans)
    print(get_num_of_intersect(lines))
