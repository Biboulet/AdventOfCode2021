import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")
length = len(scans[0])
height = len(scans)

class Octopus:
    def __init__(self, energy_level):
        self.energy_level = energy_level
        self.adjacents = []
        self.last_step_has_flashed = -1
        self.flash_count = 0

    def evolve(self, step):
        if self.last_step_has_flashed == step:
            return
        self.energy_level +=1
        if self.energy_level > 9:
            self.flash_count +=1
            self.energy_level = 0
            self.last_step_has_flashed = step
            [adj.evolve(step) for adj in self.adjacents]

    def __str__(self):
        return self.energy_level

def get_adgacent(index, points, length, height):
    # up
    if not (0 <= index <= length - 1):
        yield points[index - length]
    # up-left
    if not (0 <= index <= length - 1) and not (index % length == 0):
        yield points[index - length - 1]
    # up right
    if not (0 <= index <= length - 1) and not (index % length == length-1):
        yield points[index - length + 1]
    # down
    if not (length * (height - 1) <= index <= length * height):
        yield points[index + length]
    # down left
    if not (length * (height - 1) <= index <= length * height) and not (index % length == 0):
        yield points[index + length - 1]
    # down right
    if not (length * (height - 1) <= index <= length * height) and not (index % length == length - 1):
        yield points[index + length + 1]
    # right
    if not (index % length == length-1):
        yield points[index + 1]
    # left
    if not (index % length == 0):
        yield points[index - 1]


def instantiate_octus(scans):


    octopus_list = [Octopus(int(value)) for line in scans for value in line]

    for index, current_octopus in enumerate(octopus_list):
        if index == 39:
            a= 0
        adjacent = list(get_adgacent(index, octopus_list, length, height))
        current_octopus.adjacents = adjacent

    return octopus_list


def get_config(octupus, step):
    texte = "step number " + str(step+1) + "\n"
    index = 0
    for index, _octopus in enumerate(octupus):
        texte += str(_octopus.energy_level)
        if index % length == length - 1:
            texte +="\n"
    return texte


def simulate_octo_for(octupus):

    for step in range(999999999):
        for current_octupus in octupus:
            current_octupus.evolve(step)
        print(get_config(octupus, step))

        if all([octo.last_step_has_flashed == step for octo in octupus]):
            return step +1





if __name__ == "__main__":
    octupus = instantiate_octus(scans)
    print(simulate_octo_for(octupus))
