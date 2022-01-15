import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")

D = {}


def get_number_of_wins(score1, score2, pos1, pos2):
    if score1 >= 21:
        return (1, 0)
    if score2 >= 21:
        return (0, 1)

    if (score1, score2, pos1, pos2) in D:
        return D[(score1, score2, pos1, pos2)]

    number_of_wins = (0, 0)
    for dice1 in [1, 2, 3]:
        for dice2 in [1, 2, 3]:
            for dice3 in [1, 2, 3]:
                new_pos = (pos1 + dice1 + dice2 + dice3) % 10
                new_score = score1 + new_pos + 1
                x1, y1 = get_number_of_wins(score2, new_score, pos2, new_pos)
                number_of_wins = (number_of_wins[0] + y1, number_of_wins[1] + x1)
    D[(score1, score2, pos1, pos2)] = number_of_wins
    return number_of_wins


if __name__ == "__main__":
    a = get_number_of_wins(0, 0, 5, 8)
    print(max(a))
    print(a)
