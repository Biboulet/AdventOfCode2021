import os

class Vector2:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y



def read_file(path):
    if os.path.isfile(path):
        return open(path, "r").read().splitlines()
    print("File does not exist")

