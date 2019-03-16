from AsciiParser import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


fm = AsciiParser('files/test_files/ascii_files/fuel_map_test.asc')
fm.read()

dem = AsciiParser('files/test_files/ascii_files/dem_test.asc')
dem.read()

x_start = dem.xllcorner
x_end = x_start + (dem.cell_size * dem.ncols)

y_start = dem.xllcorner
y_end = y_start + (dem.cell_size * dem.nrows)

X = np.arange(x_start, x_end, dem.cell_size)
Y = np.arange(y_start, y_end, dem.cell_size)

xlen = len(X)
ylen = len(Y)

X, Y = np.meshgrid(X, Y)

Z = dem.data_table
# color = fm.data_table

# Create an empty array of strings with the same shape as the meshgrid, and
# populate it with two colors in a checkerboard pattern.
colortuple = ('w', 'w', 'g', 'b')
colors = np.empty(X.shape, dtype=str)
for y in range(ylen):
    for x in range(xlen):

        color = colortuple[int(fm.data_table[y, x])]

        colors[y, x] = color


print(X.shape, Y.shape, Z.shape, colors)

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, facecolors=colors, edgecolors='k', lw=1)
plt.show()