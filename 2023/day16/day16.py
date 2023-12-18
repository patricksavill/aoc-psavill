import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day16-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

# Want to track
# - History of beam
# - Direction beam is currently heading in

# When we hit a splitter, we add a new beam to the stack
# If a beam hits TWO consecutive points it has seen before, kill that beam.
# (Reason is two points make a line, so we must be heading in the same direction as before)

# Store a grid that holds state of energized or not, and update only if not energised

from enum import Enum


class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Beam():
    history = []
    direction = None

    def __init__(self, dir):
        self.direction = dir
        self.history = []

    def move(self):
        x, y = self.history[-1]
        if self.direction == Direction.Up:
            y = y - 1
        elif self.direction == Direction.Right:
            x = x + 1
        elif self.direction == Direction.Down:
            y = y + 1
        elif self.direction == Direction.Left:
            x = x - 1

        self.history.append([x, y])
        return x, y

    def set_direction(self, dir):
        self.direction = dir

    def visited(self, x, y):
        for h in self.history:
            if h[0] == x and h[1] == y:
                return True
        return False

    def visited_line(self, x, y):
        # Returns true if this beam has visited this spot AND the next
        # Assumed to be a repeated pattern, going in the same line if next index
        # has been visited in order
        for i in range(len(self.history)):
            if self.history[i][0] == x and self.history[i][1] == y:

                if i == (len(self.history) - 1):
                    # No more steps, end of list
                    return False

                if self.direction == Direction.Up:
                    y = y - 1
                elif self.direction == Direction.Right:
                    x = x + 1
                elif self.direction == Direction.Down:
                    y = y + 1
                elif self.direction == Direction.Left:
                    x = x - 1

                if self.history[i + 1][0] == x and self.history[i + 1][1] == y:
                    return True

        return False

    def set_history(self, src_history):
        # Copy
        for h in src_history:
            self.history.append(h)


char_arr = []
for l in all_lines:
    l = l.rstrip('\n')
    char_arr.append([str(x) for x in l])

max_x = len(char_arr[0])
max_y = len(char_arr)
import numpy as np
import imageio


def beam_traversal(start_x, start_y, direction, debug_vis=False):
    visited = np.zeros((len(char_arr), len(char_arr[0])))

    beam = Beam(direction)
    beam.set_history([[start_x, start_y]])
    beams = [beam]

    exited_edges = []

    if debug_vis:
        gifwriter = imageio.get_writer('movie.gif', mode='I', fps=30)
    while len(beams) > 0:
        if debug_vis:
            gifwriter.append_data(visited.astype(np.uint8) * 250)
        for b in beams:

            x, y = b.move()
            # Ensure we're not out of bounds
            if x >= max_x or 0 > x or y >= max_y or 0 > y:
                exited_edges.append([x, y])
                beams.remove(b)
                continue

            # Deal with bouncing mirrors
            if char_arr[y][x] == "\\" and b.direction == Direction.Right:
                b.set_direction(Direction.Down)
            elif char_arr[y][x] == "\\" and b.direction == Direction.Left:
                b.set_direction(Direction.Up)
            elif char_arr[y][x] == "\\" and b.direction == Direction.Down:
                b.set_direction(Direction.Right)
            elif char_arr[y][x] == "\\" and b.direction == Direction.Up:
                b.set_direction(Direction.Left)
            elif char_arr[y][x] == "/" and b.direction == Direction.Right:
                b.set_direction(Direction.Up)
            elif char_arr[y][x] == "/" and b.direction == Direction.Left:
                b.set_direction(Direction.Down)
            elif char_arr[y][x] == "/" and b.direction == Direction.Down:
                b.set_direction(Direction.Left)
            elif char_arr[y][x] == "/" and b.direction == Direction.Up:
                b.set_direction(Direction.Right)

            # Deal with splitters
            elif char_arr[y][x] == "-" and (b.direction == Direction.Down or \
                                            b.direction == Direction.Up):
                # Firstly, make the source beam turn right
                b.set_direction(Direction.Right)

                # We've been down this path before, remove and continue
                if b.visited_line(x, y) or visited[y, x] == 1:
                    beams.remove(b)
                    continue

                # Secondly, make a new beam going left
                beams.append(Beam(Direction.Left))
                # Now, append THE WHOLE first beam's history to the second
                beams[-1].set_history(b.history)

            elif char_arr[y][x] == "|" and (b.direction == Direction.Right or \
                                            b.direction == Direction.Left):
                # Firstly, make the source beam turn Down
                b.set_direction(Direction.Down)

                # We've been down this path before, remove and continue
                if b.visited_line(x, y) or visited[y, x] == 1:
                    beams.remove(b)
                    continue

                # Secondly, make a new beam going Up
                beams.append(Beam(Direction.Up))
                # Now, append THE WHOLE first beam's history to the second
                beams[-1].set_history(b.history)

            visited[y, x] = 1

            # Cull all beams that are about to repeat moves
            if b.visited_line(x, y):
                beams.remove(b)
                continue
    if debug_vis:
        gifwriter.close()

    return np.sum(visited != 0), exited_edges


# Start top left, just off the grid, heading right
part_one_energised, _ = beam_traversal(-1, 0, Direction.Right)
print("2023 day 16 pt 1: %d " % part_one_energised)

# Part 2. Call from every outer part of the grid we haven't exited through yet

# Work around the edges of the grid
energised_list = []
exited_tiles = set() # Store exited coordinates and skip over these


def start_on_edge(edge_x, edge_y, direction, exited_list):
    for start in exited_list:
        if start[0] == edge_x and start[1] == edge_y:
            # Already visited, skip
            return 0, []
    print("Started on %d %d" % (edge_x, edge_y))
    return beam_traversal(edge_x, edge_y, direction)


for y in range(max_y):
    energised, exited = start_on_edge(-1, y, Direction.Right, exited_tiles)
    if exited != []:
        for e in exited:
            exited_tiles.add((e[0], e[1]))
        energised_list.append(energised)

    energised, exited = start_on_edge(max_x, y, Direction.Left, exited_tiles)
    if exited != []:
        for e in exited:
            exited_tiles.add((e[0], e[1]))
        energised_list.append(energised)

for x in range(max_x):
    energised, exited = start_on_edge(x, -1, Direction.Down, exited_tiles)
    if exited != []:
        for e in exited:
            exited_tiles.add((e[0], e[1]))
        energised_list.append(energised)

    energised, exited = start_on_edge(x, max_y, Direction.Up, exited_tiles)
    if exited != []:
        for e in exited:
            exited_tiles.add((e[0], e[1]))
        energised_list.append(energised)

print("2023 day 16 pt 2: %d" % np.array(energised_list).max())
