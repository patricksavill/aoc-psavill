import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day6-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

def race_dist(total_time, hold_time, distance, debug=False):
    accel = 1
    velocity = hold_time * accel

    distance_gone = (total_time-hold_time) * velocity
    if debug:
        print("Held: %d\tVelocity: %d\tTravels: %d" % (hold_time, velocity, distance_gone))

    if distance_gone > distance:
        return True
    else:
        return False

def calculate_ways(time, distance):
    i = 0
    j = time
    while i < j:
        change = False
        if not race_dist(time, time - i, distance):
            i += 1
            change = True
        if not race_dist(time, time - j, distance):
            j -= 1
            change = True
        if change == False:
            break

    return j-i+1

times = [int(x) for x in all_lines[0].lstrip("Time:").split(" ") if x!=""]
distances = [int(x) for x in all_lines[1].lstrip("Distance:").split(" ") if x!=""]

ways=1
for i in range(len(times)):
    ways *= calculate_ways(times[i], distances[i])

print(ways)