"""
`.cumhist` demo
---------------

Plot cumulative distribution without binning.
"""

from matplotlib import pyplot
import numpy

import adaptiveheatmap

data = numpy.random.randn(1000)
adaptiveheatmap.cumhist(data)
pyplot.show()
