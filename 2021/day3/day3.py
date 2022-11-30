
all_lines = []
TOTAL_BITS = 12
with open("day3.txt") as file:
    all_lines = file.readlines()

def bitshift_and(position, number):
    # We COULD do binary bit shift, but the leading zero throws us off a bit
    # string comparison, whilst gnarly, is easier
    if (number[position]) == '1':
        return True
    return False

# Add or subtract one per bit position to get the most used places
counting_array = [0,0,0,0,0,0,0,0,0,0,0,0]

# 12 bit binary
for line in all_lines:
    for i in range(TOTAL_BITS):
        if bitshift_and(i, line):
            counting_array[i] +=1
        else:
            counting_array[i] -=1


gamma = 0
epsilon = 0
for i in range(TOTAL_BITS):
    if counting_array[i] > 0:
        gamma += pow(2, TOTAL_BITS-1-i)
    else:
        epsilon += pow(2, TOTAL_BITS-1-i)

print(bin(gamma))
print(bin(epsilon))
print("Final is: " + str(gamma*epsilon))
print(gamma | epsilon)
print (str(counting_array))

# Part 2
# Now we search through the list for oxygen, so most common bits each time
candidates = all_lines
bit_position = 0

while (len(candidates) != 1):
    count = 0
    usable_items = []
    for line in candidates:
        if bitshift_and(bit_position, line):
            count +=1
        else:
            count -=1
    for line in candidates:
        if count >= 0: # more 1's than zeros
            if bitshift_and(bit_position, line):
                usable_items.append(line)
        else:
            if not bitshift_and(bit_position, line):
                usable_items.append(line)
    candidates = usable_items
    if (bit_position < 11):
        bit_position += 1
    else:
        break

oxygen_report = candidates[0]
print(oxygen_report)

# Now we search through the list for c02 scrubber, so least common bits each time
candidates = all_lines
bit_position = 0

while (len(candidates) != 1):
    count = 0
    usable_items = []
    for line in candidates:
        if bitshift_and(bit_position, line):
            count +=1
        else:
            count -=1
    for line in candidates:
        if count >= 0: # more ones than zeros, keep the zeros
            if not bitshift_and(bit_position, line):
                usable_items.append(line)
        else:
            if bitshift_and(bit_position, line):
                usable_items.append(line)
    candidates = usable_items
    if (bit_position < 11):
        bit_position += 1
    else:
        break


carbon_report = candidates[0]
print(carbon_report)

print(int(oxygen_report,2)*int(carbon_report,2))