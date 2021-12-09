
import points as Points

all_lines = []
point_index = []

with open("day5.txt") as file:
    all_lines = file.readlines()

# Line format is x,y -> x,y
max_dim = 0
for line in all_lines:
    pairs = line.split("->")
    point_index.append(Points.Points(pairs[0], pairs[1]))
    if (point_index[-1].getMax() > max_dim):
        max_dim = point_index[-1].getMax()

print(len(point_index))
print(max_dim)

array = [[0]*max_dim]*max_dim
print(len(array))

for i in len(point_index):
    # Here we want to go through points. If horizontal, get the info
    # Then iterate over array and add them up
    j = 1