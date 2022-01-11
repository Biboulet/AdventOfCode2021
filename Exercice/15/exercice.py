import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")

Length = len(scans[0])
Heigth = len(scans)


class Node:
    def __init__(self, value):
        self.linked = []
        self.cost_to_go = 0
        self.value = value

    def __str__(self):
        return str(self.value)


class Map:
    def __init__(self):
        self.nodes = []

    def link(self):
        for index, node in enumerate(self.nodes):
            if node.value > 9:
                node.value -=9
            linked = []


            #up
            if not index <= (Length*5)-1:
                linked.append(self.nodes[index - Length*5])
            # left
            if not (index % (Length*5)) == 0:
                linked.append(self.nodes[index - 1])
            # right
            if not (index % (Length * 5)) == Length * 5 - 1:
                linked.append(self.nodes[index + 1])
            # bottom
            if not index >= Heigth*5 * Length*5 - Length*5:
                linked.append(self.nodes[index + Length*5])
            # peut etre ajouter d'autre direction
            node.linked = linked



def get_closest_node(local_map):
    closest = local_map[0]
    for node in local_map:
        if node.cost_to_go < closest.cost_to_go:
            closest = node
    return closest


def get_lowest_risk_path(map, target):
    # Initialisation
    local_map = []
    for node in map.nodes:
        node.cost_to_go = 9999999
        local_map.append(node)
    local_map[0].cost_to_go = 0

    while True:
        most_close_node = get_closest_node(local_map)

        if most_close_node is target:
            return most_close_node.cost_to_go

        local_map.remove(most_close_node)

        for neighbour in most_close_node.linked:
            this_path = most_close_node.cost_to_go + neighbour.value
            if this_path < neighbour.cost_to_go:
                neighbour.cost_to_go = this_path


def instantiate_nodes(scans):
    return [Node(int(value)) for line in scans for value in line]


def evolve_map(base_nodes):
    final_map = Map()

    for line in range(Heigth * 5):
        for node in range(Length * 5):
            i = node % Length
            offest = (line % Heigth)*Length
            final_index = i + offest
            final_map.nodes.append(Node(base_nodes[final_index].value + node // Length+line//Heigth))

    final_map.link()
    return final_map


if __name__ == "__main__":
    base_nodes = instantiate_nodes(scans)
    map = evolve_map(base_nodes)
    print(get_lowest_risk_path(map, map.nodes[-1]))

