from math import *

def distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def sub(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]

def add(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]

def mul(v, s):
    return v[0] * s, v[1] * s

def avg(*vectors):
    v = (0,0)
    for vector in vectors:
        v = add(v, vector)
    return mul(v, 1/len(vectors))

def unit_vector(vector):
    length = sqrt(vector[0]**2 + vector[1]**2)
    return vector[0]/length, vector[1]/length

def midpoint(p1, p2):
    return (p1[0] + p2[0])/2, (p1[1] + p2[1])/2

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
