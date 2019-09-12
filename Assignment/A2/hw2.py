#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from ast import literal_eval as make_tuple
import math


# Edge definition:
# - p1, p2: endpoints of the segment
# - slope: slope of the segment
# - intersect: intersect of the line (extention of the segment most probably) on the y axis
class Edge:
    def __init__(self, p1, p2, slope, intersect):
        self.p1 = p1
        self.p2 = p2
        self.slope = slope
        self.intersect = intersect


# The point matrix would seem like following:
# (0,0) (0,1) (0,2) ... (0,n)
# (1,0) ...
# (2,0) ...
#   .
#   .
#   .
# (m,0) ...
# - points: A 2D array, storing `True/False` indicating whether the point is on a segment or not.
# - edges: The list storing current lines
def initPoints(m=4, n=4):
    points = []
    for _ in range(m):
        row = []
        for _ in range(n):
            row.append(False)
        points.append(row)
    return points


def printPuzzle(points):
    for i in points:
        print(i)


def rollTurn():
    if random.randint(1, 10) < 5:
        return 0
    else:
        return 1


turnMap = {0: "Player1", 1: "Player2"}


def checkValidEdge(points, edges, newEdge, endpoint):
    # print("Start checking edge validation...")
    # Check if endpoints match
    if not (-1, -1) in endpoint:
        # Must start fron an endpoint
        if not (newEdge.p1 in endpoint or newEdge.p2 in endpoint):
            return False
        # Cannot accept a line that would turn itself in to a closed shape
        if newEdge.p1 in endpoint and points[newEdge.p2[1]][newEdge.p2[0]] == True:
            return False
        if newEdge.p2 in endpoint and points[newEdge.p1[1]][newEdge.p1[0]] == True:
            return False

    # Check if it's the very first input for the entire puzzle
    if not edges:
        # print(0)
        return True

    # Check intersection:
    for edge in edges:
        # print("slopes:", edge.slope, newEdge.slope)
        if edge.slope != newEdge.slope:
            # print(1)
            # print(edge.intersect, newEdge.intersect)
            if edge.slope == 'infinity':
                intersectY = newEdge.slope*edge.p1[0] + newEdge.intersect
                if newEdge.slope == 0:
                    if (edge.p1[0], intersectY) not in endpoint and edge.p1[0] > min(newEdge.p1[0], newEdge.p2[0]) and edge.p1[0] < max(newEdge.p1[0], newEdge.p2[0]) and intersectY >= min(edge.p1[1], edge.p2[1]) and intersectY <= max(edge.p1[1], edge.p2[1]):
                        # print("HERE1")
                        return False
                if intersectY > min(newEdge.p1[1], newEdge.p2[1]) and intersectY < max(newEdge.p1[1], newEdge.p2[1]):
                    # print("HERE2")
                    return False
            elif newEdge.slope == 'infinity':
                intersectY = edge.slope*newEdge.p1[0] + edge.intersect
                if (intersectY == edge.p1[1] or intersectY == edge.p2[1]) and (edge.p1 not in endpoint and edge.p2 not in endpoint) and newEdge.p1[0] > min(edge.p1[0], edge.p2[0]) and newEdge.p1[0] < max(edge.p1[0], edge.p2[0]):
                    # print("HERE3")
                    return False
                if intersectY > min(edge.p1[1], edge.p2[1]) and intersectY < max(edge.p1[1], edge.p2[1]):
                    # print("HERE6")
                    return False
            else:
                intersectX = (edge.intersect - newEdge.intersect) / \
                    (newEdge.slope - edge.slope)
                # print(intersectX)
                if (intersectX == edge.p1[0] or intersectX == edge.p2[0]) and (edge.p1 not in endpoint and edge.p2 not in endpoint):
                    # print("HERE4")
                    return False
                if (intersectX > min(newEdge.p1[0], newEdge.p2[0]) and intersectX < max(newEdge.p1[0], newEdge.p2[0])) \
                        and (intersectX > min(edge.p1[0], edge.p2[0]) and intersectX < max(edge.p1[0], edge.p2[0])):
                    # print("HERE5")
                    return False
        else:
            # print(2)
            if newEdge.slope == 'infinity':
                if newEdge.p1[0] != edge.p1[0]:
                    continue
                else:
                    newEdgeYRange = range(min(newEdge.p1[1], newEdge.p2[1]), max(
                        newEdge.p1[1], newEdge.p2[1]) + 1)
                    edgeYRange = range(min(edge.p1[1], edge.p2[1]), max(
                        edge.p1[1], edge.p2[1]) + 1)
                    ns = set(newEdgeYRange)
                    inter = ns.intersection(edgeYRange)
                    if inter and len(inter) > 1:
                        return False
            else:
                if newEdge.intersect != edge.intersect:
                    continue
                else:
                    newEdgeXRange = range(min(newEdge.p1[0], newEdge.p2[0]), max(
                        newEdge.p1[0], newEdge.p2[0]) + 1)
                    edgeXRange = range(min(edge.p1[0], edge.p2[0]), max(
                        edge.p1[0], edge.p2[0]) + 1)
                    ns = set(newEdgeXRange)
                    inter = ns.intersection(edgeXRange)
                    if inter and len(inter) > 1:
                        return False

    return True


