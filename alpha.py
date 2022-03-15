from tkinter import Tk, BOTH, X, Y, LEFT, RIGHT, Button, BOTTOM
from tkinter.ttk import Frame
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from numpy.random import rand
import numpy as np
from numpy import cos, pi
from skimage import measure
import matplotlib.pyplot as plt

root = Tk()
root.wm_title("Organizing")

leftFrame = Frame(root)
rightFrame = Frame(root)

#left
leftFigure = Figure(figsize=(5, 4), dpi=100)
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
def onpick(event):
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
leftFigure.canvas.mpl_connect('pick_event', onpick)

leftCanvas = FigureCanvasTkAgg(leftFigure, master=leftFrame)  # A tk.DrawingArea.
leftCanvas.draw()

leftToolbar = NavigationToolbar2Tk(leftCanvas, leftFrame, pack_toolbar=False)
leftToolbar.update()
leftToolbar.pack(side=BOTTOM, fill=X)

leftCanvas.get_tk_widget().pack(expand=1, fill=BOTH)

#right
def fun(x, y, z):
    return cos(x) + cos(y) + cos(z)

x, y, z = pi*np.mgrid[-1:1:31j, -1:1:31j, -1:1:31j]
vol = fun(x, y, z)
iso_val=0.0
verts, faces, _, _ = measure.marching_cubes(vol, iso_val, spacing=(0.1, 0.1, 0.1))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rightFigure = Figure(figsize=(5,4), dpi=100)
rightAx = rightFigure.add_subplot(111, projection='3d')
def plotSurface(xoffset=0, yoffset=0):
    return rightAx.plot_trisurf([x + xoffset for x in verts[:, 0]], [y + yoffset for y in verts[:,1]], faces, verts[:, 2],
                cmap='Spectral', lw=1)

surface = plotSurface()
rightAx.set_xlabel('X Label')
rightAx.set_ylabel('Y Label')
rightAx.set_zlabel('Z Label')
rightAx.set_title('Pick a point')

rightCanvas = FigureCanvasTkAgg(rightFigure, master=rightFrame)  # A tk.DrawingArea.
rightCanvas.draw()

rightToolbar = NavigationToolbar2Tk(rightCanvas, rightFrame, pack_toolbar=False)
rightToolbar.update()
rightToolbar.pack(side=BOTTOM, fill=X)

rightCanvas.get_tk_widget().pack(expand=1, fill=BOTH)

#pack main window
leftFrame.pack(side=LEFT, fill=Y)
rightFrame.pack(side=RIGHT, fill=Y)

root.mainloop()