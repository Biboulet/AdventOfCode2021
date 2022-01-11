import os
import math

class Vector2:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+ other.y)

    def __str__(self):
        return str(self.x) + " x " + str(self.y)


def BinToDec(octet):
    return sum([2 ** index for index in range(len(octet)) if octet[-(index + 1)] == 1])

def read_file(path):
    if os.path.isfile(path):
        return open(path, "r").read().splitlines()
    print("File does not exist")

