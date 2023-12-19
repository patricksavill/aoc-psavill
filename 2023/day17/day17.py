import sys
from pathlib import Path
import re
import numpy as np
sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day17-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))


# BFS approach
class Grid:
    def __init__(self, pos_x, pos_y, cost, g_x, g_y, history=[]):
        # Running total of visits up to this node
        self.x = pos_x
        self.y = pos_y
        self.goal_x = g_x
        self.goal_y = g_y
        self.cost = cost
        if len(history)== 0:
            self.history = [[pos_x, pos_y]]
        else:
            self.history = []
            self.history.extend(history)
            self.history.append([pos_x, pos_y])

    def moved_three_in_a_row(self, new_coord):
        if len(self.history) < 4:
            return False
        i = len(self.history)-4
        x1, y1 = self.history[i]
        x2, y2 = self.history[i+1]
        x3, y3 = self.history[i+2]
        x4, y4 = self.history[i + 3]

        # If x or y has been the same four times in order, we moved in order and cannot go
        # to the new coord if it matches. Note four times = 3 movements made
        if x1 == x2 == x3 == x4 == new_coord[0]:
            return True
        elif y1 == y2 == y3 == y4 == new_coord[1]:
            return True
        return False


    def __lt__(self, other):
        return self.cost < other.cost


char_arr = []
for l in all_lines:
    l = l.rstrip('\n')
    char_arr.append([int(x) for x in l])

grid = np.array(char_arr)

start_pos = [0,0]
end_pos = [grid.shape[0]-1, grid.shape[1]-1]

import queue
import imageio
Q = queue.PriorityQueue()
Q.put(Grid(start_pos[0], start_pos[1], grid[start_pos[0], start_pos[0]], end_pos[0], end_pos[1]))
N = [(0, 1), (0, -1), (1, 0), (-1, 0)]

global_costs = np.zeros((grid.shape))
visited_set = set() # Global visiting set, preventing us going to visited locations

while not Q.empty():
    curr = Q.get()
    print(Q.qsize())
    # Test for success
    if curr.x == end_pos[0] and curr.y == end_pos[1]:
        print("Finished in %d" % curr.cost)
        debug_img = np.zeros((grid.shape))
        for c in curr.history:
            debug_img[c[0], c[1]] = 250
        imageio.v3.imwrite("last_curr-%d.png" % curr.cost, debug_img.astype(np.uint8))
        # continue
        break

    # IMPORTANTLY we only add to the visited set when we pop off. I had a bug where we set visited prior to pop
    visited_set.add((curr.x, curr.y))

    for dx, dy in N:
        new_x = curr.x + dx
        new_y = curr.y + dy

        if 0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1]:
            if curr.moved_three_in_a_row([new_x, new_y]):
                continue
            if (new_x, new_y) in visited_set:
                continue
            new_cost = curr.cost + grid[new_x, new_y]

            # See if next node is better than current node
            best_cost = global_costs[new_x, new_y]
            if new_cost < best_cost or best_cost == 0:
                # We reach this node with a lower cost than previously achieved. Record it
                global_costs[new_x, new_y] = new_cost
            new_grid = Grid(new_x, new_y, new_cost, end_pos[0], end_pos[1], curr.history)
            Q.put(new_grid)



debug_img = np.zeros((grid.shape))
for c in curr.history:
    debug_img[c[0], c[1]] = 250
imageio.v3.imwrite("last_curr.png", debug_img.astype(np.uint8))

debug_img = np.zeros((grid.shape))
for c in visited_set:
    debug_img[c[0], c[1]] = 250
imageio.v3.imwrite("visited.png", debug_img.astype(np.uint8))

debug_img = np.zeros((grid.shape))

imageio.v3.imwrite("costs.png", global_costs.astype(np.uint8))


print("finished")