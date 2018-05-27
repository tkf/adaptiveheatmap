from matplotlib import colors
from matplotlib import gridspec
from matplotlib import pyplot
import numpy


class QuantileNormalize(colors.Normalize):

    @classmethod
    def from_data(cls, data, qs=None, **kwargs):
        if qs is None:
            qs = min(data.size, 100)
        if numpy.isscalar(qs):
            qs = numpy.linspace(0, 1, qs)
        quantile = numpy.nanpercentile(data, qs * 100)
        return cls(quantile, **kwargs)

    def __init__(self, quantile, clip=False):
        self.quantile = quantile
        vmin = quantile[0]
        vmax = quantile[-1]
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        idx = numpy.searchsorted(self.quantile, value)
        return numpy.ma.masked_array(idx / (len(self.quantile) - 1))
# https://matplotlib.org/users/colormapnorms.html


def cumhist(data, normed=True, ylabel=None, ax=None,
            **step_kwargs):
    """
    Plot cumulative distribution of `data`.

    .. plot::
       :include-source:

       cumhist(numpy.random.randn(1000))

    """
    if ax is None:
        ax = pyplot.gca()
    if ylabel is None:
        if normed:
            ylabel = 'Cumulative Probability'
        else:
            ylabel = 'Cumulative Count'
    if normed:
        ys = numpy.linspace(1/len(data), 1, len(data))
    else:
        ys = numpy.arange(1, len(data))

    data = numpy.sort(data)
    lines = ax.step(data, ys, **step_kwargs)
    ax.set_ylabel(ylabel)
    return lines


class AdaptiveHeatmap(object):

    @classmethod
    def make(cls, cax_quantile_width_ratio=0.1, ax_cdf_width_ratio=0.5,
             cax_original_height_ratio=0.1,
             figure=None, **kwargs):
        gs = gridspec.GridSpec(
            2, 3,
            height_ratios=[1, cax_original_height_ratio],
            width_ratios=[1, cax_quantile_width_ratio, ax_cdf_width_ratio])
        if figure is None:
            figure = pyplot.figure()

        cax_kw = dict(
            facecolor=(1, 1, 1, 0),  # transparent white
        )

        ax_main = figure.add_subplot(gs[0, 0])
        ax_cdf = figure.add_subplot(gs[0, 2])
        cax_quantile = figure.add_subplot(gs[1, 2], sharex=ax_cdf, **cax_kw)
        cax_original = figure.add_subplot(gs[0, 1], sharey=ax_cdf, **cax_kw)

        return cls(ax_main, ax_cdf, cax_quantile, cax_original,
                   gs=gs)

    def __init__(self, ax_main, ax_cdf, cax_quantile, cax_original,
                 gs=None):
        self.ax_main = ax_main
        self.ax_cdf = ax_cdf
        self.cax_quantile = cax_quantile
        self.cax_original = cax_original
        self.figure = ax_main.figure
        self.gs = gs

    def get_zdata(self, name, args):
        return args[-1].flatten()
        # return self.mappable.get_array().flatten()
    # TODO: check if is it correct always

    def plot_main(self, name, *args, **kwargs):
        self.zdata = self.get_zdata(name, args)
        self.quantile_norm = QuantileNormalize.from_data(self.zdata)
        f = getattr(self.ax_main, name)
        self.mappable = f(*args, norm=self.quantile_norm, **kwargs)
        return self.mappable

    def plot_all(self, name, *args, **kwargs):
        self.plot_main(name, *args, **kwargs)
        self.plot_sub()
        return self.mappable

    def _make_fun(self, name):
        def f(*args, **kwargs):
            return self.plot_main(name, *args, **kwargs)
        return f

    pcolormesh = property(lambda self: self._make_fun('pcolormesh'))
    pcolor = property(lambda self: self._make_fun('pcolor'))
    imshow = property(lambda self: self._make_fun('imshow'))
    matshow = property(lambda self: self._make_fun('matshow'))
    contour = property(lambda self: self._make_fun('contour'))
    contourf = property(lambda self: self._make_fun('contourf'))

    def plot_sub(self):
        self.colorbar_quantile()
        self.colorbar_original()
        self.plot_cdf()

    def colorbar_quantile(self):
        zmin = self.zdata.min()
        zmax = self.zdata.max()
        gradient = self.quantile_norm(numpy.linspace(0, 1, 256))
        gradient = numpy.vstack((gradient, gradient))
        self.cax_quantile.imshow(
            gradient, aspect='auto',
            extent=(zmin, zmax, 0, 1)  # left, right, bottom, top
        )
        self.cax_quantile.set_yticks([])  # no yticks
        # self.figure.colorbar(
        #     self.mappable, self.cax_quantile,
        #     orientation='horizontal',
        # )

    def colorbar_original(self):
        gradient = numpy.linspace(1, 0, 256)
        gradient = numpy.vstack((gradient, gradient)).T
        self.cax_original.imshow(
            gradient, aspect='auto',
            extent=(0, 1, 0, 1)  # left, right, bottom, top
        )

        self.cax_original.set_xticks([])  # no xticks

        # Hide y tick labels but keep ticks:
        self.cax_original.tick_params(labelleft=False)
        # self.cax_original.yaxis.set_visible(False)  # hide yticks
# https://matplotlib.org/examples/color/colormaps_reference.html

    def plot_cdf(self):
        cumhist(self.zdata, ax=self.ax_cdf)

        self.ax_cdf.yaxis.tick_right()
        self.ax_cdf.yaxis.set_label_position('right')

        # Hide x tick labels but keep ticks:
        self.ax_cdf.tick_params(labelbottom=False)
# https://stackoverflow.com/a/26428792
# https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html

    def set_xlabel(self, label):
        self.ax_main.set_xlabel(label)

    def set_ylabel(self, label):
        self.ax_main.set_ylabel(label)

    def set_zlabel(self, label):
        self.cax_quantile.set_xlabel(label)

    def set_plabel(self, label):
        self.ax_cdf.set_ylabel(label)


def make_shortcut(name):
    def f(*args, **kwargs):
        ah = AdaptiveHeatmap.make()
        ah.plot_all(name, *args, **kwargs)
        return ah
    f.__name__ = name
    return f


pcolormesh = make_shortcut('pcolormesh')
pcolor = make_shortcut('pcolor')
imshow = make_shortcut('imshow')
matshow = make_shortcut('matshow')
contour = make_shortcut('contour')
contourf = make_shortcut('contourf')
