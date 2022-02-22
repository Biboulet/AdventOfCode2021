import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class ALU:
    def __init__(self, input):
        self.instructions = input
        self.var = {"w": 0, "x": 0, "y": 0, "z": 0}

    def run(self, digit):
        num = digit
        index_input = 0

        for line in self.instructions:
            args = line.split()
            parameter = 0

            if args[0] == "inp":
                self.var[args[1]] = num[index_input]
                index_input += 1
                continue
            else:
                if args[2] == "w" or args[2] == "x" or args[2] == "y" or args[2] == "z":
                    parameter = self.var[args[2]]
                else:
                    parameter = int(args[2])

            if args[0] == "add":
                self.var[args[1]] += parameter

            elif args[0] == "mul":
                self.var[args[1]] *= parameter

            elif args[0] == "div":
                assert parameter != "0"
                self.var[args[1]] //= parameter

            elif args[0] == "mod":
                assert self.var[args[1]] >= 0
                assert parameter > 0
                self.var[args[1]] %= parameter

            elif args[0] == "eql":
                self.var[args[1]] = bool(self.var[args[1]] == parameter)

        return bool(self.var["z"] == 0)


def get_digit(num):
    for pow in range(14):
        yield (num // 10 ** pow) % 10


def get_biggest_input(alu):
    for i in range(99999999999999, 0, -1):
        print(i)
        digit = list(get_digit(i))
        if 0 in digit:
            continue
        digit.reverse()
        if alu.run(digit):
            return i


if __name__ == "__main__":
    alu = ALU(scans)
    print(get_biggest_input(alu))
