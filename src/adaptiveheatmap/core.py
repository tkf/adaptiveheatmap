import inspect
import warnings

from matplotlib import colors
from matplotlib import gridspec
from matplotlib import pyplot
from matplotlib.collections import QuadMesh
import numpy

from .utils import finitevalues, cumhist, undo_xylim


class QuantileNormalize(colors.Normalize):
    """
    Data normalization based on quantile function (inverse CDF).

    Attributes
    ----------
    qs : None, int or array
        If an int, `qs`-quantiles are used; i.e., it is converted to
        an array by ``qs = numpy.linspace(0, 1, qs + 1)``.
        If an array, it must be an increasing sequence of numbers
        between 0 and 1 (``qs * 100`` is passed to
        `numpy.nanpercentile`).  Note that usually `qs` should start
        at 0 (``qs[0] == 0``) and end at 1 (``qs[-1] == 1``) unless it
        is preferred to ignore extreme values.
    quantile : array
        Sorted values on the original data space.
    vmin, vmax : float
    clip : bool
        See: `matplotlib.colors.Normalize`.

    """

    def __init__(self, qs=None, quantile=None, **kwargs):
        self.quantile = quantile
        self.qs = qs
        colors.Normalize.__init__(self, **kwargs)

        if self.scaled():
            self._set_vmin_vmax()

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        data, is_scalar = self.process_value(value)

        self.autoscale_None(data)

        if clip:
            mask = numpy.ma.getmask(data)
            data = numpy.ma.array(numpy.clip(data.filled(self.vmax),
                                             self.vmin, self.vmax),
                                  mask=mask)
            # The above handling is copied from Normalize.__call__().
            # I have no idea the use-case and consequence of
            # clip=True; I couldn't find a good example in matplotlib
            # code.

        idx = numpy.searchsorted(self.quantile, data)
        result = idx / (len(self.quantile) - 1)
        result = numpy.ma.masked_array(result, numpy.ma.getmask(value))
        if is_scalar:
            result = result[0]
        return result
# https://matplotlib.org/users/colormapnorms.html

    def scaled(self):
        return self.quantile is not None

    def autoscale_None(self, data):
        if not self.scaled():
            self.autoscale(data)

    def autoscale(self, data):
        self._raw_data = data
        self.quantile = self._calc_quantile(data, self.qs,
                                            self.vmin, self.vmax)
        self._set_vmin_vmax()

    def _set_vmin_vmax(self):
        if self.vmin is None:
            self.vmin = self.quantile[0]
        if self.vmax is None:
            self.vmax = self.quantile[-1]

    @staticmethod
    def _calc_quantile(data, qs, vmin, vmax):
        if qs is None:
            qs = min(data.size, 100)
        if numpy.isscalar(qs):
            qs = numpy.linspace(0, 1, qs + 1)
            # "+ 1" so that each element is a multiple of `1/qs`.

        data = finitevalues(data)
        if vmin is not None:
            data = data[data >= vmin]
        if vmax is not None:
            data = data[data <= vmax]

        return numpy.nanpercentile(data, qs * 100)


class XYZQRelation(object):

    def __init__(self, ah):
        self.ah = ah

    def plot(self, x, y, marker='o', color='k', noline=False):
        self.lines = lines = []
        ah = self.ah
        z = ah.z_at(x, y)
        p = ah.norm(z)

        marker_kw = dict(
            marker=marker,
            color=color
        )

        lines.extend(ah.ax_main.plot(x, y, **marker_kw))
        lines.extend(ah.ax_cdf.plot(z, p, **marker_kw))
        if not noline:
            lines.append(ah.ax_cdf.axhline(p, color=color))
            lines.append(ah.ax_cdf.axvline(z, color=color))
            lines.append(ah.cax_quantile.axvline(z, color=color))
            lines.append(ah.cax_original.axhline(p, color=color))
        lines.append(ah.cax_quantile.plot(z, 0.5, **marker_kw))
        lines.append(ah.cax_original.plot(0.5, p, **marker_kw))

        return self

    def get_artists(self):
        return self.lines

    def remove(self):
        for art in self.get_artists():
            art.remove()


