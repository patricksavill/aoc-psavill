import sys
from pathlib import Path
import queue

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day5-input.txt"

all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
We're moving things around one at a time
Do it with lists, append to the end, then read from the end
FIFO

We also have some string parsing to do:
The organisation of items uses [] and spaces to delineate stacks
Then the stacks are numbered

After that we have three numbers
move X from Y to Z
X is the number to move
Y is the stack to move from
Z is the stack to move to
"""


def construct_stacks(input):
    """
    Parses the stack input and returns a list of queues

    :param input: unfiltered first stack content from the AoC input
                  This is going to be a list of strings
    :return: list of queues, LIFO specifically
    """
    raw_list = []
    for line in input:
        print(line)
        index = 1
        list_index = 0
        while index < len(line):
            # We can be a little sneaky here due to the formatting
            # We know the letter of a crate has 3 chars between
            # So we skip along by 4 each time
            if not "[" in line:
                # We've hit the end of the letter/cargo definitions, so break
                break
            if line[index] != " ":
                while len(raw_list) < (list_index + 1):
                    # Ensure the stack_list has enough lists to append on
                    raw_list.append([])
                raw_list[list_index].append(line[index])
            index += 4
            list_index += 1

    # Now as we've got the top of each stack at the bottom we need to flip it
    stack_list = []
    stack_index = 0
    for stack in raw_list:
        stack_list.append(queue.LifoQueue())
        for i in reversed(range(len(stack))):
            stack_list[stack_index].put(stack[i])
        stack_index += 1

    return stack_list


def construct_moves(input):
    """
    Here we parse the movement strings into a list of three items per list

    :param input: unfiltered movements commands from the AoC input
    :return: List of lists, each sub-list has three ints in it
    """
    moves = []
    for line in input:
        commands = line.split(" ")
        # Note we decrement the stack number by 1 as we're zero indexed
        moves.append([int(commands[1]), int(commands[3])-1, int(commands[5])-1])
    return moves


# Read input, split on the newline
stack_input = []
movement_cmds = []
end_of_stack = False
for line in all_lines:
    if line == "\n":
        end_of_stack = True
        continue

    if end_of_stack:
        movement_cmds.append(line)
    else:
        stack_input.append(line)

# Construct stacks and movement actions
stacks = construct_stacks(stack_input)
moves = construct_moves(movement_cmds)

# Apply movements
for action in moves:
    shifts_done = 0
    while shifts_done < action[0]:
        stacks[action[2]].put(stacks[action[1]].get())
        shifts_done += 1

# Print the top of each stack as a combined string
part_one_answer =""
for q in stacks:
    part_one_answer += q.get()
print("Part one is: %s" % part_one_answer)

"""
Part two:
The same as before BUT crates are moved as a group
So we're not flipping the orders, but moving in chunks

That's fine, just use an intermediary LIFO queue
"""

# Reconstruct the stacks
stacks = construct_stacks(stack_input)
moves = construct_moves(movement_cmds)

# Apply movements
temp_queue = queue.LifoQueue()
for action in moves:
    shifts_done = 0
    while shifts_done < action[0]:
        temp_queue.put(stacks[action[1]].get())
        shifts_done += 1

    while shifts_done > 0:
        stacks[action[2]].put(temp_queue.get())
        shifts_done -= 1

part_two_answer =""
for q in stacks:
    part_two_answer += q.get()
print("Part two is: %s" % part_two_answer)
