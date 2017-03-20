
import random
from math import *

def distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def point_on_line(p, line):
    x1, x2 = sorted([line[0][0], line[1][0]])
    y1, y2 = sorted([line[0][1], line[1][1]])
    return x1 <= p[0] <= x2 and y1 <= p[1] <= y2


def intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if point_on_line((x,y), line1) and point_on_line((x,y), line2):
        return x,y
    else:
        return False

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
            line(*wall)

    def getWalls(self, scale, x, y):
        walls = []
        if self.walls[0]:
            walls.append(((scale*self.x     + x, scale*self.y     + y), (scale*(self.x+1) + x, scale*self.y + y)))
        if self.walls[1]:
            walls.append(((scale*(self.x+1) + x, scale*self.y     + y), (scale*(self.x+1) + x, scale*(self.y+1) + y)))
        if self.walls[2]:
            walls.append(((scale*self.x     + x, scale*(self.y+1) + y), (scale*(self.x+1) + x, scale*(self.y+1) + y)))
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
        self.scale = 40
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

class Sensor():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y

        self.angle = angle
        self.length = 160

        self.last_pois = []

    def move(self, x, y):
        self.x += x
        self.y += y

    def turn(self, a):
        self.angle += a

    def getLine(self):
        return (self.x, self.y), (sin(self.angle) * self.length + self.x, cos(self.angle) * self.length + self.y)

    def draw(self):
        poi = self.poi()
        if poi: line((self.x, self.y), self.poi(), "red")

    def poi(self):
        line = self.getLine()
        for l in lines:
            if distance(line[0], l[0]) < self.length + distance(*l):
                poi = intersection(line, l)
                if poi:
                    return poi
        return False


    def value(self):
        poi = self.poi()
        if poi:
            circle(poi, 3, "red")
            return distance((self.x, self.y), poi)
        else:
            return False

class Robot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.angle = 0
        self.sensor = Sensor(x,y,0)

    def draw(self):
        self.sensor.draw()
        circle((self.x, self.y), 8)

    def move(self, d):
        self.x += sin(self.angle) * d
        self.y += cos(self.angle) * d
        self.sensor.x = self.x
        self.sensor.y = self.y

    def turn(self, a):
        self.angle += a
        self.sensor.angle += a

    def update(self):



maze = Maze(16,16)
maze.generate()
robot = Robot(-280, -280)


lines = []
for l in maze.getWalls(-300,-300):
    lines.append(l)

def redraw():
    t.clear()
    robot.draw()

    for l in lines:
        line(*l)

    screen.ontimer(redraw, 10)

def update():
    robot.update()
    screen.ontimer(update, 500)

update()
redraw()
