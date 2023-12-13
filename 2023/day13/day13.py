import sys
from pathlib import Path
import re
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils


INPUT = "day13-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))


patterns = []
char_arr = []
for l in all_lines:
    if l == "":
        patterns.append(char_arr.copy())
        char_arr = []
    else:
        char_arr.append([str(x) for x in l])


patterns.append(char_arr.copy())
print(len(patterns))

def print_arr(a):
    s = ""
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            if a[x][y] == 1:
                s += "#"
            else:
                s+="."
        s += "\n"
    print(s)

sum = 0
for p in patterns:
    width = len(p)
    height = len(p[0])

    n_arr = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            if p[x][y] == "#":
                n_arr[x][y] = 1

    vertical_num = 0
    for i in range(1,height):
        left = n_arr[:,0:i]
        right = n_arr[:,i:]
        matched_width = min(left.shape[1], right.shape[1])

        left_to_match = left[:,left.shape[1]-matched_width:]
        right_to_match = np.fliplr(right[:,0:matched_width])

        if np.all(left_to_match == right_to_match):
            vertical_num = i
            sum += vertical_num

    horizontal_num = 0
    for i in range(1, width):
        top = n_arr[0:i,:]
        bottom = n_arr[i:,:]
        matched_height = min(top.shape[0], bottom.shape[0])

        top_to_match = top[top.shape[0] - matched_height:, :]
        bottom_to_match = np.flipud(bottom[0:matched_height, :])

        if np.all(top_to_match == bottom_to_match):
            horizontal_num = i
            sum += horizontal_num * 100


    print("%d - vert: %d" % (horizontal_num, vertical_num))

print("2023 day 13 pt 1: %d" % sum)

sum = 0
for p in patterns:
    width = len(p)
    height = len(p[0])

    n_arr = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            if p[x][y] == "#":
                n_arr[x][y] = 1

    vertical_num = 0
    for i in range(1,height):
        left = n_arr[:,0:i]
        right = n_arr[:,i:]
        matched_width = min(left.shape[1], right.shape[1])

        left_to_match = left[:,left.shape[1]-matched_width:]
        right_to_match = np.fliplr(right[:,0:matched_width])

        if (left_to_match.size - np.count_nonzero(left_to_match == right_to_match)) == 1:
            vertical_num = i
            sum += vertical_num

    horizontal_num = 0
    for i in range(1, width):
        top = n_arr[0:i,:]
        bottom = n_arr[i:,:]
        matched_height = min(top.shape[0], bottom.shape[0])

        top_to_match = top[top.shape[0] - matched_height:, :]
        bottom_to_match = np.flipud(bottom[0:matched_height, :])

        if (top_to_match.size - np.count_nonzero(top_to_match == bottom_to_match)) == 1:
            horizontal_num = i
            sum += horizontal_num * 100


    print("%d - vert: %d" % (horizontal_num, vertical_num))

print("2023 day 13 pt 2: %d" % sum)
