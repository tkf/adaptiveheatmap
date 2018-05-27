import numpy
from matplotlib.mlab import bivariate_normal

from . import core


def data_hump_and_spike(N=100, hump_scale=10.0):
    X, Y = numpy.mgrid[-3:3:complex(0, N), -2:2:complex(0, N)]
    Z = bivariate_normal(X, Y, 0.1, 0.2, 1.0, 1.0) + \
        bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0) * hump_scale
    return X, Y, Z
# https://matplotlib.org/users/colormapnorms.html#logarithmic


def demo_contour(**kwargs):
    _, _, Z = data_hump_and_spike(**kwargs)
    ah = core.contour(Z)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    ah.figure.suptitle('contour')
    return ah


def demo_contourf(**kwargs):
    _, _, Z = data_hump_and_spike(**kwargs)
    ah = core.contourf(Z)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    ah.figure.suptitle('contourf')
    return ah


def demo_imshow(**kwargs):
    _, _, Z = data_hump_and_spike(**kwargs)
    ah = core.imshow(Z)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    ah.figure.suptitle('imshow')
    return ah


def demo_matshow(**kwargs):
    _, _, Z = data_hump_and_spike(**kwargs)
    ah = core.matshow(Z)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    ah.figure.suptitle('matshow')
    return ah


def demo_pcolor(**kwargs):
    X, Y, Z = data_hump_and_spike(**kwargs)
    ah = core.pcolor(X, Y, Z)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    ah.figure.suptitle('pcolor')
    return ah


def demo_pcolormesh(**kwargs):
    X, Y, Z = data_hump_and_spike(**kwargs)
    ah = core.pcolormesh(X, Y, Z)
    ah.set_xlabel('X')
    ah.set_ylabel('Y')
    ah.set_zlabel('Z')
    # ah.set_plabel('CDF')
    ah.figure.suptitle('pcolormesh')
    return ah
