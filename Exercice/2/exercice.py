import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


def getPositions(instructions):
    depth = 0
    horizontal = 0
    aim = 0

    for line in instructions:
        direction = line.split()[0]
        value = int(line.split()[1])

        if direction == "forward":
            horizontal += value
            depth+=aim*value
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value

    return depth * horizontal


if __name__ == "__main__":
    print(getPositions(scans))
