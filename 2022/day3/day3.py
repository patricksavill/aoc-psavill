import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day3-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
We're trying to find duplicate entries, so let's use a dict

And as the letters have numerical values, let's use the unicode standard
"""


def letter_value(letter):
    unicode_num = ord(letter)
    # A-Z in unicode are 65-90 inclusive
    # a-z in unicode are 97-122 inclusive

    if unicode_num > 96:
        # a-z are valued 1 to 26, so minus 96
        return unicode_num - 96
    elif unicode_num > 64:
        # A-Z are valued 27 to 52, so offset by -65+27
        return unicode_num - 65 + 27


def duplicate_item(first_compart, second_compart):
    # Using a dictionary we can easily find duplicates
    # Make a dictionary of the first compartment,then run through the second
    dict_obj = {}
    for item in first_compart:
        dict_obj[item] = 1
    for item in second_compart:
        if item in dict_obj:
            # this is the duplicate.
            return item


priority_sum = 0
for line in all_lines:
    # Split each rucksack in half and compute with "duplicate_items"
    line = line.rstrip("\n")
    priority_sum += letter_value(duplicate_item(line[0:int(len(line) / 2)], line[int(len(line) / 2):]))

print("Part one priority sum: %d" % priority_sum)

"""
Part two
We're now finding the item that appears across three rucksacks (six compartments)
"""


def three_rucksack_duplicate(rucksacks):
    # Iterative dictionary checking
    dict_one = {}
    dict_two = {}

    # Firstly, just create the dictionary
    for item in rucksacks[0]:
        dict_one[item] = 1

    # Now add everything that exists in both rucksacks
    for item in rucksacks[1]:
        if item in dict_one:
            dict_two[item] = 1

    # And finally find the one thing that exists in all three
    for item in rucksacks[2]:
        if item in dict_two:
            return item


priority_sum_two = 0
for i in range(int(len(all_lines) / 3)):
    ruck_one = all_lines[i * 3].rstrip("\n")
    ruck_two = all_lines[i * 3 + 1].rstrip("\n")
    ruck_three = all_lines[i * 3 + 2].rstrip("\n")

    priority_sum_two += letter_value(three_rucksack_duplicate([ruck_one, ruck_two, ruck_three]))

print("Part two priority value: %d" % priority_sum_two)
