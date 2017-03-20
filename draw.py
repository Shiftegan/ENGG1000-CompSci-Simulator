import turtle

t = turtle.Turtle()
screen = t.getscreen()

t.speed(0)
t.hideturtle()
screen.tracer(0,0)

def clear():
    t.clear()

def ontimer(func, t):
    screen.ontimer(func, t)

def line(p1, p2, color = "black"):
    t.color(color)
    t.penup()
    t.goto(p1[0],p1[1])
    t.pendown()
    t.goto(p2[0], p2[1])
    t.penup()

def circle(p, r, color = "black"):
    t.color(color)
    t.penup()
    t.goto(p[0],p[1]-r)
    t.pendown()
    t.circle(r)
    t.penup()

def mainloop():
    screen.mainloop()
