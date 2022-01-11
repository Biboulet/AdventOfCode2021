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
        scanner = Scanner(input)
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

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0""".splitlines()
        scanners = instantiate_scanner(scanners_input)
        rotated_scanner = scanners[0].as_rotated("y", 180)
        self.assertEqual(rotated_scanner, scanners[1])


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
    def __init__(self, input):
        self.beacons = []
        self.name = input[0]
        for line in input[1:]:
            args = [int(number) for number in line.split(",")]
            self.beacons.append(Vector3(args[0], args[1], args[2]))

    def __eq__(self, other):
        if len(other.beacons) != len(self.beacons):
            return False
        return all([self.beacons[index] == other.beacons[index] for index in range(len(self.beacons))])

    def __str__(self):
        return self.name + " (" + str(len(self.beacons)) + ")"

    def as_rotated(self, param, param1):
        pass


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

def get_commun_beacons(param, param1):
    pass

def instantiate_scanner(scans):
    previous_end = 0
    scanners = []
    for i, line in enumerate(scans):
        if line == "":
            scanners.append(Scanner(scans[previous_end:i]))
            previous_end = i+1
    scanners.append(Scanner(scans[previous_end:]))
    return scanners

if __name__ == "__main__":
    pass
