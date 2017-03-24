import draw, lines
import random

def randPoint(x1, x2, y1, y2):
    return (random.randint(x1, x2), random.randint(y1, y2))

def randLine(x1, x2, y1, y2):
    return (randPoint(x1, x2, y1, y2), randPoint(x1, x2, y1, y2))

TILE = 50

for row in range(-10, 10):
    for col in range(-10, 10):
        a = randLine(col*TILE, (col+1/2)*TILE, row*TILE, (row+1/2)*TILE)
        b = randLine(col*TILE, (col+1/2)*TILE, row*TILE, (row+1/2)*TILE)
        draw.line(a[0], a[1])
        draw.line(b[0], b[1])
        if lines.intersection(a, b):
            draw.circle(lines.intersection(a, b), 5)

draw.mainloop()
