all_lines = []
with open("day10.txt") as file:
    all_lines = [line.rstrip("\n") for line in file.readlines()]


open_characters =["(", "[", "{", "<"]
close_characters = [")", "]", "}", ">"]
costs = [3, 57, 1197, 25137]

# We append the matching closing character to this array
# When we encounter a closing character we check if it's matched
# with the last entry of the expected array
# If it is:
# - Remove this entry
# If it isn't
# - Corrupted line found
saved = []
expected = []
corruptions = []
for line in all_lines:
    expected = []
    for i in range(len(line)):
        if line[i] in open_characters:
            expected.append(close_characters[open_characters.index(line[i])])
        elif line[i] == expected[-1]:
            expected.pop(-1)
        else:
            saved.append(expected)
            corruptions.append(line[i])
            break

print(corruptions)

error_cost = 0
for c in corruptions:
    error_cost += costs[close_characters.index(c)]
print(error_cost)

# For part 2 we need to store a reversed list of "expected"
# Then apply the costing algorithm
# Then find the middle value and return that cost
print(saved)