all_lines = []
with open("day8.txt") as file:
    all_lines = file.readlines()

count = 0
for x in all_lines:
    z = x.split("|")[-1]
    for i in z.split(" "):
        if i == "":
            continue
        i = i.rstrip("\n")
        if len(i) == 2 or len(i) == 3 or len(i) == 4 or len(i) == 7:
            count +=1

print(count)