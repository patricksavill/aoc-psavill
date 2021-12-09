class Points:
    point1 = []
    point2 = []
    def __init__(self, coord1, coord2):
        self.point1 = []
        self.point2 = []
        self.point1.append(int(coord1.split(",")[0]))
        self.point1.append(int(coord1.split(",")[1]))
        self.point2.append(int(coord2.split(",")[0]))
        self.point2.append(int(coord2.split(",")[1]))

    def isNonDiagonal(self):
        if(self.point1[0] == self.point2[0] or self.point1[1] == self.point2[1]):
            return True
        else:
            return False

    def getMax(self):
        return max(self.point1[0], self.point1[1], self.point2[0], self.point2[1])

    def getFlatPath(self):
        xToY = []
        if (self.point1[0] == self.point2[0]):
            # Going to iterate over y
            startY = self.point2[1]
            xToY.append(self.point1[0])
            xToY.append(startY)
            while startY != self.point1[1]:
                if (self.point2[1] > self.point1[1]):
                    startY -=1
                else:
                    startY += 1
                xToY.append(self.point1[0])
                xToY.append(startY)
        else:
            # Going to iterate over x
            startX = self.point2[0]
            xToY.append(startX)
            xToY.append(self.point1[1])
            while startX != self.point1[0]:
                if (self.point2[0] > self.point1[0]):
                    startX -= 1
                else:
                    startX += 1
                xToY.append(startX)
                xToY.append(self.point1[1])


        return xToY