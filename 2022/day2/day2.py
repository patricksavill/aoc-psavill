import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day2-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one: 
According to the strategy guide:
Y = Paper
X = Rock
Z = Scissors

And inputs are
A = Rock
B = Paper
C = Scissors
"""


def shape_score(shape):
    # Scissors are 3, Paper is 2, and Rock is 1
    if shape == "Z":
        return 3
    if shape == "Y":
        return 2
    if shape == "X":
        return 1


def is_draw(opp_hand, my_hand):
    if opp_hand == "A" and my_hand == "X" or \
            opp_hand == "B" and my_hand == "Y" or \
            opp_hand == "C" and my_hand == "Z":
        return True
    return False


def is_win(opp_hand, my_hand):
    if opp_hand == "A":
        # To win against rock we must have paper
        if my_hand == "Y":
            return True
        else:
            return False
    if opp_hand == "B":
        # Against paper, we must have scissors
        if my_hand == "Z":
            return True
        else:
            return False
    if opp_hand == "C":
        # And against scissors we must have rock
        if my_hand == "X":
            return True
        else:
            return False


def calculate_score(opp_hand, my_hand):
    # Compute the outcome, and thus score, from the given data
    # hand score is for the shape chosen. outcome_score is for win/loss/draw

    outcome_score = 0
    hand_score = shape_score(my_hand)

    # Check for draw case
    if is_draw(opp_hand, my_hand):
        outcome_score = 3
    # Check for win case
    elif is_win(opp_hand, my_hand):
        outcome_score = 6

    return outcome_score + hand_score


total_score = 0
for line in all_lines:
    inputs = line.rstrip("\n").split(" ")
    total_score += calculate_score(inputs[0], inputs[1])

print("Final score is: %d" % total_score)
