import queue
import sys
from pathlib import Path
import math

sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

INPUT = "day11-input.txt"
all_lines = aoc_utils.file_reader(INPUT)

"""
Part one:
Track how many times a monkey inspects an item, and find the two most active

Doing this with a list of Monkey class objects
"""

monkey_list = []

class Monkey:
    def __init__(self):
        self.items = queue.Queue()  # A monkey's items
        self.inspections = 0  # Number of items it has inspected

        self.modulo = 0 # This is the test we use to determine the next monkey
        self.test_true_index = 0  # Monkey index it'll pass to
        self.test_false_index = 0  # Monkey index it'll pass to

        self.worry_action = ""  # Can be +, *, or ^ (^ for square)
        self.worry_constant = 0  # The integer we use with the action

    @property
    def count(self):
        return self.inspections

    def add_item(self, item):
        self.items.put(item)

    def compute_worry(self, worry_input):
        # Here we parse the string that's in worry_action
        # There may be a more elegant way to store math functions in python
        if self.worry_action == "+":
            return worry_input + self.worry_constant
        elif self.worry_action == "*":
            return worry_input * self.worry_constant
        elif self.worry_action == "^":
            return math.pow(worry_input, self.worry_constant)

    def perform_inspection(self):
        while not self.items.empty():
            self.inspections += 1
            # Perform action on item worry level
            item_worry = self.compute_worry(self.items.get())

            # Divide by 3
            item_worry = int(item_worry/3.0)

            # Test it with test and pass along
            if item_worry % self.modulo == 0:
                monkey_list[self.test_true_index].add_item(item_worry)
            else:
                monkey_list[self.test_false_index].add_item(item_worry)

    def print(self):
        # Debugging only
        print(self.items.queue)
        print("Operation: %s " % self.worry_action + "%d" % self.worry_constant)
        print("Test: /%d" % self.modulo)
        print("True monkey: %d" % self.test_true_index + " - false: %d" % self.test_false_index)
        print("Inspections: %d" % self.count)

# Creating the monkeys we rely heavily upon knowing the format of the input
for line in all_lines:
    line = line.rstrip("\n")
    if "Monkey" in line:
        monkey_list.append(Monkey())
    elif "Starting" in line:
        items = line.split(":")[-1].split(",")
        for i in items:
            monkey_list[-1].add_item(int(i))
    elif "Operation" in line:
        if "old * old" in line:
            monkey_list[-1].worry_action = "^"
            monkey_list[-1].worry_constant = 2
            continue
        elif "*" in line:
            monkey_list[-1].worry_action = "*"
        elif "+" in line:
            monkey_list[-1].worry_action = "+"
        monkey_list[-1].worry_constant = int(line.split(" ")[-1])
    elif "Test:" in line:
        monkey_list[-1].modulo = int(line.split("by")[-1])
    elif "If true" in line:
        monkey_list[-1].test_true_index = int(line.split("monkey")[-1])
    elif "If false" in line:
        monkey_list[-1].test_false_index = int(line.split("monkey")[-1])


rounds = 0
while rounds < 20:
    for m in monkey_list:
        m.perform_inspection()
    rounds += 1

totals = []
for m in monkey_list:
    m.print()
    print("\n")
    totals.append(m.count)

print(totals)
maximums = sorted(totals, reverse=True)
print("Part one answer is: %d " % (maximums[0] * maximums[1]))
