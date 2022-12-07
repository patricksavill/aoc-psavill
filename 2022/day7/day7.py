import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day7-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Read in the commands to form a directory structure
Recurse through the directory structure to find directory sizes
"""


class Directory():
    parent = ""
    children = {}
    files = {}
    def __init__(self):
        self.data = []

    def set_parent(self, parent_dir):
        parent = parent_dir

    def add_child(self, dir_child):
        self.children[dir_child] = Directory()

    def add_files(self, file_data):
        self.files[file_data[-1]] = file_data[0]

    def has_child(self, dir_name):
        if dir_name in self.children:
            return True
        return False

    def pretty_print(self, levels):
        dir_indent = "-"*levels
        for f in self.files:
            print(dir_indent + f)
        for c in self.children:
            c.pretty_print(levels+1)



def is_command(line):
    if "$" in line:
        return True
    return False

dir = Directory()
working_dir = dir

for line in all_lines:
    line = line.rstrip("\n")
    if is_command(line):
        # We're either cd, or ls
        print(line)
        if "cd" in line:
            dir_name = line.split("cd ")[-1]
            if dir_name == "..":
                print("\n\nmoving up")
                working_dir = dir.parent
            elif dir_name == "/":
                # Jump up to root
                while dir.parent != "":
                    dir = dir.parent
            else:
                if dir.has_child(dir_name):
                    dir = dir.children[dir_name]
                else:
                    dir.add_child(dir_name)
                    dir.children[dir_name].parent = dir

    else:
        # Here we're parsing the output of ls
        # Parse and append to the working_item
        if "dir" in line:
            print("is dir")
            dir_name = line.split("dir ")[-1]
            dir.add_child(dir_name)
        else:
            print("is file")
            file_attr = line.split(" ")
            dir.add_files(file_attr)
        print(line)

print(" ")
dir.pretty_print(0)
