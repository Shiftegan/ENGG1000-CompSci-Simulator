import tkinter as tk

master = tk.Tk()
width = 800
height = 800
canvas = tk.Canvas(master, width=width, height=height)
camera = (0,0)

canvas.pack()

def c(p):
    return p[0] - camera[0] + width/2, p[1] - camera[1] + height/2

def a(p, x):
    return p[0] + x, p[1] + x

def clear():
    canvas.delete("all")

def ontimer(func, t):
    canvas.after(t, func)

def line(p1, p2, color = "black"):
    return canvas.create_line(*c(p1), *c(p2), fill=color)

def circle(p, r, color = "black"):
    return canvas.create_oval(c(a(p, -r)), c(a(p, r)), outline=color)

def mainloop():
    master.mainloop()
