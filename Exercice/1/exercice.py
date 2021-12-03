import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


def part1():
    increased = 0
    previous_value = 9999
    for line in scans:
        if int(line) > previous_value:
            increased += 1
        previous_value = int(line)
    print(increased)


def part2():
    increased = 0
    previous_value = 9999
    for index in range(len(scans)):
        if index >= len(scans)-2:
            continue
        sum_of_numbers = sum([int(scans[number + index]) for number in range(3)])
        if sum_of_numbers > previous_value:
            increased += 1
        previous_value = sum_of_numbers
    print(increased)


if __name__ == "__main__":
    part2()