class AHEventHandler(object):

    def __init__(self, ah):
        self.ah = ah

    def connect(self):
        self.ah.figure.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        if event.inaxes is self.ah.ax_main:
            self.redraw_xyzq(event.xdata, event.ydata)

    def redraw_xyzq(self, x, y):
        try:
            xyzq = self.xyzq
        except AttributeError:
            pass
        else:
            xyzq.remove()

        try:
            self.xyzq = self.ah.relate_xyzq(x, y)
        except NotImplementedError:
            return

        self.ah.figure.canvas.draw()


class AdaptiveHeatmap(object):
    """
    Four-panel figure for visualizing heatmaps.

    Attributes
    ----------
    ax_main : `matplotlib.axes.Axes`
        Axes to plot the heatmap.
    ax_cdf : `matplotlib.axes.Axes`
        Axes to plot the cumulative distribution function (CDF).
    cax_quantile : `matplotlib.axes.Axes`
        Vertical colorbar along the cumulative distribution function
        (CDF) axis.
    cax_original : `matplotlib.axes.Axes`
        Horizontal colorbar in the original Z-space.
    figure : `matplotlib.figure.Figure`
    norm : `QuantileNormalize`

    """

    @classmethod
    def make(cls, cax_quantile_width_ratio=0.1, ax_cdf_width_ratio=0.5,
             cax_original_height_ratio=0.1,
             figure=None, **kwargs):
        """
        Create an `AdaptiveHeatmap` using `.GridSpec`.

        Parameters
        ----------
        cax_original_height_ratio : float
            The ratio of the height of `.cax_original` to `.ax_main`.
        cax_quantile_width_ratio : float
            The ratio of the width of `.cax_quantile` to `.ax_main`.
        ax_cdf_width_ratio : float
            The ratio of the width of `.ax_quantile` to `.ax_main`.

        """
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
        """
        Create an `AdaptiveHeatmap` from pre-existing axes.
        """
        self.ax_main = ax_main
        self.ax_cdf = ax_cdf
        self.cax_quantile = cax_quantile
        self.cax_original = cax_original
        self.figure = ax_main.figure
        self.gs = gs

        self.event_handler = AHEventHandler(self)
        self.event_handler.connect()

    def plot_main(self, name, *args, **kwargs):
        norm = kwargs.pop('norm', None)
        norm_kw = kwargs.pop('norm_kw', {})
        if norm is None:
            norm_kw = dict(norm_kw)
            for key in ('vmin', 'vmax'):
                if key in kwargs:
                    if key in norm_kw:
                        # Or maybe just ignore?
                        raise ValueError('{} passed as a keyword argument'
                                         ' but also exists in norm_kw')
                    # Should I pop?
                    norm_kw[key] = kwargs[key]
            norm = QuantileNormalize(**norm_kw)
        self.norm = norm

        f = getattr(self.ax_main, name)
        self.mappable = f(*args, norm=norm, **kwargs)
        return self.mappable

    @property
    def zdata(self):
        return self.norm._raw_data

    def plot_all(self, name, *args, **kwargs):
        self.plot_main(name, *args, **kwargs)
        self.plot_sub()
        return self.mappable

    def _make_fun(name):
        def f(self, *args, **kwargs):
            return self.plot_main(name, *args, **kwargs)
        f.__name__ = name
        f.__doc__ = """
        Run |Axes.{name}| with adaptive heatmap colorbar.

        .. |Axes.{name}| replace:: `Axes.{name} <matplotlib.axes.Axes.{name}>`

        Parameters
        ----------
        *args
        **kwargs
            All positional and keyword arguments are passed to
            |Axes.{name}| and use its default, except for the
            following keyword arguments.
        norm : QuantileNormalize
            Unlike |Axes.{name}|, `norm` here defaults to an instance of
            `QuantileNormalize` initialized with the data passed to this
            function.
        norm_kw : dict
            Keyword arguments passed to `QuantileNormalize`.

        Returns
        -------
        Whatever |Axes.{name}| returns.
        """.format(name=name)
        return f

    contour = _make_fun('contour')
    contourf = _make_fun('contourf')
    imshow = _make_fun('imshow')
    matshow = _make_fun('matshow')
    pcolor = _make_fun('pcolor')
    pcolormesh = _make_fun('pcolormesh')

    del _make_fun

    def plot_sub(self):
        self.plot_cdf()
        with undo_xylim(self.ax_cdf):
            self.colorbar_quantile()
            self.colorbar_original()

    def colorbar_quantile(self):
        zmin = numpy.nanmin(self.zdata)
        zmax = numpy.nanmax(self.zdata)
        gradient = self.norm(numpy.linspace(zmin, zmax, 256))
        gradient = numpy.vstack((gradient, gradient))
        self.cax_quantile.imshow(
            gradient, aspect='auto',
            extent=(zmin, zmax, 0, 1),  # left, right, bottom, top
            cmap=self.mappable.cmap,
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
            extent=(0, 1, 0, 1),  # left, right, bottom, top
            cmap=self.mappable.cmap,
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
        """ Set x-axis label of `.ax_main`. """
        self.ax_main.set_xlabel(label)

    def set_ylabel(self, label):
        """ Set y-axis label of `.ax_main`. """
        self.ax_main.set_ylabel(label)

    def set_zlabel(self, label):
        """ Set "z-axis" label of `.cax_quantile`. """
        self.cax_quantile.set_xlabel(label)

    def set_qlabel(self, label):
        """ Set "q-axis" label of `.ax_cdf`. """
        self.ax_cdf.set_ylabel(label)

    def z_at(self, x, y):
        zs = self.mappable.get_array()
        if zs.ndim == 2 and hasattr(self.mappable, 'get_extent'):
            nx, ny = zs.shape
            left, right, bottom, top = self.mappable.get_extent()
            ix = int((x - left) / (right - left) * (nx - 1))
            iy = int((x - bottom) / (top - bottom) * (ny - 1))
            return zs[ix, iy]
        elif isinstance(self.mappable, QuadMesh):
            coords = self.mappable._coordinates[1:, 1:, :]
            point = numpy.array([x, y]).reshape((1, 1, 2))
            i = abs(coords - point).sum(axis=-1).argmin()  # closest point
            # assert coords[:, :, 0].size == zs.size
            return zs[i]
            # h = self.mappable._meshHeight
            # w = self.mappable._meshWidth
            # zs.reshape(h, w)
            # # https://stackoverflow.com/a/34841871
        warnings.warn('z value from (x, y)-coordinate cannot be recovered'
                      ' from {}'.format(type(self.mappable)))
        raise NotImplementedError

    def relate_xyzq(self, *args, **kwargs):
        """
        Plot auxiliary lines and points to relate data at ``(x, y)``.
        """
        return XYZQRelation(self).plot(*args, **kwargs)

    try:
        relate_xyzq.__signature__ = inspect.signature(XYZQRelation.plot)
    except AttributeError:
        pass


def make_shortcut(name):
    def f(*args, **kwargs):
        ah_kw = kwargs.pop('ah_kw', {})
        ah = AdaptiveHeatmap.make(**ah_kw)
        ah.plot_all(name, *args, **kwargs)
        return ah
    f.__name__ = name
    f.__doc__ = """
    Adaptive heatmap version of |Axes.{name}|.

    Parameters
    ----------
    *args
    **kwargs
        All positional and keyword arguments are passed to |Axes.{name}|
        and use its default, except for the following keyword arguments.
    norm : QuantileNormalize
        Unlike |Axes.{name}|, `norm` here defaults to an instance of
        `QuantileNormalize` initialized with the data passed to this
        function.
    norm_kw : dict
        Keyword arguments passed to `QuantileNormalize`.
    ah_kw : dict
        Keyword arguments passed to `AdaptiveHeatmap.make`.

    Returns
    -------
    ah : AdaptiveHeatmap
        `ah.mappable` holds whatever |Axes.{name}| returns.

    Examples
    --------
    .. include:: backreferences/adaptiveheatmap.{name}.examples
    .. raw:: html

        <div style='clear:both'></div>

    """.format(name=name)
    return f


# Shortcuts:
contour = make_shortcut('contour')
contourf = make_shortcut('contourf')
imshow = make_shortcut('imshow')
matshow = make_shortcut('matshow')
pcolor = make_shortcut('pcolor')
pcolormesh = make_shortcut('pcolormesh')
