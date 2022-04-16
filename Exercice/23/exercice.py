import os
import utils
import unittest
import functools

scans = utils.read_file(os.getcwd() + "\\input.txt")

dict_energy_of_letter = {"A": 1, "B": 10, "C": 100, "D": 1000}
dict_colomnX_of_letter = {"A": 3, "B": 5, "C": 7, "D": 9}
dict_colomn_index_of_colomnX = {3:0, 5:1, 7:2, 9:3}
list_colomn_index = ["A", "B", "C", "D"]
list_coord = [(3, -5), (5, -5), (7, -5), (9, -5)]
forbidden_cases = [(3, -1), (5, -1), (7, -1), (9, -1)]


class Test(unittest.TestCase):
    def test_colomn(self):
        t1 = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".splitlines()
        t2 = """#############
#...........#
###D#A#B#C###
  #A#B#C#D#
  #A#B#C#D#
  #B#A#D#C#
  #########""".splitlines()
        t3 = """#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########""".splitlines()
        self.assertEqual(sum(parse_board(t1).all_colomn_state()), 400)
        self.assertEqual(sum(parse_board(t2).all_colomn_state()), -4)
        self.assertEqual(sum(parse_board(t3).all_colomn_state()), 0)
        self.assertTrue(parse_board(t1).is_end())

    def test_moves(self):
        t1 = """#############
#...........#
###.#A#C#D###
  #.#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".splitlines()
        t2 = """#############
#...........#
###D#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".splitlines()
        t3 = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".splitlines()

        self.assertEqual(len(parse_board(t1).all_next_moves()), 1)
        self.assertEqual(len(parse_board(t2).all_next_moves()), 7)
        self.assertEqual(len(parse_board(t3).all_next_moves()), 0)

    def test_hash(self):
        t1 = """#############
#...........#
###D#B#A#C###
  #A#B#C#D#
  #A#B#C#D#
  #B#A#D#C#
  #########""".splitlines()
        t2 = """#############
#...........#
###D#A#B#C###
  #A#B#C#D#
  #A#B#C#D#
  #B#A#D#C#
  #########""".splitlines()
        self.assertNotEqual(hash(parse_board(t1)), hash(parse_board(t2)))
        self.assertNotEqual(parse_board(t1), parse_board(t2))
        c = {parse_board(t1), parse_board(t2)}
        self.assertEqual(len(c), 2)

    def test_dijkstra(self):
        t1 = """#############
#...........#
###B#A#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".splitlines()

        self.assertEqual(solve_board(parse_board(t1)), 46)


class Colomn:
    def __init__(self, index, board):
        self.letter = list_colomn_index[index]
        self.cases = []
        x, _y = list_coord[index]
        for y in range(_y, _y + 4):
            self.cases.append(board[(x, y)])


class Board:
    def __init__(self, dict, energy=0):
        self.board = dict
        self.energy = energy

    def __str__(self):
        _str = ""
        previous_y = 0
        for key in self.board.keys():
            if key[1] != previous_y:
                _str += "\n"
                previous_y = key[1]
            _str += str(self.board[key])
        return _str

    def __hash__(self):
        return hash("".join([str(char) for char in self.board.values()]))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def is_end(self):
        return sum(self.all_colomn_state()) == 400

    # return tt les boards possible depuis cette configuration
    def all_next_moves(self):
        moves = []
        antipods = self.get_antipods_pos()
        colomns_state = self.all_colomn_state()
        for antipod_pos in antipods:
            if antipod_can_move(antipod_pos, colomns_state):
                all_moves = get_moves(self.board, antipod_pos)
                if not len(all_moves):
                    continue
                all_moves, priority_move_founded = self.sort_moves(all_moves, self.board[antipod_pos])
                if priority_move_founded:
                    return [self.move_to_board(all_moves[0], antipod_pos)]
                else:
                    moves += [self.move_to_board(move, antipod_pos) for move in all_moves]
        return moves

    def all_colomn_state(self):
        colomns = self.instantiate_colomn()
        return [self.get_colomn_state(colomn) for colomn in colomns]

    def get_colomn_state(self, colomn):
        state = 0
        for case in colomn.cases:
            if case == colomn.letter:
                state += 25
            elif case != ".":
                return -1
        return state

    def instantiate_colomn(self):
        colomn = []
        for i in range(4):
            colomn.append(Colomn(i, self.board))
        return colomn

    def get_antipods_pos(self):
        antipods_pos = []
        for key in self.board.keys():
            case = self.board[key]
            if case in ["A", "B", "C", "D"]:
                antipods_pos.append(key)
        return antipods_pos

    def sort_moves(self, all_moves, letter):
        sorted_moves = []
        x_target_colomn = dict_colomnX_of_letter[letter]
        colomn = Colomn(list_colomn_index.index(letter), self.board)
        for move in all_moves:

            is_forbidden = move[:2] in forbidden_cases
            if is_forbidden:
                continue

            is_corridor = move[1] == -1
            if is_corridor:
                sorted_moves.append(move)
                continue

            is_final_colomn = move[0] == x_target_colomn
            colomn_enterable = self.get_colomn_state(colomn) != -1
            can_enter_final_colomn = is_final_colomn and not is_corridor and colomn_enterable
            if can_enter_final_colomn:
                return [(move[0], self.lowest_position_in_colomn(colomn), move[2])], True

        return sorted_moves, False

    def lowest_position_in_colomn(self, colomn):
        return -5 + colomn.cases.index(".")

    def move_to_board(self, move, antipod_pos):
        new_board = self.board.copy()
        new_board[move[:2]] = self.board[antipod_pos]
        new_board[antipod_pos] = "."
        return Board(new_board, self.energy + move[2] * dict_energy_of_letter[self.board[antipod_pos]])


def antipod_can_move(pos, colomn_state):
    if pos[1] == -1:
        return True
    return colomn_state[dict_colomn_index_of_colomnX[pos[0]]] == -1


def get_moves(board, antipod_pos):
    moves = []
    seen_position = []
    queue = [(antipod_pos[0], antipod_pos[1], 0)]

    while len(queue):
        current = queue[0]
        queue.remove(current)
        if board[current[:2]] == "." or current[:2] == antipod_pos:
            if current[:2] not in seen_position:
                moves.append(current)
                seen_position.append(current[:2])

                queue.append((current[0] + 1, current[1], current[2] + 1))
                queue.append((current[0] - 1, current[1], current[2] + 1))
                queue.append((current[0], current[1] + 1, current[2] + 1))
                queue.append((current[0], current[1] - 1, current[2] + 1))
    moves.remove(moves[0])
    return moves


def parse_board(scans):
    board = {}
    for y, line in enumerate(scans):
        for x, char in enumerate(line):
            board[(x, -y)] = char
    return Board(board)


def get_lowest_board(boards):
    smallest = None
    first = True
    for board in boards:
        if first:
            first = False
            smallest = board
            continue

        if board.energy < smallest.energy:
            smallest = board
    print(smallest.energy, "", len(boards))
    return smallest


def solve_board(base_board):
    current_board = base_board
    boards = {base_board}
    while not current_board.is_end():
        current_board = get_lowest_board(boards)
        boards.remove(current_board)
        c = current_board.all_next_moves()
        [boards.add(board) for board in c]

    return current_board.energy


if __name__ == "__main__":
    main_board = parse_board(scans)
    print(solve_board(main_board))
