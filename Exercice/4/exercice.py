import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")

class Bingo:
    def __init__(self, _numbers):
        _numbers = [int(number) for number in _numbers]
        self.numbers = _numbers
        self.marked_numbers = []

    def update_number(self, number_rolled):
        for number in self.numbers:
            if number == number_rolled:
                self.marked_numbers.append(number)

    def end(self):
        unmarked = [number for number in self.numbers if number not in self.marked_numbers]
        return sum(unmarked) * self.marked_numbers[-1]

    def is_over(self):
        return self.is_row_over() or self.is_column_over()

    def is_row_over(self):
        return any([self.is_valid(row) for row in self.rows()])

    def is_column_over(self):
        return any([self.is_valid(column) for column in self.column()])

    def is_valid(self, row):
        return all([number in self.marked_numbers for number in row])

    def rows(self):
        return [self.numbers[index:index + 5] for index in range(0, 25, 5)]

    def column(self):
        for index in range(5):
            yield [self.numbers[5 * local_index + index] for local_index in range(5)]


def get_number(param):
    return [int(number) for number in param.split(",")]


def instatiate_bingos(scans):
    bingos = []
    for index in range(0, len(scans), 6):
        numbers = " ".join([scans[local_index] for local_index in range(index, index + 6)]).split()
        bingos.append(Bingo(numbers))
    return bingos


def update_bingo(bingos, number_rolled):

    ended_bingos = []
    is_a_winner = False
    for bingo in bingos:
        bingo.update_number(number_rolled)
        if bingo.is_over():
            is_a_winner = True
            ended_bingos.append(bingo)
    return is_a_winner, ended_bingos


def play_bingo(bingos, number_rolled):
    for number_turn in number_rolled:
        is_ended, bingo = update_bingo(bingos, number_turn)

        if is_ended:
            if len(bingos) == 1:
                print(bingo[0].end())
                return
            for curr_bingo in bingo:
                bingos.remove(curr_bingo)




if __name__ == "__main__":
    number_rolled = get_number(scans[0])
    bingos = instatiate_bingos(scans[1:])

    play_bingo(bingos, number_rolled)
