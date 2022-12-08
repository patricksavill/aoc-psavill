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

# Nice debug visual on small inputs
# for x in range(len(visible_grid)):
#    print(visible_grid[x])

print(sum(sum(visible_grid, [])))

"""
Part two:
Find the "scene score" of any given tree
Find product of summed viewable trees out from a given tree in the grid

Note this is a distance of trees, not sum of viewed trees
so reading right on 53353 from 5 gives a distance of 3, not 1

We stop when we reach a tree of the same height, or taller, as the initial tree
"""


def sum_left(x, y, max_height):
    # Requirement for tallest is it must be at least 1 unit higher than the last
    total = 0
    while x >= 0:
        total += 1
        if tree_grid[x][y] >= max_height:
            return total
        x -= 1

    return total


def sum_right(x, y, max_height):
    total = 0
    while x < len(tree_grid):
        total += 1
        if tree_grid[x][y] >= max_height:
            return total
        x += 1

    return total


def sum_down(x, y, max_height):
    total = 0
    while y < len(tree_grid):
        total += 1
        if tree_grid[x][y] >= max_height:
            return total
        y += 1

    return total


def sum_up(x, y, max_height):
    total = 0
    while y >= 0:
        total += 1
        if tree_grid[x][y] >= max_height:
            return total
        y -= 1

    return total


def scenic_score(row, column, max_height):
    left = sum_left(row - 1, column, max_height)
    right = sum_right(row + 1, column, max_height)
    down = sum_down(row, column + 1, max_height)
    up = sum_up(row, column - 1, max_height)

    return left * right * down * up


max_score = 0
for row in range(len(tree_grid)):
    for column in range(len(tree_grid[row])):
        score = scenic_score(row, column, tree_grid[row][column])
        max_score = score if score > max_score else max_score

print(max_score)
