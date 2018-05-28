"""
`pcolormesh <.core.pcolormesh>` with ``data`` keyword
-----------------------------------------------------

As `matplotlib.pyplot.pcolormesh`, `pcolormesh <.core.pcolormesh>` can
take ``data`` keyword.
"""

from matplotlib import pyplot

from adaptiveheatmap.demos import data_hump_and_spike
import adaptiveheatmap

pyplot.style.use("seaborn-pastel")

X, Y, Z = data_hump_and_spike()
data = dict(X=X, Y=Y, Z=Z)
ah = adaptiveheatmap.pcolormesh('X', 'Y', 'Z', data=data, cmap='plasma')
ah.set_xlabel('X')
ah.set_ylabel('Y')
ah.set_zlabel('Z')
ah.draw_xyz(1, -0.2)
ah.figure.suptitle('pcolormesh')

pyplot.show()
