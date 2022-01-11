import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Pair:
    def __init__(self, input, a=None, b=None):

        if input is None:
            self.a = a
            self.b = b
            return

        a = ""
        b = ""
        is_part_a = True
        parenthese_count = 0
        for char in input[1:-1]:
            # on change
            if char == "," and parenthese_count == 0:
                is_part_a = False
                continue

            # on remplit les 2 partie
            if is_part_a:
                a += char
            else:
                b += char

            if char == "[":
                parenthese_count += 1
            elif char == "]":
                parenthese_count -= 1

        if len(a) == 1:
            self.a = int(a)
        else:
            self.a = Pair(a)

        if len(b) == 1:
            self.b = int(b)
        else:
            self.b = Pair(b)

    def magnitude(self):
        return 3*self.get_value(self.a) + 2*self.get_value(self.b)

    def __add__(self, other):
        return Pair(None, self, other)

    #la fonction doit etre appeler de gauche a droite
    #previousNumber (le nombre de gauche)
    #valueToAdd (on est le nombre de droite du nombre précédent)
    def reduce(self, depth=0, previousPair=None, valueToAdd=None):
        if valueToAdd is None:
            valueToAdd = [0]

        if isinstance(self.a, int):
            self.a += valueToAdd[0]

        #explosion
        if depth == 4:
            if previousPair is not None:
                previousPair.b += self.a
            valueToAdd[0] = self.b
            del self

        for child in [self.a, self.b]:
            if isinstance(child, int) and child > 9:
                if child % 2==0:
                    child = Pair("["+str(child/2)+"," + str(child/2)+"]")
                else:
                    child = Pair("[" + str(child // 2) + "," + str((child // 2)+1) + "]")
                return
            if not isinstance(child, int):
                child.reduce(depth+1, )


    def get_value(self, param):
        if param == None:
            return 0
        if isinstance(param, int):
            return param
        else:
            return param.magnitude()


def instantiate_numbers(scans):
    numbers = []
    for line in scans:
        numbers.append(Pair(line))

    return numbers


def add_numbers(numbers):
    total = numbers[0]
    for num in numbers[1:]:
        total+=num
        total.reduce()
    return total


if __name__ == "__main__":
    numbers = instantiate_numbers(scans)
    result = add_numbers(numbers)
    print(result.magnitude())
