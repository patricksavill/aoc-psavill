import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day1-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

def calibration_reader(line_list, debug = False):
    sum = 0
    for l in line_list:
        first_num = -1
        last_num = -1
        for p in l:
            if p == "\\":
                break
            if p in "0123456789":
                if first_num == -1:
                    first_num = int(p)
                else:
                    last_num = int(p)
        if last_num == -1:
            last_num = first_num
        if debug:
            print("%d - %d - %d" % (first_num, last_num, first_num*10 + last_num))
        sum += first_num*10 + last_num
    return sum
print("Final sum for day 1 is %d" % calibration_reader(all_lines))

def words_to_numbers(line):
    num_dict = {"one":1,
             "two":2,
             "three":3,
             "four":4,
             "five":5,
             "six":6,
             "seven":7,
             "eight":8,
             "nine" : 9}

    for k in num_dict:
        # Cheeky replacement. twone becomes two2twoone
        line = line.replace(k, k + str(num_dict[k]) + k)

    return line

sub_lines = []
for l in all_lines:
    sub_lines.append(words_to_numbers(l))

print("Final sum for day 1 part 2 is %d" % calibration_reader(sub_lines, debug=True))
