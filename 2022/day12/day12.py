import queue
import sys
from pathlib import Path
import math

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day12-input.txt"
all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:

Hill climbing, lowest cost route possible
Can only jump up by 1 unit value at a time
"""

grid = []
for line in all_lines:
    grid.append([])
    line = line.rstrip("\n")
    for c in line:
        grid[-1].append(c)

MAX_Y = len(grid)
MAX_X = len(grid[0])

# Note we iterate y first, then x, for visualisation purposes
# If we did x then y it'd look to us like it's been rotated by 90 degrees
start_pos = [0, 0]
end_pos = [0, 0]
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == "S":
            start_pos = [x, y]
            grid[y][x] = "a"
        elif grid[y][x] == "E":
            # We modify the value of the char here as ord(E) breaks our checks of 1 unit height
            grid[y][x] = "z"
            end_pos = [x, y]


# BFS approach
class Grid:
    def __init__(self, pos_x, pos_y, visits):
        # Running total of visits up to this node
        self.x = pos_x
        self.y = pos_y
        self.visited = visits


Q = queue.Queue()
Q.put(Grid(start_pos[0], start_pos[1], 0))
N = [(0, 1), (0, -1), (1, 0), (-1, 0)]
visited_set = set()

while not Q.empty():
    curr = Q.get()

    # Test for success
    if curr.x == end_pos[0] and curr.y == end_pos[1]:
        print("Finished in %d" % curr.visited)
        break

    for dx, dy in N:
        new_x = curr.x + dx
        new_y = curr.y + dy
        if 0 <= new_x < MAX_X and 0 <= new_y < MAX_Y:
            if ord(grid[new_y][new_x]) - ord(grid[curr.y][curr.x]) > 1:
                continue

            if (new_x, new_y) in visited_set:
                continue
            print("%s %d %d %d" % (grid[new_y][new_x], new_x, new_y, curr.visited + 1))
            new_grid = Grid(new_x, new_y, curr.visited + 1)
            visited_set.add((new_x, new_y))

            Q.put(new_grid)

