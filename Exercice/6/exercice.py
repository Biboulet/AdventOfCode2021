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


    def evolve_for(self, days, fish_list):
        for day_passed in range(days):

            self.days_until_reproduce -= 1
            if self.days_until_reproduce < 0:
                self.days_until_reproduce = 6
                new_fish = Lanternfish(8)
                new_fish.evolve_for(days-(day_passed+1), fish_list)
                fish_list.append(new_fish)




def instatiate_lanterfish(scans):
    lanterfish = []
    numbers = scans[0].split(",")
    for num in numbers:
        lanterfish.append(Lanternfish(int(num)))
    return lanterfish



def simulate_fish(day_max, fish_list):
    for day in range(day_max):
        for fish in fish_list:
            fish.evolve(fish_list)
    return len(fish_list)


def simulate_fish_fast(day_max, fish_list):

    first_gen = []
    for fish in fish_list:
        first_gen.append(fish)

    for fish in first_gen:
        fish.evolve_for(day_max, fish_list)

    return len(fish_list)


if __name__ == "__main__":
    #faire tt les jours d'un coup puis eveolove
    lanterfish = instatiate_lanterfish(scans)


    print(simulate_fish_fast(256, lanterfish))