def moveToEdge(newMove):
    # Cannot set a same point twice as a valid segment
    if newMove[0] == newMove[1]:
        return None, False

    # Endpoints of a segement must be within the border of the puzzle
    for i in newMove:
        if not (i[0] in range(height) and i[1] in range(width)):
            return None, False

    x1 = newMove[0][1]
    y1 = newMove[0][0]
    x2 = newMove[1][1]
    y2 = newMove[1][0]
    if x1 == x2:
        slope = 'infinity'
        intersect = None
    else:
        slope = (y1 - y2)/(x1 - x2)
        intersect = (x1*y2 - x2*y1)/(x1 - x2)
    return Edge((x1, y1), (x2, y2), slope, intersect), True


def generateNextEdge(points, edges, endpoint):
    return (0, 0)


def getNextEdge(edges, endpoint):
    validMove = False
    validEdge = False
    while not validEdge:
        print("Please input a valid move:")
        newMove = input()
        # Always require two points as input
        # For example, ((0, 0), (1,0))
        newMove = make_tuple(newMove)
        if len(newMove) != 2:
            continue
        newEdge, validMove = moveToEdge(newMove)
        # print(validMove, "validMove")
        if not validMove:
            print("Invalid input!")
            continue
        validEdge = checkValidEdge(points, edges, newEdge, endpoint)
        if not validEdge:
            print("Invalid input!")
            continue
        # print(validEdge, "validEdge")
    return newEdge


def move(turn, points, edges, endpoint):
    if turn == 0:
        # newEdge = generateNextEdge(points, edges, endpoint)
        newEdge = getNextEdge(edges, endpoint)
    else:
        newEdge = getNextEdge(edges, endpoint)
    return newEdge


def checkIfFinished(points, edges, endpoint):
    for i in range(height):
        for j in range(width):
            for ep in endpoint:
                newMove = ((i, j), (ep[1], ep[0]))
                newEdge, validMove = moveToEdge(newMove)
                if validMove:
                    validEdge = checkValidEdge(
                        points, edges, newEdge, endpoint)
                    if validEdge:
                        return False
    return True


def updatePuzzle(points, newEdge, endpoint):
    # Update endpoint
    if (-1, -1) in endpoint:
        endpoint[0] = newEdge.p1
        endpoint[1] = newEdge.p2
    else:
        for i in range(2):
            if endpoint[i] == newEdge.p1:
                endpoint[i] = newEdge.p2
                break
            elif endpoint[i] == newEdge.p2:
                endpoint[i] = newEdge.p1
                break

    # Update points
    if newEdge.slope == 'infinity':
        for i in range(min(newEdge.p1[1], newEdge.p2[1]), max(newEdge.p1[1], newEdge.p2[1]) + 1):
            points[i][newEdge.p1[0]] = True
    else:
        for i in range(min(newEdge.p1[0], newEdge.p2[0]), max(newEdge.p1[0], newEdge.p2[0]) + 1):
            if math.floor(newEdge.slope*i + newEdge.intersect) == newEdge.slope*i + newEdge.intersect:
                points[math.floor(newEdge.slope*i +
                                  newEdge.intersect)][i] = True
    return


if __name__ == "__main__":
    print("Please input the height of the puzzle:")
    height = input()
    height = int(height)
    print("Please input the width of the puzzle:")
    width = input()
    width = int(width)

    points = initPoints(height, width)
    edges = []
    turn = rollTurn()
    finished = False

    endpoint = [(-1, -1), (-1, -1)]

    while not finished:
        print(turnMap[turn], "'s turn!")
        newEdge = move(turn, points, edges, endpoint)
        edges.append(newEdge)
        updatePuzzle(points, newEdge, endpoint)
        # print(endpoint)
        printPuzzle(points)
        print('\n')
        finished = checkIfFinished(points, edges, endpoint)
        turn = (turn + 1) % 2
    printPuzzle(points)
    print("No more available moves!")
    print(turnMap[turn], "wins!")
