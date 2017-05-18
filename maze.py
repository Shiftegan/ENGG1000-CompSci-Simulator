from math import *
from lines import *
import random
import draw


class Cell():
    def __init__(self, maze, x, y):
        self.neighbours = [False, False, False, False]
        self.walls = [True, True, True, True]
        self.x = x
        self.y = y
        self.maze = maze
        self.seen = False

    def __str__(self):
        return " " + str(int(self.walls[0])) + " \n" + str(int(self.walls[3])) + str(int(self.seen)) + str(int(self.walls[1])) + "\n " + str(int(self.walls[2])) + " "


    def setup(self):
        self.neighbours = self.maze.getNeighbours(self.x,self.y)

    def draw(self, scale, x, y):
        for wall in self.getWalls(scale, x, y):
            draw.line(*wall)

    def getWalls(self, scale, x, y):
        walls = []
        if self.walls[0]:
            walls.append(((scale*self.x     + x, scale*self.y     + y), (scale*(self.x+1) + x, scale*self.y + y)))
        if self.walls[1]:
            walls.append(((scale*(self.x+1) + x, scale*self.y     + y), (scale*(self.x+1) + x, scale*(self.y+1) + y + 1)))
        if self.walls[2]:
            walls.append(((scale*self.x     + x, scale*(self.y+1) + y), (scale*(self.x+1) + x + 1, scale*(self.y+1) + y)))
        if self.walls[3]:
            walls.append(((scale*self.x     + x, scale*self.y     + y), (scale*self.x     + x, scale*(self.y+1) + y)))
        return walls

    def unseenNeighbour(self):
        neighbours = []
        for n in self.neighbours:
            if n and not n.seen:
                neighbours.append(n)
        if len(neighbours):
            return random.choice(neighbours)
        else:
            return False

    def openNeighbour(self):
        neighbours = []
        for n in self.neighbours:
            if not self.walled(n):
                neighbours.append(n)
        if len(neighbours):
            return random.choice(neighbours)
        else:
            return False

    def closedNeighbour(self):
        neighbours = []
        for n in self.neighbours:
            if self.walled(n):
                neighbours.append(n)
        if len(neighbours):
            return random.choice(neighbours)
        else:
            return False

    def walled(self, other):
        if other in self.neighbours and not self.walls[self.neighbours.index(other)]:
            return False
        else:
            return True

class Maze():
    def __init__(self, width, height):
        self.cells = []
        self.width = width
        self.height = height
        self.scale = 60
        self.populate()
        self.setup()

    def populate(self):
        for x in range(self.width):
                self.cells.append([])
                for y in range(self.height):
                    self.cells[x].append(Cell(self, x, y))

    def setup(self):
        for x in range(self.width):
            for y in range(self.height):
                self.cells[x][y].setup()

    def getNeighbours(self, x, y):
        neighbours = []
        if y != 0:
            neighbours.append(self.cells[x][y-1])
        else:
            neighbours.append(False)
        if x != self.width-1:
            neighbours.append(self.cells[x+1][y])
        else:
            neighbours.append(False)
        if y != self.height-1:
            neighbours.append(self.cells[x][y+1])
        else:
            neighbours.append(False)
        if x != 0:
            neighbours.append(self.cells[x-1][y])
        else:
            neighbours.append(False)
        return neighbours

    def draw(self, x, y):
        scale = self.scale
        for i in range(maze.width):
            for j in range(maze.height):
                cell = maze.cells[i][j]
                cell.draw(scale, x, y)

    def connect(self, cell1, cell2):
        index = cell1.neighbours.index(cell2)
        cell1.walls[index] = False
        cell2.walls[index-2] = False

    def randomCell(self):
        return self.cells[random.randint(0, self.width-1)][random.randint(0, self.height-1)]

    def generate(self):
        self.cells[0][0].seen = True
        stack = [self.cells[0][0]]
        while len(stack):
            current = stack[-1]
            nextcell = current.unseenNeighbour()
            if not nextcell:
                stack.pop()
            else:
                self.connect(current, nextcell)
                stack.append(nextcell)
                nextcell.seen = True

        for i in range(int(self.width*self.height*0.1)):
            cell = self.randomCell()
            other = cell.closedNeighbour()
            if other:
                self.connect(cell, other)

    def getWalls(self, x, y):
        scale = self.scale
        lines = []
        for i in range(self.width):
            for j in range(self.height):
                for line in self.cells[i][j].getWalls(scale, x, y):
                    if not line in lines:
                        lines.append(line)
        return lines
