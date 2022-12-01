INPUT = "day1-input.txt"

all_lines = []
with open(INPUT, 'r') as instream:
    all_lines = instream.readlines()

elf_totals = [0]
elf_index = 0
for line in all_lines:
    if line == "\n":
        elf_index += 1
        elf_totals.append(0)
    else:
        elf_totals[elf_index] += int(line.rstrip("\n"))

print(elf_totals)
print(max(elf_totals))  # answer 1

max_totals = 0
for i in range(3):
    max_totals += max(elf_totals)
    elf_totals.remove(max(elf_totals))

print(max_totals)  # answer 2
