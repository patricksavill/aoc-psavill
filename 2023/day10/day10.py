import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day10-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))


def coord_shift_symbol(s):
    # Return format y, x
    if s == '|':
        # Return top and bottom shift coords
        return [[1, 0], [-1, 0]]
    elif s == '-':
        return [[0, 1], [0, -1]]
    elif s == 'L':
        # east, north
        return [[0, 1], [-1, 0]]
    elif s == 'J':
        # west, then north
        return [[0, -1], [-1, 0]]

    elif s == '7':
        # west, south
        return [[0, -1], [1, 0]]
    elif s == 'F':
        # east, south
        return [[0, 1], [1, 0]]
    elif s == '.':
        return []
    elif s == 'S':
        # Goal state
        return [[0, 0]]


def testing_pipes():
    with open('day10-test.txt') as handle:
        test_lines = handle.readlines()

    char_arr = []
    for l in test_lines:
        l = l.rstrip('\n')
        char_arr.append([str(x) for x in l])
    print(char_arr)

    test_coords = [[1, 2], [1, 1], [1, 3], [3, 3], [3, 1], [2, 3]]
    for t in test_coords:
        c = char_arr[t[0]][t[1]]
        shifts = coord_shift_symbol(c)
        debug_str = ''
        debug_str += '%s ' % c
        for s in shifts:
            cs = char_arr[t[0] + s[0]][t[1] + s[1]]
            debug_str += '%s ' % cs
        print(debug_str)


def find_start_pos(c_arr):
    for y in range(len(c_arr)):
        for x in range(len(c_arr[y])):
            if c_arr[y][x] == 'S':
                return y, x


def neighbour_coords():
    c = []
    for y in range(-1, 2):
        for x in range(-1, 2):
            if y == 0 and x == 0:
                continue
            c.append([y, x])
    return c


def starting_pipes(c_arr, y, x):
    candidates = []
    for n in neighbour_coords():
        if 0 <= y + n[0] <= len(c_arr) and \
                0 <= x + n[1] <= len(c_arr[y]):

            neighbour_symbol = c_arr[y + n[0]][x + n[1]]
            shifts = coord_shift_symbol(neighbour_symbol)
            # Determine if this symbol points back to start pos

            for s in shifts:
                if (n[0] + s[0]) == 0 and (n[1] + s[1]) == 0:
                    candidates.append([y + n[0], x + n[1]])

    return candidates


def return_next_coord(c_arr, y, x, a, b):
    # y,x are source, a,b are neighbour
    working_sym = c_arr[a][b]
    shifts = coord_shift_symbol(c_arr[a][b])
    for s in shifts:
        if (a + s[0]) == y and (b + s[1]) == x:
            # Back to the starting symbol, continue
            continue
        else:
            # print(c_arr[a + s[0]][b + s[1]], [a + s[0], b + s[1]])
            return c_arr[a + s[0]][b + s[1]], a + s[0], b + s[1]


def testing_traversal(input_file):
    with open(input_file) as handle:
        test_lines = handle.readlines()

    char_arr = []
    for l in test_lines:
        l = l.rstrip('\n')
        char_arr.append([str(x) for x in l])
    print(char_arr)

    start_loc = find_start_pos(char_arr)
    print(char_arr[start_loc[0]][start_loc[1]])

    working_pipes = starting_pipes(char_arr, start_loc[0], start_loc[1])
    print(working_pipes)

    working_pipes.remove(working_pipes[0])
    start_y = start_loc[0]
    start_x = start_loc[1]
    steps = 1
    while True:
        w = working_pipes[0]
        working_pipes.remove(w)
        s, y1, x1 = return_next_coord(char_arr, start_y, start_x, w[0], w[1])
        # Need to handle the starting position PER PIPE as there are two running round
        start_y = w[0]
        start_x = w[1]
        if s == 'S':
            steps+=1
            print(steps)
            print(steps/2)
            return steps/2

        working_pipes.append([y1, x1])
        steps += 1


testing_traversal('day10-test.txt')

half_steps = testing_traversal('day10-input.txt')
print('2023 half loop length part 1:', half_steps)

# Part 2
# Counting number of squares within the pipes

def shoelace_approach(input_file):
    with open(input_file) as handle:
        test_lines = handle.readlines()

    char_arr = []
    for l in test_lines:
        l = l.rstrip('\n')
        char_arr.append([str(x) for x in l])

    start_loc = find_start_pos(char_arr)

    working_pipes = starting_pipes(char_arr, start_loc[0], start_loc[1])

    # Only use one pipe
    working_pipes.remove(working_pipes[0])
    start_y = start_loc[0]
    start_x = start_loc[1]

    coords = []
    coords.append([start_x, start_y])
    coords.append([working_pipes[0][1], working_pipes[0][0]])

    while True:
        w = working_pipes[0]
        working_pipes.remove(w)
        s, y1, x1 = return_next_coord(char_arr, start_y, start_x, w[0], w[1])

        # Need to handle the starting position PER PIPE as there are two running round
        start_y = w[0]
        start_x = w[1]

        coords.append([x1, y1])

        if s == 'S':
            break
        working_pipes.append([y1, x1])

    area = 0
    perimeter = 0
    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i+1]
        area += 0.5 * ((x1 * y2) - (x2 * y1))
        perimeter += abs((x1 - x2) + (y1 - y2))

    # Have to account for the start, so wrap around
    perimeter += abs((coords[-1][0] - coords[0][0]) + (coords[-1][1] - coords[0][1]))

    area = abs(area)

    picks_area = int(area - (perimeter/2) + 1)
    return picks_area

picks_area = shoelace_approach('day10-input.txt')
print("2023 day 10 pt 2: %d" % picks_area)
