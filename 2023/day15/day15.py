import sys
from pathlib import Path
import re
import numpy as np


sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils


INPUT = "day15-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))


def hash_alg(c, current_value=0):
    val = ord(c)
    current_value += val
    current_value = current_value*17
    current_value = current_value % 256
    return current_value

hash_blocks = all_lines[0].split(",")

c_vals = []
for b in hash_blocks:
    c_val = 0
    for h in b:
        c_val = hash_alg(h, c_val)
        print(c_val)
    c_vals.append(c_val)

print(c_vals)
print("2023 day 15 pt 1: %d" % np.sum(np.array(c_vals)))

# Part 2

def index_in_list(c, l):
    for i in range(len(l)):
        if c in l[i]:
            # Double check this isn't a partial match
            label = l[i].split(" ")[0]
            if c == label:
                return i
    return -1

# Initialise lens box
lens_box = {}
for i in range(256):
    lens_box[i] = []

for b in hash_blocks:
    # Split on both = and - to get the label to hash on
    label = b.split("=")[0]
    label = label.split("-")[0]

    lens = re.sub("[-=]", " ", b)

    box_index = 0
    for h in label:
        box_index = hash_alg(h, box_index)

    if len(lens_box[box_index]) == 0 and "-" not in b:
        lens_box[box_index].append(lens)
    else:
        contents = lens_box[box_index]
        existing_index = index_in_list(label,contents)
        if existing_index >= 0:
            if "=" in b:
                # Replace lens
                lens_box[box_index][existing_index] = lens
            elif '-' in b:
                # Remove lens
                lens_box[box_index].remove(lens_box[box_index][existing_index])
            else:
                print("Hit edge case, shouldn't occur")
        elif "=" in b:
            lens_box[box_index].append(lens)
print(lens_box)

focus_power = 0
for k in lens_box:
    box_num = k +1
    for i in range(len(lens_box[k])):
        focus_power += box_num * int(lens_box[k][i].split(" ")[-1]) * (i+1)


print("2023 day 15 pt 2: %d" % focus_power)