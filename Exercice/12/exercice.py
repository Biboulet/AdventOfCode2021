import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Cave:
    def __init__(self, name):
        self.name = name
        self.linked = []
        if name.isupper():
            self.is_big_cave = True
        else:
            self.is_big_cave = False

    def add_linked(self, cave):
        self.linked.append(cave)

    def __str__(self):
        return self.name
    def __eq__(self, other):
        if other is None:
            return False
        return other.name == self.name


class Path:

    def __init__(self, cave=None):
        self.black_listed_caves = []
        self.visited_caves = []
        self.cave_which_can_be_visited_twice = cave

    def get_all_paths_of(self, current_cave):
        self.visited_caves.append(current_cave)
        if not current_cave.is_big_cave:
            if current_cave == self.cave_which_can_be_visited_twice:
                self.cave_which_can_be_visited_twice = None
            else:
                self.black_listed_caves.append(current_cave)

        if current_cave.name == "end":
            return [self]

        local_paths = []
        for linked_cave in current_cave.linked:
            if linked_cave not in self.black_listed_caves:
                local_paths += self.clone().get_all_paths_of(linked_cave)

        return local_paths

    def clone(self):
        clone = Path(self.cave_which_can_be_visited_twice)
        clone.black_listed_caves += self.black_listed_caves
        clone.visited_caves += self.visited_caves
        return clone

    def __eq__(self, other):
        if len(self.visited_caves) != len(other.visited_caves):
            return False
        for index in range(len(self.visited_caves)):
            if self.visited_caves[index] != other.visited_caves[index]:
                return False
        return True


def get_cave(name, caves):
    for cave in caves:
        if cave.name == name:
            return cave

    new_cave = Cave(name)
    caves.append(new_cave)
    return new_cave


def instantiate_caves(scans):
    caves = []
    for line in scans:
        args = line.split("-")
        cave1 = get_cave(args[0], caves)
        cave2 = get_cave(args[1], caves)

        cave1.add_linked(cave2)
        cave2.add_linked(cave1)

    return caves


def get_paths(caves):
    start = get_cave("start", caves)
    paths = Path().get_all_paths_of(start)
    return paths

def get_paths2(caves):
    start = get_cave("start", caves)

    paths = []
    for cave in caves:
        print("a")
        cave_which_can_be_visited_twice= None
        if not cave.is_big_cave and not cave.name == "start":
            cave_which_can_be_visited_twice = cave
        else:
            continue


        current_paths = Path(cave_which_can_be_visited_twice).get_all_paths_of(start)

        for path in current_paths:
            if path not in paths:
                paths.append(path)

    return paths


if __name__ == "__main__":
    caves = instantiate_caves(scans)
    paths = get_paths2(caves)
    print(len(paths))