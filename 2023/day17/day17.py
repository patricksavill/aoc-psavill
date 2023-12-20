import sys
from pathlib import Path
import re
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day17-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

from enum import Enum


class Direction(Enum):
    Up = 1
    Right = 2
    Down = 3
    Left = 4


# BFS approach
class Grid:
    def __init__(self, pos_x, pos_y, cost, dir, history=[]):
        # Running total of visits up to this node
        self.x = pos_x
        self.y = pos_y
        self.cost = cost
        self.direction = dir

        if len(history) == 0:
            self.history = [[pos_x, pos_y]]
        else:
            self.history = []
            self.history.extend(history)
            self.history.append([pos_x, pos_y])

    def parallel(self, new_dir):
        # Up = 1, Down = 3. So difference is two
        # Right = 2, Left = 4, so difference is still two
        return abs(self.direction.value - new_dir.value) == 2 or self.direction == new_dir

    def __lt__(self, other):
        return self.cost < other.cost


def test_parallel():
    g = Grid(0, 0, 0, Direction.Right)
    assert g.parallel(Direction.Left)
    g.direction = Direction.Left
    assert g.parallel(Direction.Right)
    g.direction = Direction.Up
    assert g.parallel(Direction.Down)
    g.direction = Direction.Down
    assert g.parallel(Direction.Up)


test_parallel()

char_arr = []
for l in all_lines:
    l = l.rstrip('\n')
    char_arr.append([int(x) for x in l])

grid = np.array(char_arr)

start_pos = [0, 0]
end_pos = [grid.shape[0] - 1, grid.shape[1] - 1]

import queue

import imageio

def move_crucible(min_moves, max_moves, part_two = False):

    Q = queue.PriorityQueue()
    Q.put(Grid(start_pos[0], start_pos[1], 0, Direction.Down))
    Q.put(Grid(start_pos[0], start_pos[1], 0, Direction.Right))

    N = [(0, 1, Direction.Down), (0, -1, Direction.Up),
         (1, 0, Direction.Right), (-1, 0, Direction.Left)]

    global_costs = np.zeros((grid.shape))
    visited_set = set()  # Global visiting set, preventing us going to visited locations

    while not Q.empty():
        curr = Q.get()

        # Test for success
        if curr.x == end_pos[0] and curr.y == end_pos[1]:
            print("Finished in %d" % curr.cost)
            debug_img = np.zeros((grid.shape))
            for i in range(len(curr.history)-1):
                # Write out joined segments of history
                debug_img[curr.history[i][0]:curr.history[i+1][0]+1, curr.history[i][1]:curr.history[i+1][1]+1] = 250
            imageio.v3.imwrite("last_curr-%d.png" % curr.cost, debug_img.astype(np.uint8))
            break

        if (curr.x, curr.y, curr.direction) in visited_set:
            continue

        # IMPORTANTLY we only add to the visited set when we pop off. I had a bug where we set visited prior to pop
        visited_set.add((curr.x, curr.y, curr.direction))


        for dx, dy, new_dir in N:
            new_cost = curr.cost

            # Here's the trick, we move up to max_moves  in one direction at a time
            # We THEN only move next time at right angles to the previous direction, since we moved up to the max last time
            for steps in range(1, max_moves +1):
                new_x = curr.x + dx * steps
                new_y = curr.y + dy * steps
                if 0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1]:
                    # Add to the running cost of the steps in this direction
                    new_cost += grid[new_x, new_y]
                    if steps < min_moves:
                        # Part two, HAVE to move at least four moves
                        continue

                    if curr.parallel(new_dir):
                        # Ensure we're moving at a right angle to the previous direction
                        continue

                    # Debug visuals only, store best code per node
                    if new_cost < global_costs[new_x, new_y] or global_costs[new_x, new_y] == 0:
                        global_costs[new_x, new_y] = new_cost

                    new_grid = Grid(new_x, new_y, new_cost, new_dir, curr.history)
                    Q.put(new_grid)


    if part_two:
        imageio.v3.imwrite("costs-part-two.png", (global_costs * 255/global_costs.max()).astype(np.uint8))
    else:
        imageio.v3.imwrite("costs-part-one.png", (global_costs * 255/global_costs.max()).astype(np.uint8))
    return curr.cost

print("2023 day 17 pt 1: %d" % move_crucible(1,3))
print("2023 day 17 pt 2: %d" % move_crucible(4,10, part_two=True))
