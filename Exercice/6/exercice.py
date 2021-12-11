import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")

class Lanternfish:
    def __init__(self, a):
        self.days_until_reproduce = a
    def evolve(self, fish_list):
        self.days_until_reproduce -= 1
        if self.days_until_reproduce < 0:
            self.days_until_reproduce = 6
            fish_list.append(Lanternfish(9))
            #car gerer just apres


def instatiate_lanterfish(scans):
    lanterfish = []
    numbers = scans[0].split(",")
    for num in numbers:
        lanterfish.append(Lanternfish(num))
    return lanterfish



def simulate_fish(day_max, fish_list):
    for day in range(day_max + 1):
        for fish in fish_list:
            fish.evolve(fish_list)



if __name__ == "__main__":
    lanterfish = instatiate_lanterfish(scans)
    print(simulate_fish(80, lanterfish))

