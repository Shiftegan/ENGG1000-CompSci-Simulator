import maze
import draw
import robot
from math import *

import threading

maze = maze.Maze(16,16)
maze.generate()

lines = []
for l in maze.getWalls(-300,-300):
    lines.append(l)

robot = robot.setup(-140, -140, lines)

def redraw():
    draw.clear()
    robot.draw()

    for l in lines:
        draw.line(*l)

    draw.ontimer(redraw, 1000//60)

def update():
    robot.update()
    draw.ontimer(update, 100)

update()
redraw()

def other():
    import ev_code

my_thread = threading.Thread(target=other)
my_thread.daemon = True
my_thread.start()

draw.mainloop()
