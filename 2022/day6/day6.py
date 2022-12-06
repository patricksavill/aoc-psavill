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
        print("Part one's answer is %d " % (index+4))
        break
    index +=1

"""
Part two:
Same as part one, but a window of 14 characters

Note: made a window variable here, it's more readable
"""
index = 0
window = 14
while (index + window) < len(all_lines[0]):
    if is_unique(all_lines[0][index:index + window]):
        print("Part two's answer is %d" % (index + window))
        break
    index += 1