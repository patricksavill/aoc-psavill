# We're gonna need a helper class that is a bingo board
# it should store an array of numbers, then check if there is a bingo or not

import bingo as bingo
all_lines = []
bingo_boards = []

with open("day4.txt") as file:
    all_lines = file.readlines()

bingo_input = all_lines[0]
print(bingo_input)
input_count = 0
board_input = ""
for i in range(1, len(all_lines)):
    if all_lines[i] == "":
        continue
    else:
        board_input += all_lines[i].rstrip("\n") + " "
        input_count +=1

    if input_count == 6 :
        bingo_boards.append(bingo.Bingo())
        bingo_boards[-1].createBoard(board_input)
        input_count = 0
        board_input = ""

winning_board = -1
winning_number = -1
for number in bingo_input.split(","):
    if(winning_board != -1):
        break
    for i in range(len(bingo_boards)):
        bingo_boards[i].numberCheck(int(number))
        if (bingo_boards[i].checkBingo()):
            print("winner!!")
            winning_board = i
            winning_number = number
            break

# We want to know the final score, so after all numbers called?
if (winning_board ==-1):
    print("No one won")
else:
    print("Winning board: " + str(winning_board))
    print(bingo_boards[winning_board].board[:])
    print("Winning number: " + str(winning_number))
    print("Sum of board:" + str(bingo_boards[winning_board].sumUnmarked()))
    total = int(winning_number) * bingo_boards[winning_board].sumUnmarked()
    print(total)

# Go again but find the last board to win
for i in range(len(bingo_boards)):
    bingo_boards[i].resetMarkers()

boards_won = [0] * len(bingo_boards)
last_board = -1
last_number = -1
winning_total = -1
for number in bingo_input.split(","):
    for i in range(len(bingo_boards)):
        # we skip any board that's already won
        if boards_won[i] == 0:
            bingo_boards[i].numberCheck(int(number))
            if (bingo_boards[i].checkBingo()):
                print("winner!! " + str(i))
                boards_won[i] = 1 # Mark it as won
                last_board = i
                last_number = number
                winning_total = int(last_number) * bingo_boards[last_board].sumUnmarked()


print("Last board: " + str(last_board))
print(bingo_boards[last_board].board[:])
print("Last number: " + str(last_number))
print("Sum of board:" + str(bingo_boards[last_board].sumUnmarked()))
total = int(last_number) * bingo_boards[last_board].sumUnmarked()
print(total)
print(winning_total)