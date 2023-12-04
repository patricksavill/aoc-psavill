import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day2-input.txt"
all_lines = aoc_utils.file_reader(INPUT)

def parse_cubes_per_game(game_info):
    red_search = re.search('[0-9]+ (?=red)', game_info)
    green_search = re.search('[0-9]+ (?=green)', game_info)
    blue_search = re.search('[0-9]+ (?=blue)', game_info)

    red = 0
    green = 0
    blue = 0
    if red_search is not None:
        red = int(red_search.group())
    if green_search is not None:
        green = int(green_search.group())
    if blue_search is not None:
        blue = int(blue_search.group())

    return red, green, blue

def game_valid(line:str, r_num:int, g_num:int, b_num:int):
    game_number = re.search(r'(?<=Game )[0-9]+', line).group()

    games = line.split(":")[-1].split(";")
    for g in games:
        r,g,b = parse_cubes_per_game(g)
        if r > r_num or g > g_num or b > b_num:
            return int(game_number), False

    return int(game_number), True


sum = 0
for l in all_lines:
    g_num, valid = game_valid(l, 12, 13, 14)
    if valid:
        sum += g_num
    else:
        print(l)

print(sum)
