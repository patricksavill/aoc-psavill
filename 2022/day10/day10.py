import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day10-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Computing cycles, carry out operations and total every 20 +nth cycle
noop - takes one cycle
addx - takes two cycles, addition occurs AFTER the 2nd cycle
"""


def signal_strength(cycle, value):
    if (cycle - 20) % 40 == 0:
        # Use modulo to find every 20+nth cycle
        print("Signal strength: %d" % int(cycle * value))
        return cycle*value
    return 0


x_value = 1
cycle_count = 0
signal_total = 0
for line in all_lines:
    if line == "\n":
        continue
    instruction = line.rstrip("\n").split(" ")
    if instruction[0] == "noop":
        cycle_count += 1
        signal_total += signal_strength(cycle_count, x_value)
    elif instruction[0] == "addx":
        for i in range(2):
            # We run two cycles, doing nothing
            cycle_count += 1
            # We check signal strength here again
            signal_total += signal_strength(cycle_count, x_value)
        # After two cycles we increment x
        x_value += int(instruction[1])


print("Part one answer is %d" % signal_total)
