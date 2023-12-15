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

print("2023 day 14 pt 1: %d" % sum_rounded)


# Now part 2
stacked_arr = np.zeros((height, width))
for x in range(height):
    for y in range(width):
        if char_arr[x][y] == "#":
            stacked_arr[x][y] = 1


# Every 100 cycles we write into a list
# We check that list for matches of the current cycle
# If it matches, we know the repeated cycle range we can skip forward, and get the same result
# We thus skip forward as far as we can, then keep iterating until we reach the target cycles

cycles = 1000000000
src_arr = n_arr
aoc_utils.print_arr(src_arr)
cache_iter = []
cycle_cache_repetition = 10
c = 0
while c < cycles:
    for i in range(4):
        stack_rocks(src_arr, stacked_arr, debug=False)
        src_arr = np.rot90(stacked_arr.copy(),3)
        stacked_arr = np.rot90(stacked_arr,3)
        if i != 3:
            stacked_arr[np.where(stacked_arr == 2)] = 0
    if c % cycle_cache_repetition == 0:

        if len(cache_iter) > 0:
            # Search for a match
            for ci in range(len(cache_iter)):
                if np.all(cache_iter[ci] == src_arr):
                    print("Cache num: %d\tCycle num: %d" % (ci, c))
                    repeated_range = (c-ci*cycle_cache_repetition)
                    skippable = (cycles - c) // repeated_range
                    c += skippable*repeated_range

        cache_iter.append(src_arr)
        print(c)
    if c != cycles-1:
        # Reset the stacked array for writing into, prevents duplicated rocks (in current implementation)
        stacked_arr[np.where(stacked_arr == 2)] = 0

    c += 1


sum_rounded = 0
aoc_utils.print_arr(stacked_arr)
for x in range(height):
    sum_rounded += (height - x) * np.sum(stacked_arr[x,:] == 2)

print("2023 day 14 pt 2: %d" % sum_rounded)
