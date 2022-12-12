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

# Note we iterate y first, then x, for visualisation purposes
# If we did x then y it'd look to us like it's been rotated by 90 degrees
start_pos = [0, 0]
end_pos = [0, 0]
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == "S":
            start_pos = [x, y]
        elif grid[y][x] == "E":
            # We modify the value of the char here as ord(E) breaks our checks of 1 unit height
            grid[y][x] = chr(ord("z") + 1)
            end_pos = [x, y]


class GridNode:
    def __init__(self, posX, posY, char, parent):
        self.x = posX
        self.y = posY
        self.c = char
        self.parent = parent
        self.visited = 0  # Running count of how many node visited before this
        self.goal_dist = 0
        self.start_dist = 0
        self.cost = 0

    # Functions to be used when sorting nodes:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.cost < other.cost

    def backtrace(self):
        print("Char: %s - Visited cost: %d " % (self.c, self.visited))
        if self.parent is not None:
            self.parent.backtrace()


start_node = GridNode(start_pos[0], start_pos[1], "a", None)
end_node = GridNode(end_pos[0], end_pos[1], "z", None)

to_process = [start_node]  # Initiliase with starting node
finished = []
neighs = [[0, 1], [0, -1], [1, 0], [-1, 0]]  # Neighbour vectors

while len(to_process) > 0:
    to_process.sort()
    curr = to_process.pop(0)

    finished.append(curr)

    if curr == end_node:
        curr.backtrace()
        print("Reached the goal")
        print("Total visited was: %d" % curr.visited)
        break

    x = curr.x
    y = curr.y
    for n in neighs:
        xc = x + n[0]
        yc = y + n[1]
        if 0 <= xc < len(grid[0]) and 0 <= yc < len(grid):
            # Check if neighbour is within the max height diff of 1
            if ord(grid[yc][xc]) > ord(curr.c) and ord(grid[yc][xc]) - ord(curr.c) > 1:
                continue

            # We can jump to the neighbour, make the node
            neigh_node = GridNode(xc, yc, grid[yc][xc], curr)
            if neigh_node in finished:
                continue

            # Set heuristic costs of the node
            neigh_node.start_dist = abs(xc - start_node.x) + abs(yc - start_node.y)
            neigh_node.goal_dist = abs(xc - end_node.x) + abs(yc - end_node.y)
            neigh_node.visited = curr.visited + 1
            neigh_node.cost = neigh_node.start_dist + neigh_node.goal_dist - neigh_node.visited 

            # Now check if we want to add the node to be processed
            if len(to_process) == 0:
                to_process.append(neigh_node)
            else:
                for i in range(len(to_process)):
                    if to_process[i].x != neigh_node.x and to_process[i].y != neigh_node.y \
                            and to_process[i].cost >= neigh_node.cost:
                        to_process.append(neigh_node)
                        break
