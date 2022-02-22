import os
import utils
import math
import unittest
import itertools

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
        self.assertEqual(6, len(scanner))
        self.assertEqual("0", scanner.name)

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
        self.assertEqual(6, len(scanners[0]))

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
        self.assertEqual(scanners[0].as_translated(Vector3(1, 1, 1)), scanners[1])

    def test_scanners_commun_beacons(self):
        scanner_inputs = """--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""".splitlines()
        scanners = instantiate_scanner(scanner_inputs)
        a = get_scanner2_as_linked_to_1(scanners[0], scanners[1])[0]
        self.assert_(a is not None)

    def test_rotated_scanners_equal(self):
        scanner_inputs = """--- scanner 0 ---
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
        scanners = instantiate_scanner(scanner_inputs)


        has_found = False
        for scanner in scanners:
            for rotation_index in range(48):
                if scanner == scanners[0].as_rotated(rotation_index, Vector3(0, 0, 0))[0]:
                    self.assert_(True)
                    has_found = True
                    break
            if not has_found:
                self.assert_(False)

    def test_combinate_scanner(self):
        scanner_inputs = """--- scanner 0 ---
        -1,-1,1
        -2,-2,2
        -3,-3,3
        -2,-3,1
        5,6,-4
        8,0,7

        --- scanner 1 ---
        -1,-1,1
        -2,-2,2
        -3,-3,3
        -2,-3,1
        5,6,-4
        8,0,7
        4,5,6
        7,8,9
""".splitlines()
        scanners = instantiate_scanner(scanner_inputs)
        len_beacons1 = len(scanners[0])
        self.assertEqual(len_beacons1 + 2, len(combinate_scanners(scanners[0], scanners[1]).beacons))


class Scanner:
    def __init__(self, name, beacons):
        self.beacons_set = set(beacons)
        self.name = name

    def __eq__(self, other):
        return self.beacons_set == other.beacons_set

    def __str__(self):
        return self.name + " (" + str(len(self)) + ")"

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.beacons_set)

    def as_rotated(self, rotation_index, origine):
        assert 0 <= rotation_index < 48
        return Scanner(self.name, [beacon.as_rotated(rotation_index) for beacon in self.beacons]), \
               origine.as_rotated(rotation_index)

    def as_translated(self, vector):
        new_beacons = [beacon + vector for beacon in self.beacons]
        return Scanner(self.name, new_beacons)

    @property
    def beacons(self):
        return list(self.beacons_set)

    @beacons.setter
    def beacons(self, new_value):
        self.beacons_set = set(new_value)


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


def has_commun_beacons(scanner1, translated_scanner2):
    # retourner les vrais balises
    number_of_min_commun = 12
    commun = scanner1.beacons_set.intersection(translated_scanner2.beacons_set)
    return len(commun) >= number_of_min_commun


def get_scanner2_as_linked_to_1(scanner1, scanner2):
    for origin1 in scanner1.beacons:
        for origin2 in scanner2.beacons:
            for rotation_index in range(48):
                translated_scanner, origin_rotated = scanner2.as_rotated(rotation_index, origin2)
                offset = origin1 - origin_rotated
                translated_scanner = translated_scanner.as_translated(offset)

                if has_commun_beacons(scanner1, translated_scanner):
                    print("founded commun between " + scanner1.name + " and " + scanner2.name)
                    return translated_scanner, offset
    print("didn't founded commun between " + scanner1.name + " and " + scanner2.name)
    return None, None


def parse_scanner(input):
    name = input[0].split("scanner ")[1].split(" ---")[0]
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


def combinate_scanners(scanner, modified_scanner):
    scanner.beacons += modified_scanner.beacons
    return scanner


def compare_scanner(scanners):
    main_scanner = scanners.pop(0)
    scanners_position = {}
    while len(scanners):
        for tested_scanner in scanners:
            modified_scanner, offset = get_scanner2_as_linked_to_1(main_scanner, tested_scanner)
            if modified_scanner is not None:
                main_scanner = combinate_scanners(main_scanner, modified_scanner)
                scanners_position[tested_scanner.name] = offset
                scanners.remove(tested_scanner)

    return main_scanner, scanners_position


def max_manathan_distance(scanners_positions):
    distances = []
    for scanner1pos in scanners_positions.values():
        for scanner2pos in scanners_positions.values():
            D = abs(scanner1pos.x - scanner2pos.x) + abs(scanner1pos.y - scanner2pos.y) + abs(scanner1pos.z - scanner2pos.z)
            distances.append(D)

    return max(distances)

if __name__ == "__main__":
    scanners = instantiate_scanner(scans)
    main_scanner, scanners_positions = compare_scanner(scanners)
    print(len(main_scanner))
    print(max_manathan_distance(scanners_positions))
