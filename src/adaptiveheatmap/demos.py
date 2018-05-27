import numpy
from matplotlib.mlab import bivariate_normal

from .core import pcolormesh, imshow


def demo_pcolormesh():
    N = 100
    X, Y = numpy.mgrid[-3:3:complex(0, N), -2:2:complex(0, N)]
    Z1 = bivariate_normal(X, Y, 0.1, 0.2, 1.0, 1.0) +  \
        0.1 * bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    # https://matplotlib.org/users/colormapnorms.html

    ah = pcolormesh(X, Y, Z1)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    # ah.set_plabel('CDF')

    return ah


def demo_imshow():
    ah = imshow(numpy.exp(numpy.random.random((100, 100))))
    return ah
