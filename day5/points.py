class Points:
    point1 = [0,0]
    point2 = [-1,-1]
    def __init__(self, coord1, coord2):
        self.point1[0] = int(coord1.split(",")[0])
        self.point1[1] = int(coord1.split(",")[1])
        self.point2[0] = int(coord2.split(",")[0])
        self.point2[1] = int(coord2.split(",")[1])

    def isNonDiagonal(self):
        if(self.point1[0] == self.point2[0] or self.point1[1] == self.point2[1]):
            return True
        else:
            return False

    def getMax(self):
        return max(self.point1[0], self.point1[1], self.point2[0], self.point2[1])