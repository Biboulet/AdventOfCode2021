import os
import utils
import math
import unittest

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Test(unittest.TestCase):
    def test_scanner(self):
        input = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7""".splitlines()
        scanner = parse_scanner(input)
        self.assertEqual(6, len(scanner.beacons))
        self.assertEqual("--- scanner 0 ---", scanner.name)

    def test_scanner_instantiate(self):
        scanners_input = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8""".splitlines()
        scanners = instantiate_scanner(scanners_input)
        self.assertEqual(5, len(scanners))
        self.assertEqual(6, len(scanners[0].beacons))

    def test_scanner_equal(self):
        scanners_input = """--- scanner 0 ---
        -1,-1,1
        -2,-2,2
        -3,-3,3
        -2,-3,1
        5,6,-4
        8,0,7

        --- scanner 0 ---
        -1,-1,1
        -2,-2,2
        -3,-3,3
        -2,-3,1
        5,6,-4
        8,0,7
""".splitlines()
        scanners = instantiate_scanner(scanners_input)
        self.assertEqual(2, len(scanners))
        self.assertEqual(scanners[0], scanners[1])

    def test_rotated_scanner_is_equal(self):
        scanners_input = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 1 ---
1,-1,-1
2,-2,-2
3,-3,-3
2,-3,-1
-5,6,4
-8,0,-7""".splitlines()
        scanners = instantiate_scanner(scanners_input)
        rotated_scanner = scanners[0].as_rotated("y", 180)
        self.assertEqual(rotated_scanner, scanners[1])

    def test_translated_scanner(self):
        scanner_inputs = """--- scanner 0 ---
        0,2,0
        4,1,0
        3,3,0

        --- scanner 1 ---
        1,3,1
        5,2,1
        4,4,1""".splitlines()
        scanners = instantiate_scanner(scanner_inputs)
        self.assertEqual(scanners[0].as_translated(Vector3(1,1,1)), scanners[1])

    def test_scanners_commun_beacons(self):
        scanner_inputs = """--- scanner 0 ---
0,2,0
4,1,0
3,3,0

--- scanner 1 ---
-1,-1,0
-5,0,0
-2,1,0""".splitlines()
        scanners = instantiate_scanner(scanner_inputs)
        self.assertEqual(3, get_commun_beacons(scanners[0], scanners[1]))


class Scanner:
    def __init__(self, name, beacons):

        self.beacons = beacons
        self.name = name

    def __eq__(self, other):
        if len(other.beacons) != len(self.beacons):
            return False
        return all([self.beacons[index] == other.beacons[index] for index in range(len(self.beacons))])

    def __str__(self):
        return self.name + " (" + str(len(self.beacons)) + ")"

    def as_rotated(self, direction, value):
        new_beacons = []
        if direction == "x":
            if value == 90:
                pass
            if value == 180:
                pass
            if value == 270:
                pass
        if direction == "y":
            if value == 90:
                new_beacons = [Vector3(-beacon.z, beacon.y, beacon.x) for beacon in self.beacons]
            if value == 180:
                new_beacons = [Vector3(-beacon.x, beacon.y, -beacon.z) for beacon in self.beacons]
            if value == 270:
                new_beacons = [Vector3(beacon.z, beacon.y, -beacon.z) for beacon in self.beacons]
        if direction == "z":
            if value == 90:
                pass
            if value == 180:
                pass
            if value == 270:
                pass
        return Scanner(self.name, new_beacons)

    def as_translated(self, vector):
        new_beacons = [beacon+vector for beacon in self.beacons]
        return Scanner(self.name, new_beacons)


class Vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def magnitude(self):
        return self.distance(Vector3(0, 0, 0))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return str(self.x) + " x " + str(self.y) + " x " + str(self.z)

    def __hash__(self):
        return self.x^self.y^self.z


def compare_beacons(translated_scanner1, translated_scanner2):
    number_of_min_commun = 3
    commun = set(translated_scanner1.beacons).intersection(set(translated_scanner2.beacons))
    if len(commun) >= number_of_min_commun:
        return list(commun)
    return []



def get_commun_beacons(scanner1, scanner2):

    for origin1 in scanner1.beacons:
        #negatif vecteur
        translated_scanner1 = scanner1.as_translated(origin1)
        for origin2 in scanner2.beacons:
            translated_scanner2 = scanner2.as_translated(origin2)
            commun = compare_beacons(translated_scanner1, translated_scanner2)
            if len(commun):
                return commun



def parse_scanner(input):

    name = input[0]
    beacons = []
    for line in input[1:]:
        args = [int(number) for number in line.split(",")]
        beacons.append(Vector3(args[0], args[1], args[2]))
    return Scanner(name, beacons)


def instantiate_scanner(scans):
    previous_end = 0
    scanners = []
    for i, line in enumerate(scans):
        if line == "":
            scanner = parse_scanner(scans[previous_end:i])
            scanners.append(scanner)
            previous_end = i + 1

    scanners.append(parse_scanner(scans[previous_end:]))
    return scanners


if __name__ == "__main__":
    pass
