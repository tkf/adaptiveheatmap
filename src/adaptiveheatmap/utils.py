from contextlib import contextmanager

import numpy
from matplotlib import pyplot


def finitevalues(data):
    """
    Filter out masked and non-normal values from `data`.

    Parameters
    ----------
    data : array-like
        Arbitrary-dimensional array-like container with numerical values.

    Returns
    -------
    array : numpy.ndarray
        One dimensional array filled with finite values in `data`.

    Examples
    --------
    >>> finitevalues([1, numpy.nan, 2, 3])
    array([1., 2., 3.])
    >>> finitevalues(numpy.ma.MaskedArray([
    ...     [1, numpy.nan, 2, 3],
    ...     [-numpy.inf, 4, numpy.inf, numpy.inf],
    ... ], [
    ...     [1, 0, 0, 1],
    ...     [1, 0, 1, 0],
    ... ]))
    array([1., 2., 3., 4.])

    """
    data = numpy.asarray(data)
    if numpy.ma.is_masked(data):
        data = data.data[~data.mask]
    data = numpy.ma.getdata(data)  # may still be a MaskedArray
    return data[numpy.isfinite(data)]


def cdf(data, normed=True):
    """
    Calculate cumulative distribution function from `data`.
    """
    xs = numpy.sort(finitevalues(data))

    if normed:
        ys = numpy.linspace(1/len(xs), 1, len(xs))
    else:
        ys = numpy.arange(1, len(xs))
    return xs, ys


def cumhist(data, normed=True, ylabel=None, ax=None,
            **step_kwargs):
    """
    Plot cumulative distribution of `data`.

    See also `.cdf`.

    .. include:: backreferences/adaptiveheatmap.cumhist.examples
    .. raw:: html

        <div style='clear:both'></div>
    """
    if ax is None:
        ax = pyplot.gca()
    if ylabel is None:
        if normed:
            ylabel = 'Cumulative Probability'
        else:
            ylabel = 'Cumulative Count'

    xs, ys = cdf(data, normed=normed)
    lines = ax.step(xs, ys, **step_kwargs)
    ax.set_ylabel(ylabel)
    return lines


@contextmanager
def undo_xylim(ax):
    xilm = ax.get_xlim()
    ylim = ax.get_ylim()
    yield
    ax.set_xlim(xilm)
    ax.set_ylim(ylim)
