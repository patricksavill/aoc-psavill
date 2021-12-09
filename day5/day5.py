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

array = [[0 for i in range(max_dim + 1)] for j in range(max_dim + 1)]
print(len(array))

for i in range(len(point_index)):
    # Here we want to go through points. If horizontal, get the info
    # Then iterate over array and add them up
    if point_index[i].isNonDiagonal():
        indexes = point_index[i].getFlatPath()
        for i in range(int(len(indexes) / 2)):
            array[indexes[i * 2]][indexes[i * 2 + 1]] += 1

total = 0
for i in range(len(array[0])):
    for j in range(len(array[i])):
        if (array[i][j] > 1):
            total += 1

print("here we go for horizontal/vertical lines: " + str(total))

# Now do it for diagonals
for i in range(len(point_index)):
    if not point_index[i].isNonDiagonal():
        indexes = point_index[i].getDiagonalPath()
        for i in range(int(len(indexes) / 2)):
            array[indexes[i * 2]][indexes[i * 2 + 1]] += 1

total = 0
for i in range(len(array[0])):
    for j in range(len(array[i])):
        if (array[i][j] > 1):
            total += 1
print("here we go for diagonal lines: " + str(total))
