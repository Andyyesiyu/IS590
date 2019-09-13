#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


# Point definition
#   - prev: For solution member, indicating the previous point. `None` for start point.
#   - dirToNxt: For solution member, indicating the direction it is pointing to the next point.
#   - nxt: For solution member, indicating the next point. `None` for end point.
#   - arrows: A `string` list storing all available arrows at current point.
#       - arrows are strings representing the direction it's pointing
#       - 12 types in total: e, w ,s ,n, se, sw, wn, ws, ne, nw, en, es
class Point:
    def __init__(self, prev, dirToNxt, nxt, arrows):
        self.prev = prev
        self.dirToNxt = dirToNxt
        self.nxt = nxt
        self.arrows = arrows


# pairMap:
# For checking the pair that would generate unexpected new arrows
pairMap = {
    "ws": ["se", "n", "nw"],
    "wn": ["ne", "s", "sw"],
    "ne": ["wn", "w", "es"],
    "es": ["ne", "n", "sw"],
    "se": ["en", "w", "ws"],
    "en": ["se", "s", "nw"],
    "sw": ["wn", "e", "es"],
    "nw": ["ws", "e", "en"],
    "n": ["ws", "es"],
    "s": ["wn", "en"],
    "w": ["ne", "se"],
    "e": ["sw", "nw"]
}


# outcomeMap:
# For checking the extra outcome generated by the combinations of certain arrows
outcomeMap = {
    ('se', 'ws'): 'es',
    ('ne', 'ne'): 'en',
    ('es', 'ne'): 'se',
    ('en', 'se'): 'ne',
    ('se', 'wn'): 'nw',
    ('nw', 'ws'): 'sw',
    ('en', 'nw'): 'wn',
    ('es', 'sw'): 'ws',
    ('n', 'ws'): 's',
    ('es', 'n'): 's',
    ('s', 'wn'): 'n',
    ('en', 's'): 'n',
    ('ne', 'w'): 'e',
    ('se', 'w'): 'e',
    ('e', 'sw'): 'w',
    ('e', 'nw'): 'w'
}


def printPuzzle(points):
    a = ""
    for i in range(len(points)):
        for j in range(len(points[i])):
            currPoint = points[i][j]
            if not currPoint.arrows:
                a += 'null' + '\t'
            else:
                a += ','.join(currPoint.arrows) + '\t'
        a += '\n'
    print(a)


def initPoints(width, height):
    points = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(Point(None, None, None, []))
        points.append(row)
    return points


# directMap:
# For quickly getting the type of arrow depending on prev direction and next direction
directMap = {
    ("n", "n"): "n",
    ("e", "e"): "e",
    ("s", "s"): "s",
    ("w", "w"): "w",
    ("n", "e"): "se",
    ("n", "w"): "sw",
    ("s", "e"): "ne",
    ("s", "w"): "nw",
    ("e", "n"): "wn",
    ("e", "s"): "ws",
    ("w", "n"): "en",
    ("w", "s"): "es"
}


# Our puzzle will always start from the left border and ends on the right border for simplicity
# This feature has little impact on the puzzle difficulty as the remaining parts for determining the solution are all random
# The direction of next step is randomly generated:
#   0 for up, 1 for right, 2 for down, 3 for left
def findValidMove(current, width, height):
    # check whether in a line, whether conflict with
    validMoveList = []

    # Check left


def getDirection(current, nextMove):
    if current[0] != nextMove[0]:
        if current[0] - nextMove[0] == -1:
            return "s"
        if current[0] - nextMove[0] == 1:
            return "n"
    if current[1] != nextMove[1]:
        if current[1] - nextMove[1] == -1:
            return "e"
        if current[1] - nextMove[1] == 1:
            return "w"
    return "nonsense"


def pushArrow(points, current, arrow):
    # points[current[0]][current[1]].arrows
    arrowList = [arrow]
    while len(arrowList) > 0:
        candidate = arrowList.pop(0)
        for targetArr in pairMap[candidate]:
            if targetArr in points[current[0]][current[1]].arrows:
                addionArrow = outcomeMap[tuple(sorted([targetArr, arrow]))]
                points[current[0]][current[1]].arrows.append(addionArrow)
                arrowList.append(candidate)
    return


def findSolution(points, width, height):
    randStartRow = random.randint(0, len(points[0]) - 1)
    start = (randStartRow, 0)
    current = start
    points[current[0]][0]
    finished = False

    while not finished:
        # Get all valid moves and randomly pick one
        validMovelist = findValidMove(current, width, height)
        nextMove = random.choice(validMovelist)
        points[nextMove[0]][nextMove[1]].prev = current
        points[current[0]][current[1]].next = nextMove
        dirToNxt = getDirection(current, nextMove)
        points[current[0]][current[1]].dirToNxt = dirToNxt

        # Get  the direction from current point to the picked move and get the corresponding arrow
        if points[current[0]][current[1]].prev:
            prev0 = points[current[0]][current[1]].prev[0]
            prev1 = points[current[0]][current[1]].prev[1]
            arrow = directMap[points[prev0][prev1].dirToNxt, dirToNxt]
        else:
            arrow = directMap[dirToNxt, dirToNxt]
        pushArrow(points, current, arrow)

    return start


def generatePuzzle(width, height):
    points = initPoints(width, height)
    start = findSolution(points, width, height)
    return points, start


if __name__ == "__main__":
    width = 4
    height = 4

    points, start = generatePuzzle(width, height)
    printPuzzle(points)