"""
`matshow <.core.matshow>` demo
------------------------------

`matshow <.core.matshow>` can be used like
`matplotlib.pyplot.matshow`.
"""

from matplotlib import pyplot

from adaptiveheatmap.demos import data_hump_and_spike
import adaptiveheatmap

pyplot.style.use("bmh")

_X, _Y, Z = data_hump_and_spike()
ah = adaptiveheatmap.matshow(Z)
ah.set_xlabel('X')
ah.set_ylabel('Y')
ah.set_zlabel('Z')
ah.draw_xyz(40, 80)
ah.figure.suptitle('matshow')

pyplot.show()
