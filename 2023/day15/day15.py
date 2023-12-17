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