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

# Part 2

starting_nodes = []
for k in map_nodes.keys():
    if k.endswith("A"):
        starting_nodes.append(k)

steps = 0
instr_count = 0

# Really we want to find loops, then the lowest common multiple of all the loop lengths
loops = []
for i in range(len(starting_nodes)):
    instr_count = 0
    steps = 0
    while True:
        if instr_count == len(instrs):
            # Loop around instructions
            instr_count = 0

        step_instr = instrs[instr_count]
        if step_instr == "L":
            starting_nodes[i] = map_nodes[starting_nodes[i]][0]
        else:
            starting_nodes[i] = map_nodes[starting_nodes[i]][1]


        steps += 1
        instr_count += 1
        if starting_nodes[i].endswith("Z"):
            loops.append(steps)
            break

# Took these two functions from stack overflow:
# https://stackoverflow.com/a/147539
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


running_lcm = loops[0]
for l in loops:
    if running_lcm == l:
        continue
    else:
        running_lcm = lcm(running_lcm, l)
    print(l)

print("2023 day 8 pt 2 %d", running_lcm)