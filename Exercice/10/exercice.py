import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class Chunk:
    def __init__(self, signe):
        self.signe = signe
        self.contenu = ""

    def add_char(self, char):
        self.contenu += char

    def close(self):
        self.contenu = self.contenu[:-1]

    def is_valid(self):
        parenth_count = 0
        fleche_count = 0
        crochet_count = 0
        acolade_count = 0

        for char in self.contenu:
            if char == "(":
                parenth_count += 1
            if char == "<":
                fleche_count += 1
            if char == "[":
                crochet_count += 1
            if char == "{":
                acolade_count += 1

            if char == ")":
                parenth_count -= 1
            if char == ">":
                fleche_count -= 1
            if char == "]":
                crochet_count -= 1
            if char == "}":
                acolade_count -= 1

        return parenth_count == 0 and fleche_count == 0 and crochet_count == 0 and acolade_count == 0


def opposite(char):
    if char == ")":
        return "("
    if char == ">":
        return "<"
    if char == "]":
        return "["
    if char == "}":
        return "{"


def get_last_chunk_of_type(char, opened_chunk):
    openned_char = opposite(char)
    for i in range(len(opened_chunk)):
        if opened_chunk[-(i + 1)].signe == openned_char:
            return opened_chunk[-(i + 1)]
    return None


def get_value(char):
    if char == ")":
        return 3
    if char == ">":
        return 25137
    if char == "]":
        return 57
    if char == "}":
        return 1197


def solve(scans):
    points = 0
    scores = []
    for line in scans:
        is_corrupted = False
        opened_chunk = []
        for char in line:
            [current_chunk.add_char(char) for current_chunk in opened_chunk]

            if char == '(' or char == '[' or char == '{' or char == '<':
                opened_chunk.append(Chunk(char))
            else:
                closed_chunk = get_last_chunk_of_type(char, opened_chunk)
                if not closed_chunk:
                    points += get_value(char)
                    is_corrupted = True
                    break
                opened_chunk.remove(closed_chunk)

                closed_chunk.close()

                if not closed_chunk.is_valid():
                    points += get_value(char)
                    is_corrupted = True
                    break

        if is_corrupted:
            continue
        local_score = 0
        opened_chunk.reverse()
        for remaining_scores in opened_chunk:
            local_score *= 5
            local_score += get_value2(remaining_scores.signe)
        scores.append(local_score)

    return points, scores


def get_value2(char):
    if char == "(":
        return 1
    if char == "<":
        return 4
    if char == "[":
        return 2
    if char == "{":
        return 3


def sovle_for_incomplete_lines(scans):
    scores = []
    for line in scans:
        opened_chunk = []
        for char in line:
            [current_chunk.add_char(char) for current_chunk in opened_chunk]

            if char == '(' or char == '[' or char == '{' or char == '<':
                opened_chunk.append(Chunk(char))
            else:
                closed_chunk = get_last_chunk_of_type(char, opened_chunk)
                opened_chunk.remove(closed_chunk)
                closed_chunk.close()






    return scores


def sort(scores):
    sorted_score = []
    while scores:
        higest_score = 0
        for current_score in scores:
            if current_score > higest_score:
                higest_score = current_score

        scores.remove(higest_score)
        sorted_score.append(higest_score)
    return sorted_score

if __name__ == "__main__":
    points, scores = solve(scans)
    scores = sort(scores)
    print(scores[len(scores)//2])
