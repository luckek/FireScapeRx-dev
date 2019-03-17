from AsciiParser import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QScrollArea
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class Visualization(QScrollArea):

    def __init__(self, fm, dem, parent=None):

        super(Visualization, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        self._fm = fm
        self._dem = dem

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        self.button.click()

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.setGeometry(QtCore.QRect(10, 70, 600, 510))

    def plot(self):

        ''' plot some random stuff '''

        # random data
        X, Y, Z, colors = self.make_data_and_colors()

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.gca(projection='3d')

        # plot data
        ax.plot_surface(X, Y, Z, facecolors=colors, edgecolors='k', lw=0)
        ax.view_init(elev=48, azim=-91)

        # ax.

        # refresh canvas
        self.canvas.draw()

    def make_data_and_colors(self):

        x_start = self._dem.xllcorner
        x_end = x_start + (self._dem.cell_size * self._dem.ncols)

        y_start = self._dem.yllcorner
        y_end = y_start + (self._dem.cell_size * self._dem.nrows)

        X = np.arange(x_start, x_end, self._dem.cell_size)
        Y = np.arange(y_start, y_end, self._dem.cell_size)

        xlen = len(X)
        ylen = len(Y)

        X, Y = np.meshgrid(X, Y)

        Z = self._dem.data_table

        # Create an empty array of strings with the same shape as the meshgrid, and
        # populate it with two colors in a checkerboard pattern.
        colortuple = ('w', 'b', 'g', 'k')
        colors = np.empty(X.shape, dtype=str)
        for y in range(ylen):
            for x in range(xlen):
                color = colortuple[int(self._fm.data_table[y, x])]

                colors[y, x] = color

        print(X.shape, Y.shape, Z.shape, colors)

        return X, Y, Z, colors
