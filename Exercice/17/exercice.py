import os
from utils import Vector2
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")

class TargetAera:
    def __init__(self, texte):
        args = texte.split(": ")[1]
        coord = args.split(", ")
        self.min_x = int(coord[0].split("=")[1].split("..")[0])
        self.max_x = int(coord[0].split("=")[1].split("..")[1])
        self.min_y = int(coord[1].split("=")[1].split("..")[0])
        self.max_y = int(coord[1].split("=")[1].split("..")[1])

    def intersect(self, vector2):
        if self.min_x <= vector2.x <= self.max_x and self.min_y <= vector2.y <= self.max_y:
            return "yes"
        if vector2.x > self.max_x or vector2.y < self.min_y:
            return "never"
        return "no"

class Probe:
    def __init__(self, vel_x, vel_y):
        self.position = Vector2(0,0)
        self.velocity = Vector2(vel_x, vel_y)

    def move(self):
        self.position += self.velocity
        self.velocity.y -= 1
        if self.velocity.x > 0:
            self.velocity.x -= 1
        elif self.velocity.x < 0:
            self.velocity.x += 1

def simulate(current_probe, targetAera):

    y_pos = []
    while True:
        current_probe.move()
        y_pos.append(current_probe.position.y)
        if targetAera.intersect(current_probe.position) == "yes":
            return 1
        elif targetAera.intersect(current_probe.position) == "never":
            return 0



def get_max_heigth(targetAera):
    path_count = 0
    for velocity_y in range(targetAera.min_y, 1000):
        for velocity_x in range(1, targetAera.max_x+1):
            current_probe = Probe(velocity_x, velocity_y)
            path_count += simulate(current_probe, targetAera)
    return path_count



if __name__ == "__main__":
    targetAera = TargetAera(scans[0])
    print(get_max_heigth(targetAera))
