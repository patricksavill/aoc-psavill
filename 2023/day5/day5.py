import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day5-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

def make_dict_map(lines):
    # This is a naive approach, and the dictionary size may be waaay too large

    d = {}
    for l in lines:
        if l == "":
            continue

        # 0: destination range start, 1: source range start, 2: range length
        dr_start, sr_start, r =[int(x) for x in l.split(" ")]
        for index in range(sr_start, sr_start+r):
            d[index] = dr_start + index - sr_start

def in_map_range(num, map_list):
    if map_list[0] <= num <= map_list[1]:
        return True
    else:
        return False

def map_number(num, map_list):
    diff = num - map_list[0]
    return map_list[2] + diff

def map_list_to_next(input_list, mapping_lines, debug=False, flip_order=False):
    # Directly map the input list values to the next map

    output_list = []

    map_list = []
    for l in mapping_lines:
        if l == "":
            continue


        dr_start, sr_start, r = [int(x) for x in l.split(" ")]
        if flip_order:
            sr_start, dr_start, r = [int(x) for x in l.split(" ")]

        # We make the map [source_start, source_end, destination_start, destination_end] inclusively
        map_list.append([sr_start, sr_start+r-1, dr_start, dr_start+r-1])
    if debug:
        print(map_list)
    for a in input_list:
        found_map = False
        for m in map_list:
            if in_map_range(a, m):
                found_map = True
                if debug:
                    print("TODO mapping")
                    print(map_number(a, m))
                output_list.append(map_number(a,m))

        if not found_map:
            # Append number directly
            if debug:
                print("Mapping directly")
            output_list.append(a)

    return output_list

seeds = []
i = 0
while i < len(all_lines):
    if "seeds:" in all_lines[i]:
        seeds = [int(x) for x in all_lines[i].lstrip("seeds:").split(" ") if x!=""]
        print(seeds)
        i+=1
    elif "map" in all_lines[i]:
        i+=1
        map_lines = []
        while 'map' not in all_lines[i]:
            map_lines.append(all_lines[i])
            i+=1
            if i >= len(all_lines):
                break

        seeds = map_list_to_next(seeds, map_lines)
        print("\t\t", seeds)
    else:
        i+=1

import numpy as np
print(np.array(seeds).min())

# Part 2, map from location back to seed iteratively until we find a valid one

def search_location(loc):
    seeds = [loc]
    i = len(all_lines) -1
    while i> 0:
        map_lines = []
        while 'map' not in all_lines[i]:
            map_lines.append(all_lines[i])
            i-=1
            if i <0:
                break
        if 'map' in all_lines[i]:
            seeds = map_list_to_next(seeds, map_lines, flip_order=True)
            # print("\t\t", seeds)
            i-=1
        else:
            i-=1
    return seeds

def seed_in_range(seeds, target):
    i = 0
    while i<len(seeds):
        if seeds[i] <= target <= (seeds[i]+seeds[i+1]):
            return True
        i+=2
    return False

valid_seed_ranges = []
seeds = [int(x) for x in all_lines[0].lstrip("seeds:").split(" ") if x!=""]
print(seeds)

loc_jump = 1e6
last_true_loc = 0
loc = last_true_loc
while True:
    start_seed = search_location(loc)
    # print(start_seed)
    # print(seed_in_range(seeds, start_seed[0]))
    if seed_in_range(seeds, start_seed[0]):
        last_true_loc = loc - loc_jump
        print(loc)
        loc_jump = loc_jump//10
        if loc_jump < 1:
            break
        loc = last_true_loc
    else:
        loc += loc_jump

print(loc)
