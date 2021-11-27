import os


def read_file(path):
    if os.path.isfile(path):
        return open(path, "r").readlines()
    print("File does not exist")

