all_lines = []
with open("day11.txt") as file:
    all_lines = file.readlines()

all_lines = [line.rstrip("\n") for line in all_lines]
# octo_array = [[0]*len(all_lines[0])] * len(all_lines)
octo_array = []
has_flashed = []

for i in range(len(all_lines)):
    octo_array.append([])
    has_flashed.append([])
    for j in range(len(all_lines[i])):
        octo_array[i].append(int(all_lines[i][j]))
        has_flashed[i].append(0)

# From a given point add 1 to all neighbours (up to 8)
def flash_neighbours(x,y):
    # Static grid of the eight neighbours of the point [0,0]
    grid = [[-1,-1],[0, -1],[1, -1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    for k in range(len(grid)):
        grid[k][0] += x
        grid[k][1] += y
    # We now have a grid, iterate over it and apply to octo

    for k in range(len(grid)):
        # Check we're not out of bounds for x
        if grid[k][0] >=0 and grid[k][0] < len(octo_array[0]):
            if grid[k][1] >=0 and grid[k][1] < len(octo_array):
                octo_array[grid[k][0]][grid[k][1]] += 1

### LOOP begins
total_flashes = 0
total_loops = 1000 # MAKE THIS 100 for part 1 execution
all_flash_step = -1
while total_loops > 0:
    total_loops -= 1
    # add 1 to everything to start
    for i in range(len(octo_array)):
        for j in range(len(octo_array[i])):
            octo_array[i][j] += 1


    # If over nine we flash, and we keep going until no more flashes have occured
    flashed = True
    while (flashed):
        flashed = False
        for i in range(len(octo_array)):
            for j in range(len(octo_array[i])):
                if octo_array[i][j] > 9 and has_flashed[i][j] == 0:
                    # If it's over nine and hasn't yet flashed, flash it
                    flash_neighbours(i,j)
                    flashed = True
                    has_flashed[i][j] = 1 # Mark this for later
                    total_flashes += 1


    flashes_per_step = 0
    for i in range(len(octo_array)):
        for j in range(len(octo_array[i])):
            if has_flashed[i][j] == 1:
                octo_array[i][j] = 0 # We set it to zero, all energy went into flash
                has_flashed[i][j] = 0
                flashes_per_step +=1

    # Record the first time they all flash together
    if flashes_per_step == len(has_flashed) * len(has_flashed[0]) and all_flash_step == -1:
        all_flash_step = 1000 - total_loops


print(total_flashes)
print(octo_array)

print(all_flash_step)
