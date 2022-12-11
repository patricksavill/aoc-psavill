import sys
from pathlib import Path
import math

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day9-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Follow along the moving head of a rope and count the squares the tail moves through

The tail moves inline with the head whenever possible
So the check is:
if (tail->head distance < threshold):
    nothing
else:
    move tail inline with head, jumping in line with row or column
"""

# Using globals
head_x = 0
head_y = 0
tail_x = 0
tail_y = 0


def tail_touching():
    """
    Determine if the head is too far from the tail or not
    Each dimension has to be within 1 unit

    :return: true if "touching"
    """
    if math.fabs(head_x - tail_x) > 1:
        return False
    if math.fabs(head_y - tail_y) > 1:
        return False

    print(math.fabs(-1))


def print_visited(grid):
    for i in range(len(grid)):
        print(grid[i])


def move_tail():
    global head_y, head_x, tail_y, tail_x
    # Move tail to within 1 unit of the head

    # First we determine which distance is greatest
    # We then jump inline with the head on the smaller axis

    if math.fabs(head_x - tail_x) > 1:
        # X is the greatest, so increment that and move tail_y to head_y
        tail_x += int(math.copysign(1, head_x - tail_x))
        tail_y = head_y

    elif math.fabs(head_y - tail_y) > 1:
        # Y is the greatest, so increment that and move tail_x to head_x
        tail_y += int(math.copysign(1, head_y - tail_y))
        tail_x = head_x


def move_head(dir, steps):
    global head_y, head_x, tail_y, tail_x
    while steps > 0:
        if dir == "R":
            head_x += 1
        elif dir == "U":
            head_y += 1
        elif dir == "L":
            head_x -= 1
        elif dir == "D":
            head_y -= 1

        # Catch the tail up
        move_tail()
        # Update the visited grid (Y first, to get vertical index)
        visited_grid[tail_y][tail_x] = 1
        steps -= 1

        # print_visited(visited_grid)
        # print("\n\n")


grid_size = 1000 # Iteratively built this bigger
visited_grid = []
for i in range(grid_size):
    visited_grid.append([0] * grid_size)

for line in all_lines:
    moves = line.rstrip("\n").split(" ")
    move_head(moves[0], int(moves[1]))

print(sum(sum(visited_grid, [])))
