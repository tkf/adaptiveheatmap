"""
`hist2d <.core.hist2d>` demo
----------------------------

`hist2d <.core.hist2d>` can be used like `matplotlib.pyplot.hist2d`.

https://matplotlib.org/examples/pylab_examples/hist2d_log_demo.html
"""

from matplotlib import pyplot
import numpy

import adaptiveheatmap

pyplot.style.use("ggplot")

x = numpy.random.randn(100000)
y = numpy.random.randn(100000)
ah = adaptiveheatmap.hist2d(x, y, bins=40, cmap='cividis')
ah.relate_xyzq(0.5, 0.5)
ah.figure.suptitle('hist2d')

pyplot.show()
