all_lines = []
with open("day7.txt") as file:
    all_lines = file.readlines()

# Make an array of crabs, with a "1" in each location to show a crab is there
crab_locations = [int(c) for c in all_lines[0].split(',')]
max_dim = max(crab_locations)

crabs = [0] * (max_dim + 1)
for i in crab_locations:
    crabs[i] += 1

cost_per_position = [0] * len(crabs)

for i in range(len(cost_per_position)):
    # Sum all crabs locations to this position
    costs = 0
    for j in range(len(crabs)):
        if crabs[j] == 0:
            # No crab at this location, move along
            continue
        elif j > i:
            # We're shifting left, remember to multiply by number of crabs
            costs += (j - i) * crabs[j]
            # print("crab:" + str(j) + " costs:" + str(j - i))
        else:
            costs += (i - j) * crabs[j]
            # print("crab:" + str(j) + " costs:" + str(i - j))

    cost_per_position[i] = costs

print(cost_per_position)
print("Minimum is: " + str(min(cost_per_position)))
print("Which is at: " + str(cost_per_position.index(min(cost_per_position))))

# Now do it again, but use the pyramid problem math of (n+1)*n/2 for cost

for i in range(len(cost_per_position)):
    # Sum all crabs locations to this position
    costs = 0
    for j in range(len(crabs)):
        if crabs[j] == 0:
            # No crab at this location, move along
            continue
        elif j > i:
            # We're shifting left, remember to multiply by number of crabs
            temp_cost = (j-i)
            costs += (temp_cost+1) * temp_cost/2 * crabs[j]
            # print("crab:" + str(j) + " costs:" + str(j - i))
        else:
            temp_cost = (i - j)
            costs += (temp_cost+1) * temp_cost/2 * crabs[j]
            # print("crab:" + str(j) + " costs:" + str(i - j))

    cost_per_position[i] = costs

print("Minimum with weight costs is: " + str(min(cost_per_position)))
print("Which is at: " + str(cost_per_position.index(min(cost_per_position))))

