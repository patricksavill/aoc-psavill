import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day8-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

instrs = [c for c in all_lines[0]]

map_nodes = {}

for l in all_lines:
    if "=" in l:
        parts = l.split("=")
        key = parts[0].rstrip(" ")
        left = parts[1].split(",")[0].strip(" ()")
        right = parts[1].split(",")[1].strip(" ()")
        print(parts, key, left, right)
        map_nodes[key] = [left, right]

print(map_nodes)
current_node = "AAA"
steps = 0
instr_count = 0
while current_node != "ZZZ":
    if instr_count == len(instrs):
        # Loop around instructions
        instr_count = 0
    step_instr = instrs[instr_count]
    if step_instr == "L":
        current_node = map_nodes[current_node][0]
    else:
        current_node = map_nodes[current_node][1]

    steps += 1
    instr_count += 1

print(steps)
