import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


def is_valid(coords):
    for coord in coords:
        if coord < -50 or coord > 50:
            return False
    return True

def solve(scans):
    cubes = {}
    index = 0
    for line in scans:
        print(index)
        args = line.split()
        dimension = args[1].split(",")

        minX, maxX = [int(value) for value in dimension[0].split("=")[1].split("..")]
        minY, maxY = [int(value) for value in dimension[1].split("=")[1].split("..")]
        minZ, maxZ = [int(value) for value in dimension[2].split("=")[1].split("..")]

        value = int(args[0] == "on")

        for x in range(minX, maxX+1):
            for y in range(minY, maxY + 1):
                for z in range(minZ, maxZ + 1):
                    cubes[(x,y,z)] = value
        index += 1
    print(sum([value for value in cubes.values()]))





if __name__ == "__main__":
    solve(scans)

