import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day14-input.txt"
all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Dropping sand on column 500 we need to determine when the cave spills over
Drop straight down
If down is blocked, attempt down and to the left
If that's blocked, go down and to the right
If none, the sand is inert
"""

# Create the grid we're going to use
cave_rocks = []
x_bounds = [1e8, 0]
y_max = 0
for line in all_lines:
    cave_rocks.append(line.rstrip("\n"))
    # Determine min and max x and y
    for a in line.rstrip("\n").split("->"):
        b = a.split(",")
        x_bounds[0] = min(x_bounds[0], int(b[0]))
        x_bounds[1] = max(x_bounds[1], int(b[0]))

        # +1 as if y=10 we need y_max to be 11 (runs 0 -> 10)
        y_max = max(y_max, int(b[1]) + 1)

# We adjust x_bounds to be zero indexed
origin = 500 - x_bounds[0]
shift_x = origin - 500
x_bounds[0] = 0
x_bounds[1] = x_bounds[1] - 500 + origin + 1

# Create zeroed out cave grid
cave_grid = [[0] * x_bounds[1] for i in range(y_max)]

# Create the rocks in the grid
for c in cave_rocks:
    r_split = c.split("->")
    for i in range(len(r_split)-1):
        x1 = int(r_split[i].split(",")[0]) + shift_x
        x2 = int(r_split[i+1].split(",")[0])  + shift_x

        y1 = int(r_split[i].split(",")[1])
        y2 = int(r_split[i+1].split(",")[1])

        if y2 == y1:
            for x in range(abs(x1-x2)+1):
                cave_grid[y2][min(x1,x2) + x] = 1

        elif x2 == x1:
            for y in range(abs(y1-y2)+1):
                cave_grid[min(y2,y1)+ y][x1]=1

        else:
            print("unknown")

# Debug printing statement
# for c in cave_grid:
#     print(c)
#

def drop_sand(x, y):
    # Recursive function to keep dropping sand down
    # If x or y is out of bounds, we hit the abyss

    try:
        if cave_grid[y+1][x] == 0:
            return drop_sand(x, y+1)
        elif cave_grid[y+1][x-1] == 0:
            return drop_sand(x-1, y+1)
        elif cave_grid[y+1][x+1] == 0:
            return drop_sand(x+1, y+1)
        else:
            # Set the sand here
            cave_grid[y][x] = 1

        return False
    except IndexError:
        print("Hit the abyss!")
        return True


# Start ddropping sand in
sand_orig = (0, origin)
count = 0
while True:
    if not drop_sand(sand_orig[1], sand_orig[0]):
        count += 1
    else:
        break

print("Part one hit abyss in %d" % count)