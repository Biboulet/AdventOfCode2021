import os
import math
import itertools

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

    def __neg__(self):
        return Vector2(-self.x, -self.y)

class Vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def magnitude(self):
        return self.distance(Vector3(0, 0, 0))

    def as_rotated(self, rotation_index):
        assert 0 <= rotation_index < 48
        coords = [self.x, self.y, self.z]

        # 6 possiiblité de permutation
        for index, new_order in enumerate(list(itertools.permutations([0, 1, 2]))):
            if rotation_index // 8 == index:
                coords = [coords[new_order[0]], coords[new_order[1]], coords[new_order[2]]]

        # 8 possibilité (2^3)
        if rotation_index % 2 == 1:
            coords[0] *= -1
        if (rotation_index // 2) % 2 == 1:
            coords[1] *= -1
        if (rotation_index // 4) % 2 == 1:
            coords[2] *= -1

        return Vector3(coords[0], coords[1], coords[2])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return str(self.x) + " x " + str(self.y) + " x " + str(self.z)

    def __hash__(self):
        return self.x ^ self.y ^ self.z

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

def BinToDec(octet):
    return sum([2 ** index for index in range(len(octet)) if octet[-(index + 1)] == 1])

def read_file(path):
    if os.path.isfile(path):
        return open(path, "r").read().splitlines()
    print("File does not exist")

