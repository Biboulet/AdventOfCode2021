import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")

class InsertionRule:
    def __init__(self,a,b):
        self.input = a
        self.ouput = b


def instantiate_rules(scans):
    rules = {}
    for line in scans:
        args = line.split(" -> ")
        rules[args[0]] = args[1]
    return rules


def get_intercalaire(input, rules):
    for instruction in rules:
        if instruction.input == input:
            return instruction.ouput
    pass


def evolve_template(template, cycles, rules):

    #contient le nombre de tt les pairs
    list_of_pairs = {}
    #on crée tt les pair possible
    for pair in rules:
        list_of_pairs[pair] = 0

    #on ajoute les pairs de base
    for i in range(len(template)-1):
        list_of_pairs[template[i] + template[i+1]] +=1

    for cycle_passed in range(cycles):
        new_list_of_pairs = {}

        #on crée tt les pair possible
        for pair in rules:
            new_list_of_pairs[pair] = 0

        #si ab-->c, alors ab devient ac et cb
        for pairs in list_of_pairs:
            new_list_of_pairs[pairs[0] + rules[pairs]] += list_of_pairs[pairs]
            new_list_of_pairs[rules[pairs] + pairs[1]] += list_of_pairs[pairs]
        list_of_pairs = new_list_of_pairs

    return list_of_pairs


def finish(list_of_pairs, last_letter):
    letter_dict = {}

    for pair in list_of_pairs:
        letter_dict[pair[0]] = 0
        letter_dict[pair[1]] = 0

    for pair in list_of_pairs:
        letter_dict[pair[0]] += list_of_pairs[pair]
    letter_dict[last_letter]+=1
    length = sum(letter_dict.values())
    return max(letter_dict.values()) - min(letter_dict.values())


if __name__ == "__main__":
    rules = instantiate_rules(scans[2:])
    template = scans[0]
    list_of_pairs = evolve_template(template, 40, rules)
    print(finish(list_of_pairs, template[-1]))
