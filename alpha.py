from tkinter import Tk, BOTH, X, Y, LEFT, RIGHT, Button, BOTTOM
from tkinter.ttk import Frame
from turtle import screensize

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from numpy.random import rand
import numpy as np

import matplotlib.pyplot as plt

root = Tk()
root.wm_title("Fooling")
root.geometry("1200x600")

leftFrame = Frame(root)
rightFrame = Frame(root)

leftFigure = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
leftAx = leftFigure.add_subplot()
leftAx.set_title('custom picker for line data')

maxd = 0.02
def line_picker(line, mouseevent):
    if mouseevent.xdata is None:
        return False, dict()
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    d = np.sqrt((xdata - mouseevent.xdata)**2. + (ydata - mouseevent.ydata)**2.)

    ind = np.nonzero(np.less_equal(d, maxd))
    if len(ind):
        pickx = np.take(xdata, ind)
        picky = np.take(ydata, ind)
        props = dict(ind=ind, pickx=pickx, picky=picky)
        return True, props
    else:
        return False, dict()

global markedPoint
global surface
markedPoint = None
def onpick2(event):
    global markedPoint
    global surface
    if event.pickx.size>0:
        xCord = event.pickx[0][0]
        yCord = event.picky[0][0]
        circle = plt.Circle((xCord, yCord), maxd, color='r', fill=False)
        if markedPoint:
            markedPoint.remove()
        leftAx.add_patch(circle)
        rightAx.set_title('(%2f,%2f)'%(xCord, yCord))
        surface.remove()
        surface = plotSurface(xCord, yCord)
        markedPoint = circle
    else:
        if markedPoint:
            markedPoint.remove()
            markedPoint = None
        rightAx.set_title('Pick a point')
    rightCanvas.draw()
    leftCanvas.draw()

line, = leftAx.plot(rand(100), rand(100), 'o', picker=line_picker)
leftFigure.canvas.mpl_connect('pick_event', onpick2)

def fun(x, y):
    return x**2 + y

rightFigure = Figure(figsize=(5,4), dpi=100)
rightAx = rightFigure.add_subplot(111, projection='3d')
def plotSurface(xoffset=0, yoffset=0):
    xData = yData = np.arange(-3.0+xoffset, 3.0+yoffset, 0.05)
    xGrid, yGrid = np.meshgrid(xData, yData)
    zData = np.array(fun(np.ravel(xGrid), np.ravel(yGrid)))
    zGrid = zData.reshape(xGrid.shape)
    return rightAx.plot_surface(xGrid, yGrid, zGrid)

surface = plotSurface()
rightAx.set_xlabel('X Label')
rightAx.set_ylabel('Y Label')
rightAx.set_zlabel('Z Label')
rightAx.set_title('Pick a point')

leftCanvas = FigureCanvasTkAgg(leftFigure, master=leftFrame)  # A tk.DrawingArea.
leftCanvas.draw()

rightCanvas = FigureCanvasTkAgg(rightFigure, master=rightFrame)  # A tk.DrawingArea.
rightCanvas.draw()

leftToolbar = NavigationToolbar2Tk(leftCanvas, leftFrame, pack_toolbar=False)
leftToolbar.update()
leftToolbar.pack(side=BOTTOM, fill=X)

rightToolbar = NavigationToolbar2Tk(rightCanvas, rightFrame, pack_toolbar=False)
rightToolbar.update()
rightToolbar.pack(side=BOTTOM, fill=X)

leftCanvas.get_tk_widget().pack(expand=1, fill=BOTH)
rightCanvas.get_tk_widget().pack(expand=1, fill=BOTH)

leftFrame.pack(side=LEFT, fill=Y)
rightFrame.pack(side=RIGHT, fill=Y)


root.mainloop()