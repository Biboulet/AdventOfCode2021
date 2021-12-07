import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Crab:
    def __init__(self, a):
        self.position = a

    def fuel_to_get_to(self, pos_target):

        return sum([num for num in range(abs(self.position - pos_target)+1)])



def instantiate_crab(scans):
    crab = []

    for number in scans[0].split(","):
        crab.append(Crab(int(number)))

    return crab


def best_position(crabs):
    # 2000
    total_fuel_to_pos = []

    for position in range(2000):
        print(position)
        fuel_to_get = 0
        for crab in crabs:
            fuel_to_get += crab.fuel_to_get_to(position)
        total_fuel_to_pos.append(fuel_to_get)

    return min(total_fuel_to_pos)


if __name__ == "__main__":
    crabs = instantiate_crab(scans)
    print(best_position(crabs))
