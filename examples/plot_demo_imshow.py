"""
`.imshow` demo
--------------

`.imshow` can be used like `matplotlib.pyplot.imshow`.
"""

from matplotlib import pyplot

from adaptiveheatmap.demos import data_hump_and_spike
import adaptiveheatmap

_X, _Y, Z = data_hump_and_spike()
ah = adaptiveheatmap.imshow(Z)
ah.set_xlabel('X')
ah.set_ylabel('Y')
ah.set_zlabel('Z')
ah.draw_xyz(1, -0.2)
ah.figure.suptitle('imshow')

pyplot.show()
