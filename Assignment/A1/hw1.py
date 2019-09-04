#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import permutations

# Cell Definition
#   - cellType: monster/mirror
#   - value for monster: 0 for none, 1 for Ghost, 2 for Vampire, 3 for Zombie
#   - value for mirror: 0 for \, 1 for /
#   - fixed: indicating whether this cell is known for sure. Should always be `True` for mirrors


class Cell:
    def __init__(self, cellType, value, fixed):
        self.cellType = cellType
        self.value = value
        self.fixed = fixed


# Define switch for monster & mirror for convenience
def monster(i):
    switcher = {
        0: '*',
        1: 'G',
        2: 'V',
        3: 'Z'
    }
    return switcher.get(i, "Invalid monster type!")


def mirror(i):
    switcher = {
        0: '\\',
        1: '/'
    }
    return switcher.get(i, "Invalid mirror type!")


PUZZLESIZE = 4


# No random generation process is taken. Please refer to https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html to initiate the puzzle for current stage.
def initPuzzle():
    amount = {
        "ghost": 2,
        "vampire": 2,
        "zombie": 8
    }

    # Let's start with a 4x4 puzzle
    cells = [
        [Cell('monster', 2, False), Cell('monster', 3, False), Cell('monster', 3, False), Cell('monster', 3, False)],
        [Cell('monster', 3, False), Cell('mirror', 0, False), Cell('monster', 3, False), Cell('monster', 3, False)],
        [Cell('monster', 1, False), Cell('monster', 1, False), Cell('mirror', 1, False), Cell('monster', 3, False)],
        [Cell('monster', 2, False), Cell('mirror', 0, False), Cell('monster', 3, False), Cell('mirror', 0, False)]
    ]

    # For borders, the first dimension of the array indicates which border it is taking care of.
    # To be specific, 0 for left border, 1 for top border, 2 for right border and 3 for bottom border.
    # Then borders[0][0] indicates the first row of left border, borders[0][1] indicates the second row of left border, borders[1][0] indicates the first column of the top border and so on.
    borders = [
        [4, 3, 2, 1],
        [3, 3, 4, 3],
        [4, 3, 2, 3],
        [3, 0, 2, 3]
    ]

    return cells, borders, amount


# Print the puzzle out based on current map
def printPuzzle(cells, borders, amount):
    print("Ghost: " + str(amount["ghost"]), end=' ')
    print("Vampire: " + str(amount["vampire"]), end=' ')
    print("Zombie: " + str(amount["zombie"]) + "\n")

    print("    ", end='')
    for i in range(PUZZLESIZE):
        print(str(borders[1][i]) + "  ", end='')
    print('\n')

    for i in range(PUZZLESIZE):
        print(" " + str(borders[0][i]) + " ", end='')
        for j in range(PUZZLESIZE):
            if cells[i][j].cellType == "monster":
                print(" " + monster(cells[i][j].value) + " ", end='')
            else:
                print(" " + mirror(cells[i][j].value) + " ", end='')
        print(" " + str(borders[2][i]) + " ", end='')
        print('\n')

    print("    ", end='')
    for i in range(PUZZLESIZE):
        print(str(borders[3][i]) + "  ", end='')
    print('\n')


class CheckInfo:
    def __init__(self, visibleNum, direction, hasMetMirror, currentVisNum, coordinate):
        self.visibleNum = visibleNum
        self.direction = direction
        self.hasMetMirror = hasMetMirror
        self.currentVisNum = currentVisNum
        self.coordinate = coordinate


# TODO(Optional): Check the total number of monsters in the puzzle. Make sure it'll not exceed the limitation. (Implement if puzzle is randonmly generated)
def isValidPuzzle(cells, borders):
    for i in range(4):
        for j in range(PUZZLESIZE):
            # coordinate = initCoordinate(i, j)
            # visibleNum = borders[i][j]
            info = CheckInfo(visibleNum=borders[i][j], direction=i,
                             hasMetMirror=False, currentVisNum=0, coordinate=initCoordinate(i, j))
            result = isValidRoute(
                cells, info)
            if result == False:
                return False
    return True


def initCoordinate(i, j):
    if i == 0:
        return [j, -1]
    if i == 1:
        return [-1, j]
    if i == 2:
        return [j, PUZZLESIZE]
    if i == 3:
        return [PUZZLESIZE, j]


def isValidRoute(cells, info):
    # Move to next cell
    if info.direction == 0:
        info.coordinate[1] += 1
    if info.direction == 1:
        info.coordinate[0] += 1
    if info.direction == 2:
        info.coordinate[1] -= 1
    if info.direction == 3:
        info.coordinate[0] -= 1

    # Check if out of boundary, indicating the end of the route
    if info.coordinate[0] < 0 or info.coordinate[0] >= PUZZLESIZE or info.coordinate[1] < 0 or info.coordinate[1] >= PUZZLESIZE:
        if info.currentVisNum == info.visibleNum:
            return True
        else:
            return False

    thisCell = cells[info.coordinate[0]][info.coordinate[1]]

    # Check if mirror
    if thisCell.cellType == "mirror":
        info.hasMetMirror = True
        if thisCell.value == 0:
            if info.direction == 0:
                info.direction = 1
            elif info.direction == 1:
                info.direction = 0
            elif info.direction == 2:
                info.direction = 3
            elif info.direction == 3:
                info.direction = 2
            else:
                print("Error when asserting direction")
                exit(0)
        elif thisCell.value == 1:
            if info.direction in range(0, 4):
                info.direction = 3 - info.direction
            else:
                print("Error when asserting direction")
                exit(0)
        else:
            print("Invalid mirror value.")
            exit(0)
        return isValidRoute(cells, info)

    # Check if monster
    if thisCell.cellType == "monster":
        if thisCell.value == 0:
            return False
        if thisCell.value == 1 and info.hasMetMirror == True:
            info.currentVisNum += 1
        if thisCell.value == 2 and info.hasMetMirror == False:
            info.currentVisNum += 1
        if thisCell.value == 3:
            info.currentVisNum += 1

        if info.currentVisNum > info.visibleNum:
            return False
        else:
            return isValidRoute(cells, info)


# Get a plain list of monsters TBD
def getMonsterList(amount):
    monsterList = []
    for _ in range(amount["ghost"]):
        monsterList.append(1)

    for _ in range(amount["vampire"]):
        monsterList.append(2)

    for _ in range(amount["zombie"]):
        monsterList.append(3)

    return monsterList


def findAllSolutions(cells, borders, amount):
    totalSol = 0

    monsterList = getMonsterList(amount)
    monsterPerm = permutations(
        monsterList, len(monsterList))
    for trial in set(monsterPerm):
        index = 0
        for lenIndex in range(PUZZLESIZE):
            for widIndex in range(PUZZLESIZE):
                if cells[lenIndex][widIndex].cellType == "monster":
                    cells[lenIndex][widIndex].value = trial[index]
                    index += 1
        if isValidPuzzle(cells, borders) == True:
            totalSol += 1
            if totalSol <= 3:
                print("Solution " + str(totalSol) + ":")
                printPuzzle(cells, borders, amount)

    return totalSol


if __name__ == "__main__":
    cells, borders, amount = initPuzzle()
    printPuzzle(cells, borders, amount)
    print("Start finding solutions...")
    print("It might take a few minutes, please be patient...")
    solNum = findAllSolutions(cells, borders, amount)
    print("There are " + str(solNum) + " solution(s) in all")
