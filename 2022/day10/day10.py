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


def signal_strength(cycle, value, logging=True):
    if (cycle - 20) % 40 == 0:
        # Use modulo to find every 20+nth cycle
        if logging:
            print("Signal strength: %d" % int(cycle * value))
        return cycle * value
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

"""
Part two:
Really having to think about code here

So we draw exactly 220 pixels, one per cycle
if the pixel we're drawing is occupied by the 3-pixel wide sprite we show #
Else we show .

Then we (humans) look at the output and read the eight capital letters drawn
"""

output_chars = []
line_break_cycle = 40


def per_clock_cycle(sprite, cycle):
    # Determine cursor position
    cursor_pos = cycle % line_break_cycle - 1
    if cursor_pos == 0:
        # At the start of a new line, add another list to output_chars
        output_chars.append([])

    # Compare to sprite position, sprite is 3 pixels wide
    if sprite >= cursor_pos - 1 and sprite <= cursor_pos + 1:
        output_chars[-1].append("X")
    else:
        output_chars[-1].append(".")


sprite_position = 1
cycle_count = 0
for line in all_lines:
    if line == "\n":
        continue
    instruction = line.rstrip("\n").split(" ")
    if instruction[0] == "noop":
        cycle_count += 1
        per_clock_cycle(sprite_position, cycle_count)
    elif instruction[0] == "addx":
        for i in range(2):
            # We run two cycles, doing nothing
            cycle_count += 1
            # We check signal strength here again
            per_clock_cycle(sprite_position, cycle_count)
        # After two cycles we increment the sprite position
        sprite_position += int(instruction[1])

for i in range(len(output_chars)):
    print("".join(output_chars[i]))
print("Part two answer is above")
