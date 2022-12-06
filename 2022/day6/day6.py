import sys
from pathlib import Path
import queue

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day6-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Detecting first non repeating window of 4 characters
"""

def is_unique(char_window):
    dict_obj = {}
    for c in char_window:
        if c in dict_obj:
            return False
        dict_obj[c] = 1
    return True


index = 0
while (index + 4) < len(all_lines[0]):
    if is_unique(all_lines[0][index:index+4]):
        print(index+4)
        break
    index +=1