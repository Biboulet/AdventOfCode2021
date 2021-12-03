import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


def getPositions1(instructions):
    depth = 0
    horizontal = 0

    for line in instructions:
        direction = line.split()[0]
        value = int(line.split()[1])

        if direction == "forward":
            horizontal += value
        elif direction == "down":
            depth += value
        elif direction == "up":
            depth -= value

    return depth * horizontal


if __name__ == "__main__":
    print(getPositions1(scans))
