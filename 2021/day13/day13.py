all_lines = []
with open("day13.txt") as file:
    all_lines = file.readlines()


def debug_print(array_to_print):
    for i in range(len(array_to_print)):
        print("")
        for j in range(len(array_to_print[i])):
            if paper[i][j] > 0:
                print("#", end='')
            else:
                print(".", end='')
    print("")


coords = []
instr = []
max_x = -1
max_y = -1
for line in all_lines:
    if ',' in line:
        coords.append([int(x) for x in line.rstrip('\n').split(',')])
        # And get dimensions for the array
        if max_x < coords[-1][0]:
            max_x = coords[-1][0]
        if max_y < coords[-1][1]:
            max_y = coords[-1][1]
    elif 'fold' in line:
        instr.append(line.rstrip('\n'))

print(coords)
print(instr)
print(max_x)
print(max_y)

paper = [[0] * (max_x + 1) for x in range(max_y + 1)]

for c in range(len(coords)):
    paper[coords[c][1]][coords[c][0]] = 1


# Do first fold
fold_number = 0
for fold in instr:
    fold_number += 1
    if 'y' in fold:
        # Fold over y
        print("folding y")
        y_index = int(fold.split('=')[-1])
        new_paper = []
        for i in range(y_index):
            new_paper.append([])
            for j in range(len(paper[0])):
                new_paper[i].append(paper[i][j] + paper[len(paper) - 1 - i][j])
        paper = new_paper


    elif 'x' in fold:
        # Fold over x
        print('folding x')
        x_index = int(fold.split('=')[-1])
        new_paper = []
        for i in range(len(paper)):
            new_paper.append([])
            for j in range(x_index):
                new_paper[i].append(paper[i][j] + paper[i][len(paper[0]) - 1 - j])
        paper = new_paper

    if fold_number == 1:
        sum_points = 0
        for i in range(len(paper)):
            for j in range(len(paper[0])):
                if (paper[i][j] > 0):
                    sum_points += 1
        print(sum_points)

debug_print(paper)
