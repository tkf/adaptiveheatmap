"""
`pcolor <.core.pcolor>` demo
----------------------------

`pcolor <.core.pcolor>` can be used like
`matplotlib.pyplot.pcolor`.
"""

from matplotlib import pyplot

from adaptiveheatmap.demos import data_hump_and_spike
import adaptiveheatmap

pyplot.style.use("fivethirtyeight")

X, Y, Z = data_hump_and_spike()
ah = adaptiveheatmap.pcolor(X, Y, Z, cmap='inferno')
ah.set_xlabel('X')
ah.set_ylabel('Y')
ah.set_zlabel('Z')
# ah.relate_xyzq(1, -0.2)  # not supported
ah.figure.suptitle('pcolor')

pyplot.show()
