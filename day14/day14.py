import re
all_lines = []
with open("day14.txt") as file:
    all_lines = file.readlines()

all_lines = [line.rstrip("\n") for line in all_lines]
print(all_lines)

def join_polymer_pairs(pair_list):
    joined = ""
    for i in range(len(pair_list)):
        joined += pair_list[i][:-1]

    # Skipped last entry, so join it now
    joined += pair_list[-1][-1]
    return joined

def split_polymer_pairs(polymer_string):
    split_pairs = []
    for i in range(len(polymer_string) - 1):
        split_pairs.append(polymer_string[i] + polymer_string[i + 1])
    return split_pairs

starting_polymer = all_lines[0]
rules = [x for x in all_lines if "->" in x]
print(rules)

# Due to the pairwise searching we need a list of pairs
starting_polymer_pairs =[]
for i in range(len(starting_polymer)-1):
    starting_polymer_pairs.append(starting_polymer[i] + starting_polymer[i+1])

print(starting_polymer_pairs)

# 10 steps for part 1
# 40 steps for part 2 (gonna hurt I feel if we do it normally)
# The smart way would be to use an array to count the amount of times a unique pair exists, then increase that count
for step in range(10):
    # First step
    next_pairs = []
    for r in rules:
        search_pair = r.split("->")[0].strip(" ")
        # We make the sub in by splitting the pair, and adding the rules substitution character
        sub_in = search_pair[0] + r.split("->")[-1].strip(" ") + search_pair[1]

        # Need to use index from range. If we use "starting_polymer_pairs.index(pair)"
        # then we only find the first index
        for i in range(len(starting_polymer_pairs)):
            if re.search(search_pair, starting_polymer_pairs[i]):
                # Store the index (for later sort) and the new pair to add
                next_pairs.append([i, re.sub(search_pair, sub_in, starting_polymer_pairs[i])])

    subbed_polymer_pairs = []
    for p in sorted(next_pairs):
        subbed_polymer_pairs.append(p[-1])

    # Need to split into pairs again
    starting_polymer_pairs = split_polymer_pairs(join_polymer_pairs(subbed_polymer_pairs))

final_polymer = join_polymer_pairs(subbed_polymer_pairs)
set_items = list(set(final_polymer))
min = 9999999999
max = -1
min_char = ''
max_char = ''
for char in set_items:
    counted = final_polymer.count(char)
    if counted < min:
        min = counted
        min_char = char
    if counted > max:
        max = counted
        max_char = char
print("Char min: " + min_char + " count: " + str(min))
print("Char max: " + max_char + " count: " + str(max))
print("Difference: " + str(max - min))