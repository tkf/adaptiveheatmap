"""
`pcolor <.core.pcolor>` demo
----------------------------

`pcolor <.core.pcolor>` can be used like
`matplotlib.pyplot.pcolormesh`.
"""

from matplotlib import pyplot

from adaptiveheatmap.demos import data_hump_and_spike
import adaptiveheatmap

X, Y, Z = data_hump_and_spike()
ah = adaptiveheatmap.pcolor(X, Y, Z)
ah.set_xlabel('X')
ah.set_ylabel('Y')
ah.set_zlabel('Z')
# ah.draw_xyz(1, -0.2)  # not supported
ah.figure.suptitle('pcolor')

pyplot.show()
