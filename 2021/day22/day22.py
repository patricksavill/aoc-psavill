import numpy as np

all_lines = []
with open("day22.txt") as file:
    all_lines = [line.rstrip("\n") for line in file.readlines()]

# Make a grid from -50 to +50, including a 0 position
grid = np.zeros((101,101,101))
lower_bound = -50
upper_bound = 50

x_start = 0
x_end = 0
y_start = 0
y_end = 0
z_start = 0
z_end = 0

for line in all_lines:
    set_val = 0
    if "on" in line:
        set_val = 1
    else:
        set_val = 0

    split_line = line.split(" ")[-1].split(",")
    x_start = int(split_line[0].split("=")[-1].split("..")[0])
    x_end = int(split_line[0].split("=")[-1].split("..")[1])
    y_start = int(split_line[1].split("=")[-1].split("..")[0])
    y_end = int(split_line[1].split("=")[-1].split("..")[1])
    z_start = int(split_line[2].split("=")[-1].split("..")[0])
    z_end = int(split_line[2].split("=")[-1].split("..")[1])

    # Check that ranges are in the region
    if lower_bound > x_end or lower_bound > y_end or lower_bound > z_end:
        continue
    if upper_bound < x_start or upper_bound < y_start or upper_bound < z_start:
        continue

    # Now iterate over grid
    for i in range(z_start,z_end+1):
        for j in range(y_start,y_end+1):
            for k in range(x_start,x_end+1):
                # Set values but offset with + upper bound to get the "-50" starting position
                grid[i+upper_bound,j+upper_bound,k+upper_bound] = set_val


# Sum it all up
print(sum(sum(sum(grid))))