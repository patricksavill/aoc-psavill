import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day4-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one

Find the pairs where one range is fully enclosed by the other
1-9,7-8 would count as true for example
"""

contained_pairs = 0
for line in all_lines:
    pairs = line.rstrip("\n").split(",")
    range_one = pairs[0].split("-")
    range_two = pairs[1].split("-")
    if int(range_one[0]) <= int(range_two[0]) and int(range_one[1]) >= int(range_two[1]):
        contained_pairs += 1
    elif int(range_one[0]) >= int(range_two[0]) and int(range_one[1]) <= int(range_two[1]):
        contained_pairs += 1

print("Part one container pairs: %d" % contained_pairs)
