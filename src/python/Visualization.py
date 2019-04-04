import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D


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
        self.plot()

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.setGeometry(QtCore.QRect(10, 120, 820, 800))

    def plot(self):

        """ plot given data """

        # random data
        X, Y, Z, colors = self.make_data_and_colors()

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.gca(projection='3d')

        # plot data
        ax.plot_surface(X, Y, Z, facecolors=colors, edgecolors='k', lw=0, alpha=1.0)
        ax.view_init(elev=48, azim=-91)

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
        colortuple = ('grey', 'green', 'black')

        # TODO:
        # fuel_colors = FuelMapViewer.colors()

        # fuel_colors = [x.getRgb()[:3] for x in fuel_colors]

        # for name in fuel_colors:
        #     if name is 'grey':
        #         colortuple.append('g')
        #

        colors = np.empty(X.shape, dtype=object)
        for y in range(ylen):
            for x in range(xlen):

                curr_value = int(self._fm.data_table[y, x])

                if curr_value == -1:
                    color = colortuple[curr_value]

                else:
                    color = colortuple[curr_value - 1]

                colors[y, x] = color

        return X, Y, Z, colors
