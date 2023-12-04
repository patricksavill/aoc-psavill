import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day4-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))


def card_won(line: str):
    card_number = re.search(r'[0-9]+',line.split(":")[0]).group()


    nums = line.split(":")[-1].split("|")
    winning_nums = [int(x) for x in nums[0].strip(" ").split(" ") if x != ""]
    scratch_nums = [int(x) for x in nums[1].strip(" ").split(" ") if x != ""]
    matches = 0
    for s in scratch_nums:
        if s in winning_nums:
            matches += 1

    if matches != 0:
        return 2 ** (matches - 1)
    return 0


sum = 0
for l in all_lines:
    print(card_won(l))
    sum += card_won(l)

print("2023 Day 4 pt 1: %d" % sum)
