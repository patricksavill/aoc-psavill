fish = []
with open("day6.txt") as file:
    all_lines = file.readlines()
    for item in all_lines[0].split(","):
        fish.append(int(item))

days = 80
# Life span of lantern fish: 8 on new, 6 on others
while days < 80: # Part 1 only
    new_fish = []
    for i in range(len(fish)):
        if fish[i] == 0:
            new_fish.append(8) # Fresh lantern added
            fish[i] = 6
        else:
            fish[i] -= 1
    fish.extend(new_fish)
    days += 1

print(len(fish))

# We can do this better though, use a count of the number of fish lives
life_numbers = [0] * 9
with open("day6.txt") as file:
    all_lines = file.readlines()
    for item in all_lines[0].split(","):
         life_numbers[int(item)] += 1

life_numbers = [z for z in range(9)]

days = 0
while days < 2:

    # All zero fish get new babies at the end

    print(life_numbers)
    zero_fishes = life_numbers[0]
    six_year_old = life_numbers[5]
    life_numbers[5] = life_numbers[6] + life_numbers[0]
    life_numbers[0] = life_numbers[1]
    life_numbers[1] = life_numbers[2]
    life_numbers[3] = life_numbers[4]
    life_numbers[4] = six_year_old

    life_numbers[6] = life_numbers[7]
    life_numbers[7] = life_numbers[8]
    life_numbers[8] = zero_fishes

    print(life_numbers)
    print(sum(life_numbers))
    days += 1

print(sum(life_numbers))