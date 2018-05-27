"""
`.pcolormesh` demo
------------------

`.pcolormesh` can be used like `matplotlib.pyplot.pcolormesh`.
"""

from matplotlib import pyplot

from adaptiveheatmap.demos import data_hump_and_spike
import adaptiveheatmap

X, Y, Z = data_hump_and_spike()
ah = adaptiveheatmap.pcolormesh(X, Y, Z)
ah.set_xlabel('X')
ah.set_ylabel('Y')
ah.set_zlabel('Z')
ah.draw_xyz(1, -0.2)
ah.figure.suptitle('pcolormesh')

pyplot.show()
