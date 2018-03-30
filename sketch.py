#!/usr/bin/python
import tkinter as tk
from random import random
from astar import *

# two points as user input (source cell and destination cell)
points = 2

# windows size (height x width)
height = 500
width = 500

# size of each cell(in pixels) in grid
pixel = 10

# grid (rows x cols)
rows = height // pixel
cols = width // pixel

# show open and closed list
showoc = True

# walls 0 <= x < 1
walldensity = 0.3

class Node(object):
    def __init__(self, i, j, walldens=0.2):
        self.i = i
        self.j = j
        self.x = i*pixel + pixel//2
        self.y = j*pixel + pixel//2

        self.f = 0
        self.g = 0
        self.h = 0

        self.neighbors = []
        self.previous = None
        self.wall = False

        if random() < walldens:
            self.wall = True

    def show(self, **kwargs):
        if not self.wall:
            c.create_rectangle(self.i*pixel,
                               self.j*pixel,
                               self.i*pixel + pixel,
                               self.j*pixel + pixel,
                               **kwargs)
        else:
            c.create_rectangle(self.i*pixel,
                               self.j*pixel,
                               self.i*pixel + pixel,
                               self.j*pixel + pixel,
                               fill='black')

    def draw_line(self, **kwargs):
        if self.previous:
            c.create_line(self.previous.x,
                          self.previous.y,
                          self.x,
                          self.y,
                          **kwargs)


    def addNeighbors(self):
        i = self.i
        j = self.j
        if i < rows - 1:
            self.neighbors.append(grid[i+1][j])
            if j > 0: self.neighbors.append(grid[i+1][j-1])
            if j < cols - 1: self.neighbors.append(grid[i+1][j+1])
        if i > 0:
            self.neighbors.append(grid[i-1][j])
            if j > 0: self.neighbors.append(grid[i-1][j-1])
            if j < cols - 1: self.neighbors.append(grid[i-1][j+1])
        if j < cols - 1: self.neighbors.append(grid[i][j+1])
        if j > 0: self.neighbors.append(grid[i][j-1])

    def getNeighbors(self):
        if len(self.neighbors) > 0:
            return self.neighbors
        else:
            self.addNeighbors()
            return self.neighbors


def get_run(event):
    # get global values of vars
    global points, c, src, dst

    # get source vertex
    if points == 2:
        src = grid[event.x // pixel][event.y // pixel]
        # ignore input if its wall
        if src.wall:
            return
        src.show(fill='blue')
        points -= 1

    # get destination vertex
    elif points == 1:
        dst = grid[event.x // pixel][event.y // pixel]
        if dst.wall:
            return
        dst.show(fill='green')
        points -= 1

        # run A* Path Finder
        Astar = AStarPathFinder(src, dst)
        while True:
            ret = Astar.step(showoc=showoc)

            # backtrack path from current node
            Astar.backtrack()

            if ret:
                break

            # update canvas at each step
            c.update()
    else: pass

top = tk.Tk()

c = tk.Canvas(top, width=width, height=height)
c.pack()

c.bind("<Button-1>", get_run)
grid = [[Node(i, j, walldensity) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        if showoc:
            grid[i][j].show(fill='white')
        else:
            grid[i][j].show(fill='white', outline='')

tk.mainloop()
