import sys
from pathlib import Path
import re
import numpy as np


sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils


INPUT = "day14-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

patterns = []
char_arr = []
for l in all_lines:
    if l == "":
        patterns.append(char_arr.copy())
        char_arr = []
    else:
        char_arr.append([str(x) for x in l])

height = len(char_arr)
width = len(char_arr[0])
n_arr = np.zeros((height, width))
stacked_arr = np.zeros((height, width))
for x in range(height):
    for y in range(width):
        if char_arr[x][y] == "#":
            n_arr[x][y] = 1
            stacked_arr[x][y] = 1
        elif char_arr[x][y] == "O":
            n_arr[x][y] = 2

aoc_utils.print_arr(n_arr)

def stack_rocks(src_arr, dst_arr, debug=False):
    # Per column find the indexes of the cube shaped rocks
    for y in range(src_arr.shape[1]):
        col = src_arr[:,y]
        cube_rocks_index = []
        round_rocks_index = []
        for i in range(len(col)):
            if col[i] == 1:
                cube_rocks_index.append(i)
            elif col[i] == 2:
                round_rocks_index.append(i)
        cube_rocks_index.append(len(src_arr[:,y])+1) # End at the southmost position

        if len(cube_rocks_index) == 1:
            # Edge case were there are no cube rocks in this column except the virtual one we added
            continuous_rocks = np.sum(src_arr[:, y] == 2)

            dst_arr[0:continuous_rocks, y] = 2
            if debug:
                aoc_utils.print_arr(dst_arr)

        for i in range(len(cube_rocks_index)-1):
            s = cube_rocks_index[i]
            e = cube_rocks_index[i + 1]

            # First case where a cube rock exists beyond the first row, need to start those before it
            if i == 0 and s > 0:
                continuous_rocks = np.sum(src_arr[0:s, y] == 2)
                dst_arr[0:0 + continuous_rocks, y] = 2
                if debug:
                    aoc_utils.print_arr(dst_arr)

            # Count number of round rocks between cube rocks
            continuous_rocks = np.sum(src_arr[s:e,y] == 2)

            # Put block of round rocks following cube rock start of range
            dst_arr[s+1:s+1 + continuous_rocks, y] = 2
            if debug:
                aoc_utils.print_arr(dst_arr)


# Now sum up the distance from each rounded rock to the bottom
stack_rocks(n_arr, stacked_arr)
sum_rounded = 0
aoc_utils.print_arr(stacked_arr)
for x in range(height):
    sum_rounded += (height - x) * np.sum(stacked_arr[x,:] == 2)
    print(sum_rounded)
