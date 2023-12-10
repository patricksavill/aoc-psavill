import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day9-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

def all_values_zero(values):
    for v in values:
        if v != 0:
            return False
    return True
def predict_value(values, backwards=False):
    zero_found = False
    list_values = []
    list_values.append(values)
    while not zero_found:
        running_list = []
        for i in range(len(list_values[-1]) - 1):
            running_list.append(list_values[-1][i+1] - list_values[-1][i])

        list_values.append(running_list)
        if sum(running_list) == 0:
            zero_found = all_values_zero(running_list)

    if backwards:
        for i in range(len(list_values)):
            list_values[i].reverse()

    print(list_values)
    for j in range(len(list_values)-1, 0, -1):
        if j > 0:
            if backwards:
                new_value = list_values[j-1][-1] -list_values[j][-1]
            else:
                new_value = list_values[j - 1][-1] + list_values[j][-1]
            list_values[j-1].append(new_value)

    print(list_values)
    return list_values[0][-1]

history_sum = 0
for l in all_lines:
    v = [int(x) for x in l.split(" ") if x != '']
    p = predict_value(v)
    history_sum += p

print('2023 day 9 pt 1: %d' % history_sum)


history_sum = 0
for l in all_lines:
    v = [int(x) for x in l.split(" ") if x != '']
    p = predict_value(v, backwards=True)
    history_sum += p

print('2023 day 9 pt 2: %d' % history_sum)
