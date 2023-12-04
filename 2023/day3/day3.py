import sys
from pathlib import Path
import re
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day3-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

def neighbouring_symbol(c_arr, x1, x2, y1, debug=False):
    """
    Checks all surrounding squares for a character

    :param c_arr: Array of all characters
    :param x1: Start of number
    :param x2: End of number
    :param y1: Line to search on
    :return: True if a special symbol is found
    """

    max_y = len(c_arr)
    max_x = len(c_arr[y1])

    for y in range(y1-1, y1+2):
        for x in range(x1-1, x2+1):
            if debug:
                print("%d - %d - %s" % (y, x, c_arr[y][x]))
            if 0 <= y < max_y and 0 <= x < max_x:
                if str(c_arr[y][x]) in "/=$*&+-#%@!^()":
                    return True
    return False

test_arr = []
test_arr.append([x for x in "abcdefg"])
test_arr.append([x for x in "abc8efg"])
test_arr.append([x for x in "abcdefg"])

neighbouring_symbol(test_arr, 3,4,1, debug=True)


char_arr = []
for l in all_lines:
    char_arr.append([str(x) for x in l])

sum = 0
for l in all_lines:
    y_index = all_lines.index(l)

    while re.search(r'[0-9]+', l) is not None:
        index = re.search(r'[0-9]+', l).span()
        value = re.search(r'[0-9]+', l).group()
        if int(value) == 102:
            debug = True
        valid_part = neighbouring_symbol(char_arr, index[0], index[1], y_index)
        print("%d - %s" % (int(value), valid_part))
        if valid_part:
            sum += int(value)

        # Remove the number we just used
        dots = "".join(["." for v in value])
        l = re.sub(r'[0-9]+', dots, l, count=1)

print("Day 3 part 1 %d" % sum)
