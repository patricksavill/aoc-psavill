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

One thing that tripped me up was duplicate folder names in the input,
 a child could be named the same as a parent

"""


class Directory():
    parent = ""
    children = {}
    files = {}
    total_size = 0

    def __init__(self):
        self.data = []
        self.parent = ""
        self.children = {}
        self.files = {}
        self.total_size = 0

    def set_parent(self, parent_dir):
        self.parent = parent_dir

    def add_child(self, dir_child):
        self.children[dir_child] = Directory()

    def add_files(self, file_data):
        self.files[file_data[-1]] = file_data[0]
        self.total_size += int(file_data[0])

    def has_child(self, dir_name):
        if dir_name in self.children:
            return True
        return False

    def pretty_print(self, levels):
        dir_indent = "- " * levels
        for f in self.files:
            print(dir_indent + f + " size: " + self.files[f])
        for c in self.children:
            print(dir_indent + c + "(dir)")
            self.children[c].pretty_print(levels + 1)

    def print_sizes(self):
        for c in self.children:
            print(c + " size " + str(self.children[c].total_size))
            self.children[c].print_sizes()

    def sum_part_one(self):
        sum_part = 0
        for c in self.children:
            if self.children[c].total_size <= 100000:
                sum_part += self.children[c].total_size
            sum_part += self.children[c].sum_part_one()
        return sum_part

    def sum_part_two(self, goal, candidates):
        # Add itself to candidates if >= goal
        if self.total_size >= goal:
            candidates.append(self.total_size)

        for c in self.children:
            self.children[c].sum_part_two(goal, candidates)


    def sum_sizes(self):
        for c in self.children:
            self.total_size += self.children[c].sum_sizes()
        return self.total_size


def is_command(line):
    if "$" in line:
        return True
    return False


dir = Directory()
root_dir = dir

for line in all_lines:
    line = line.rstrip("\n")
    if is_command(line):
        # We're either cd, or ls
        if "cd" in line:
            dir_name = line.split("cd ")[-1]
            if dir_name == "..":
                dir = dir.parent
            elif dir_name == "/":
                # Jump up to root
                dir = root_dir
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
            dir_name = line.split("dir ")[-1]
            dir.add_child(dir_name)
            dir.children[dir_name].parent = dir
        else:
            file_attr = line.split(" ")
            dir.add_files(file_attr)

print(" ")
root_dir.pretty_print(0)

# Sum up dir sizes
root_dir.sum_sizes()
root_dir.print_sizes()

print("\nPart one sum: %d" % root_dir.sum_part_one())

"""
Part two:
Delete the smallest directory that will still free up enough space
The total space is 70,000,000, we want 30,000,000 free
The current free space is equal to the 70,000,000 - root_dir.total_size
Thus the goal for subdir to delete is:
root_dir.total_size - (total_disk_size - goal_size) = dir to delete
root_dir.total_size - 40,000,000

"""

candidate = []
root_dir.sum_part_two(root_dir.total_size- 40000000, candidate)
print("Part two answer is %d" % min(candidate))
