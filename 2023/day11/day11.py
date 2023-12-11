import sys
from pathlib import Path
import re
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day11-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

char_arr = []
binary_arr = []
for l in all_lines:
    l = l.rstrip('\n')
    char_arr.append([str(x) for x in l])
    binary_arr.append([0 if x == "." else 1 for x in l])

img_src = np.array(binary_arr)
print(img_src.shape)


def expand_space(array, given_axis, zero_indexes):
    for i in range(len(zero_indexes) - 1, 0, -1):
        # Want to go back to front, so new insertions don't throw out index
        if zero_indexes[i] == 0:
            array = np.insert(array, i, 0, axis=given_axis)
    return array


zero_col_index = np.sum(binary_arr, axis=1)  # Sum columns
zero_row_index = np.sum(binary_arr, axis=0)  # Sum rows

col_expansion = expand_space(binary_arr, 0, zero_col_index)
row_expansion = expand_space(col_expansion, 1, zero_row_index)

print(col_expansion.shape)
print(row_expansion.shape)

sum_dist = 0
x, y = np.where(row_expansion == 1)
for i in range(len(x)):
    src_x = x[i]
    src_y = y[i]
    for j in range(i + 1, len(x)):
        dst_x = x[j]
        dst_y = y[j]

        dist = dst_x - src_x + dst_y - src_y
        sum_dist += np.abs(dst_x - src_x) + np.abs(dst_y - src_y)

print("2023 day 11 pt 1: %d" % sum_dist)

# Part 2, can't expand numpy arrays, have to add expanded dimensions to path length
sum_dist = 0
expansion_offset = 1000000-1 # Expansion -1, as we count the source row still

# Use x, y indexes from source, not expanded array
x, y = np.where(img_src == 1)
for i in range(len(x)):
    src_x = x[i]
    src_y = y[i]
    for j in range(i + 1, len(x)):
        dst_x = x[j]
        dst_y = y[j]

        dist = dst_x - src_x + dst_y - src_y
        sum_dist += np.abs(dst_x - src_x) + np.abs(dst_y - src_y)

        # Get the vector of all galaxies that need expansion and are crossed in this path
        expand_x_arr = zero_col_index[min(src_x, dst_x):max(src_x, dst_x)]
        expand_y_arr = zero_row_index[min(src_y, dst_y):max(src_y, dst_y)]

        # Add the expansion offset equal to the number of crossed expanded space areas
        sum_dist += np.sum(expand_x_arr == 0) * expansion_offset
        sum_dist += np.sum(expand_y_arr == 0) * expansion_offset


print("2023 day 11 pt 2: %d" % sum_dist)
