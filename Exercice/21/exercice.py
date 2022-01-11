import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Player:
    def __init__(self, startingpos):
        self.position = startingpos
        self.score = 0


def play(Player1, Player2, target_score, number_of_rolls = 0):

    while True:

        for player in [Player1, Player2]:

            for dice in range(1, 4):
                # on change la position
                player.position += turn
                if player.position > 10:
                    player.position -= 10



                number_of_rolls += 1

            # on ajoute le score
            player.score += player.position
            if Player1.score >= target_score or Player2.score >= target_score:
                return number_of_rolls * min([Player1.score, Player2.score])




if __name__ == "__main__":
    player_1 = Player(int(scans[0].split(": ")[1]))
    player_2 = Player(int(scans[1].split(": ")[1]))
    print(play(player_1, player_2, 21))
