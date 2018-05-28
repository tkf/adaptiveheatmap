"""
`hexbin <.core.hexbin>` demo
----------------------------

`hexbin <.core.hexbin>` can be used like `matplotlib.pyplot.hexbin`.
"""

from matplotlib import pyplot
import numpy

import adaptiveheatmap

pyplot.style.use("ggplot")

x = numpy.random.randn(100000)
y = numpy.random.randn(100000)
ah = adaptiveheatmap.hexbin(x, y, cmap='cividis')
# ah.relate_xyzq(0.5, 0.5)  # not supported
ah.figure.suptitle('hexbin')

pyplot.show()
