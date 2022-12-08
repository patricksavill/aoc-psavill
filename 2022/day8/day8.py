import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day8-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Determine how many trees are visible
For a tree to be visible it must have a straight line from it to the edge, with no taller trees in the way
"""

tree_grid = []
visible_grid = []
grid_index = 0
for line in all_lines:
    tree_grid.append([int(x) for x in line.rstrip("\n")])
    visible_grid.append([0] * len(tree_grid[0]))

# Iterate first left to right and right to left each row
# visible _grid: 0 is invisible, 1 is visible
print(tree_grid)
print(visible_grid)


def check_horizontal(row):
    tallest = -1
    for y in range(len(tree_grid[row])):
        if tree_grid[row][y] > tallest:
            visible_grid[row][y] = 1
            tallest = tree_grid[row][y]

    tallest = -1
    # going right to left
    for y in reversed(range(len(tree_grid[row]))):
        if tree_grid[row][y] > tallest:
            visible_grid[row][y] = 1
            tallest = tree_grid[row][y]


def check_vertical(column):
    # top to bottom
    tallest = -1
    for x in range(len(tree_grid)):
        if tree_grid[x][column] > tallest:
            visible_grid[x][column] = 1
            tallest = tree_grid[x][column]

    # bottom to top
    tallest = -1
    for x in reversed(range(len(tree_grid))):
        if tree_grid[x][column] > tallest:
            visible_grid[x][column] = 1
            tallest = tree_grid[x][column]


# Top to bottom
for row_index in range(len(tree_grid)):
    check_horizontal(row_index)

for colum_index in range(len(tree_grid[0])):
    check_vertical(colum_index)

for x in range(len(visible_grid)):
    print(visible_grid[x])

print(sum(sum(visible_grid, [])))
