import maze
import draw
import robot
from math import *

import threading

speed = 1
target_frames = 30

maze = maze.Maze(5,5)
maze.generate()
lines = []
# lines = [((0,0), (0,40)), ((0,0), (40,0)), ((40,0), (40,40)), ((0,40), (40,40))]
for l in maze.getWalls(10,10):
    lines.append(l)

robot = robot.setup(100,100, lines)

def redraw():
    draw.clear()

    for i in range(speed):
        robot.update()

    for l in lines:
        draw.line(*l)

    robot.draw()
    draw.camera = robot.getPos()
    draw.ontimer(redraw, 1000//target_frames)

def other():
    import ev_code

redraw()

my_thread = threading.Thread(target=other)
my_thread.daemon = True
my_thread.start()

draw.mainloop()
