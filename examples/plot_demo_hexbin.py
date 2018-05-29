"""
`hexbin <.core.hexbin>` demo
----------------------------

`hexbin <.core.hexbin>` can be used like `matplotlib.pyplot.hexbin`.
"""

from matplotlib import pyplot
import numpy

import adaptiveheatmap

pyplot.style.use("ggplot")

x = numpy.exp(numpy.random.randn(100000))
y = numpy.random.randn(100000)
ah = adaptiveheatmap.hexbin(x, y, vmin=1)
# ah.relate_xyzq(0.5, 0.5)  # not supported
ah.figure.suptitle('adaptiveheatmap.hexbin')
ah.ax_main.set_xlim(xmax=30)

pyplot.figure()
pyplot.hexbin(x, y, vmin=1)
pyplot.colorbar()
pyplot.suptitle('pyplot.hexbin')
pyplot.xlim(xmax=30)

pyplot.show()
