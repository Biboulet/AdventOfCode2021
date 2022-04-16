import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


def remove_duplicates(list):
    final_list = []
    for thing in list:
        if thing not in final_list:
            final_list.append(thing)
    return final_list


class OctreeNode:
    def __init__(self, _min, _max, activated=False):
        self.min = _min
        self.max = _max
        self._activated = activated

        self.children = []

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        self._activated = value
        for child in self.children:
            child.activated = value

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max

    def get_corners_inter_other(self, other):
        corner_in_other = sum([1 for corner in get_corners(self) if contains(other, corner)])
        corner_in_self = sum([1 for corner in get_corners(other) if contains(self, corner)])
        return corner_in_other, corner_in_self

    def insert(self, other):
        # les 2
        corners_in_other, corners_in_self = self.get_corners_inter_other(other)

        # si on est dans le cube
        if corners_in_other == 8:
            self.activated = other.activated
            return

        # si le cube n'est ni en nous et que nous ne somme pas dans le cube, on skip
        if corners_in_self == 0 and corners_in_other == 0:
            return

        if len(self.children) == 0:
            self.children = self.subdivide()

        for child in self.children:
            child.insert(other)

    def subdivide(self):
        # centre = (self.min + self.max)//2
        centre = Vector3((self.min.x + self.max.x) // 2, (self.min.y + self.max.y) // 2, (self.min.z + self.max.z) // 2)

        second_half_x = centre.x + 1 if self.min.x != self.max.x else centre.x
        second_half_y = centre.y + 1 if self.min.y != self.max.y else centre.y
        second_half_z = centre.z + 1 if self.min.z != self.max.z else centre.z

        min = self.min
        max = self.max

        # min ; centre
        bas_gauche_back = OctreeNode(Vector3(min.x, min.y, min.z), Vector3(centre.x, centre.y, centre.z), self.activated)

        # (centre.x+1,min.y,min.z) ; (max.x, centre.y, centre.z)
        bas_droite_back = OctreeNode(Vector3(second_half_x, min.y, min.z), Vector3(max.x, centre.y, centre.z), self.activated)

        # (min.x, centre.y+1, min.z) ; (centre.x, max.y, centre.z)
        haut_gauche_back = OctreeNode(Vector3(min.x, second_half_y, min.z), Vector3(centre.x, max.y, centre.z), self.activated)

        # (centre.x+1, centre.y+1, min.z) ; (max.x, max.y, centre.z)
        haut_droite_back = OctreeNode(Vector3(second_half_x, second_half_y, min.z), Vector3(max.x, max.y, centre.z), self.activated)

        # min ; centre
        bas_gauche_front = OctreeNode(Vector3(min.x, min.y, second_half_z), Vector3(centre.x, centre.y, max.z), self.activated)

        # (centre.x+1,min.y,centre.z+1) ; (max.x, centre.y, centre.z)
        bas_droite_front = OctreeNode(Vector3(second_half_x, min.y, second_half_z), Vector3(max.x, centre.y, max.z), self.activated)

        # (min.x, centre.y+1, centre.z+1) ; (centre.x, max.y, centre.z)
        haut_gauche_front = OctreeNode(Vector3(min.x, second_half_y, second_half_z), Vector3(centre.x, max.y, max.z), self.activated)

        # (centre.x+1, centre.y+1, centre.z+1) ; (max.x, max.y, centre.z)
        haut_droite_front = OctreeNode(Vector3(second_half_x, second_half_y, second_half_z),
                                       Vector3(max.x, max.y, max.z), self.activated)

        return remove_duplicates([bas_gauche_back, bas_droite_back, haut_gauche_back, haut_droite_back, bas_gauche_front,
                 bas_droite_front, haut_gauche_front, haut_droite_front])

    def get_activated(self):
        if len(self.children):
            return sum([child.get_activated() for child in self.children])

        if self.activated:
            return self.volume()
        return 0

    def volume(self):
        return (self.max.x + 1 - self.min.x) * (self.max.y + 1 - self.min.y) * (self.max.z + 1 - self.min.z)

    def __str__(self):
        return str(self.min) + " ; " + str(self.max) + (" ; has children" if len(self.children) != 0 else "") + (
            " ; activated" if self.activated else "")


class Vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

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


class Cube:
    def __init__(self, x, X, y, Y, z, Z, value):
        self.min = Vector3(x, y, z)
        self.max = Vector3(X, Y, Z)
        self.activated = value


def get_corners(cube):
    return [Vector3(X, Y, Z) for X in [cube.min.x, cube.max.x] for Y in [cube.min.y, cube.max.y] for Z in
            [cube.min.z, cube.max.z]]


def contains(cube, point):
    return cube.min.x <= point.x <= cube.max.x and cube.min.y <= point.y <= cube.max.y and cube.min.z <= point.z <= cube.max.z


def get_cubes(scans):
    list_cubes = []
    for line in scans:
        args = line.split()
        dimension = args[1].split(",")
        _minX, _maxX = [int(value) for value in dimension[0].split("=")[1].split("..")]
        _minY, _maxY = [int(value) for value in dimension[1].split("=")[1].split("..")]
        _minZ, _maxZ = [int(value) for value in dimension[2].split("=")[1].split("..")]

        list_cubes.append(Cube(_minX, _maxX, _minY, _maxY, _minZ, _maxZ, "n" in line))

    return list_cubes


def compute_octree(main_octree, cubes):
    for i, cube in enumerate(cubes):
        print(i)
        main_octree.insert(cube)


if __name__ == "__main__":
    cubes = get_cubes(scans)
    main_octree = OctreeNode(Vector3(-100000, -100000, -100000), Vector3(100000, 100000, 100000))
    compute_octree(main_octree, cubes)
    print(main_octree.get_activated())
