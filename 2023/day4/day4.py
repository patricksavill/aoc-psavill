import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day4-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))


def card_won(line: str, num_matches=False):
    card_number = re.search(r'[0-9]+',line.split(":")[0]).group()

    nums = line.split(":")[-1].split("|")
    winning_nums = [int(x) for x in nums[0].strip(" ").split(" ") if x != ""]
    scratch_nums = [int(x) for x in nums[1].strip(" ").split(" ") if x != ""]
    matches = 0
    for s in scratch_nums:
        if s in winning_nums:
            matches += 1

    if num_matches:
        return matches # this if for part 2
    if matches != 0:
        return 2 ** (matches - 1)
    return 0


sum = 0
for l in all_lines:
    print(card_won(l))
    sum += card_won(l)

print("2023 Day 4 pt 1: %d" % sum)

card_dict = {}
for i in range(len(all_lines)):
    if i not in card_dict.keys():
        # Initialise as 1 card
        card_dict[i] = 1

    for count in range(0,card_dict[i]):
        num_matches = card_won(all_lines[i], num_matches=True)
        for n in range(i+1, i+num_matches+1):
            if n not in card_dict.keys():
                card_dict[n] = 2 # We know there's one original, and then add this copy
            else:
                card_dict[n] = card_dict[n] + 1

print(card_dict)
total_cards = 0
for k in card_dict:
    total_cards += card_dict[k]
print("2023 Day 4 pt 2: %d" % total_cards)

