all_lines = []
with open("day9.txt") as file:
    all_lines = file.readlines()

all_lines = [line.rstrip("\n") for line in all_lines]

# Low points are lower than top/bottom/left/right
low_points = []
for i in range(len(all_lines)):
    for j in range(len(all_lines[i])):
        low = int(all_lines[i][j])
        left = 999
        right = 999
        top = 999
        bottom = 999
        if j != 0:
            # Not on left edge, can assign left
            left = int(all_lines[i][j-1])
        if j != len(all_lines[i])-1:
            # Not on right edge, can assign right
            right = int(all_lines[i][j+1])
        if i != 0:
            # Not on top, can assign top
            top = int(all_lines[i-1][j])
        if i != len(all_lines)-1:
            # Not on bottom, can assign bottom
            bottom = int(all_lines[i+1][j])
        if (low < left and low < right and low< top and low <bottom):
            low_points.append(low)

print(low_points)
print("So total risk: " + str(sum(low_points) + len(low_points)))
