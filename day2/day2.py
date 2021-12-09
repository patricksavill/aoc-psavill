
all_lines = []
with open("day2.txt") as file:
    all_lines = file.readlines()

x = 0
y = 0

for line in all_lines:
    line = line.rstrip("\n")
    val = int(line.split(" ")[-1])
    if "forward" in line:
        x += val
    elif "up" in line:
        y -= val
    elif "down" in line:
        y += val

print(x)
print(y)

x = 0
y = 0
aim = 0
for line in all_lines:
    line = line.rstrip("\n")
    val = int(line.split(" ")[-1])

    if "up" in line:
        aim -= val
    elif "down" in line:
        aim += val
    elif "forward" in line:
        x += val
        y += (aim * val)

print(x)
print("s")
print(y)