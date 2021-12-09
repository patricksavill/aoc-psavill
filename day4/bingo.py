class Bingo():
    board = []
    marker = []
    bingo = False

    def __init__(self):
        self.data = []

    def createBoard(self, input):
        self.board = []
        temp = input.split(" ")
        for a in temp:
            if (a!= ""):
                self.board.append(int(a))
        if(len(self.board)!=25):
            print("Invalid board input, please try again")
            print(self.board)
            return
        else:
            self.marker = [0] * 25

    def numberCheck(self, num):
        if(num in self.board):
            self.marker[self.board.index(num)] = 1

    def checkBingo(self):
        # Check horizontals first)
        if (sum(self.marker[0:4]) == 5):
            return True
        if (sum(self.marker[5:9]) == 5):
            return True
        if (sum(self.marker[10:4]) == 5):
            return True
        if (sum(self.marker[15:19]) == 5):
            return True
        if (sum(self.marker[20:24]) == 5):
            return True
        # Check verticals
        for i in range(5):
            count = 0
            for j in range(5):
                count += self.marker[j*5 + i]
            if count == 5 :
                return True

        return False

    def sumUnmarked(self):
        total = 0
        for i in range(len(self.marker)):
            if self.marker[i] == 0:
                total += self.board[i]

        return total

    def resetMarkers(self):
        self.marker = [0] * 25