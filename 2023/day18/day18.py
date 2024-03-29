import sys
from pathlib import Path
import re
import numpy as np
sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day18-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

from enum import Enum

class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

# Need to have an array we add columns and horizontals too as we expand

dirt = np.zeros((1,1))
x = 0
y = 0
for l in all_lines:
    d, digs, col = l.split(" ")

    digs = int(digs)
    while digs > 0:
        dirt[y,x] = 1
        digs -=1
        if d == "R":
                x = x+1
        if d == "L":
                x = x-1
        if d == "D":
                y = y+1
        if d == "U":
                y = y-1

        try:
            if x > (dirt.shape[1]-1):
                dirt = np.hstack((dirt, np.zeros((dirt.shape[0], 1))))
            elif x < 0:
                # Have to shift whole array to the right
                dirt = np.hstack((np.zeros((dirt.shape[0], 1)), dirt))
                x +=1

            if y > (dirt.shape[0]-1):
                dirt = np.vstack((dirt, np.zeros((1,dirt.shape[1]))))
            elif y < 0:
                # Have to shift whole array to the right
                dirt = np.vstack((np.zeros((1,dirt.shape[1])), dirt))
                y += 1
        except ValueError:
            print("Broken hstack/vstack")

def flood_fill(src_grid):
    # Make an enclosing grid to fill in outer edges with flood fill
    grid = np.zeros((src_grid.shape[0] +2, src_grid.shape[1]+2))

    for x in range(1,grid.shape[0]-1):
        for y in range(1,grid.shape[1]-1):
            if src_grid[x-1][y-1] != 0:
                grid[x,y] = 1 # Means there's something here


    flooding_coords = [[0,0]]
    while len(flooding_coords) > 0:
        x, y = flooding_coords.pop()
        if grid[x,y] == 0:
            grid[x,y] = 2

        if x+1 < grid.shape[0]:
            if grid[x+1,y] ==0:
                flooding_coords.append([x+1,y])
        if y+1 < grid.shape[1]:
            if grid[x,y+1] ==0:
                flooding_coords.append([x,y+1])
        if x-1 >=0:
            if grid[x-1,y] == 0:
                flooding_coords.append([x-1,y])
        if y-1 >=0:
            if grid[x,y-1] == 0:
                flooding_coords.append([x, y-1])

    return grid

filled = flood_fill(dirt)
print("2023 day 18 pt 1: %d" % np.sum(filled!=2))

# Part 2, far far bigger
# Recommended ways to find area of a polygon are shoelace and pick's theorems
# Shoelace: Sum up areas of a polygon in order 0.5 * (x1*y2 - x2*y1)
# Pick's theorem: (number of interior points) + (number of perimeter points)/2 - 1

coords = []
x = 0
y = 0
edge_lengths = []
for l in all_lines:
    coords.append([x, y])
    _, _, col = l.split(" ")

    digs = int(col.split("#")[-1][0:5], 16)
    hex_dir = int(col.split("#")[-1][5])
    if hex_dir == 0:
        d = "R"
        x = x + digs
    elif hex_dir == 1:
        d = "D"
        y = y + digs
    elif hex_dir == 2:
        d = "L"
        x = x - digs
    elif hex_dir == 3:
        d = "U"
        y = y - digs

    edge_lengths.append(digs)


# Shoelace theorem to calculate area of polygon
area = 0
for i in range(len(coords)-1):
    area += 0.5 * ((coords[i][0] * coords[i+1][1]) - (coords[i+1][0] * coords[i][1]))

# Perimeter is simply the sum of all edge lengths
perimeter = np.sum(np.array(edge_lengths))
picks_area = int(area - perimeter / 2 + 1)
dug_out_blocks = perimeter + picks_area

print("2023 day 18 pt 2: %d" % dug_out_blocks)
