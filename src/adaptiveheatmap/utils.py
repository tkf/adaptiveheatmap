from contextlib import contextmanager

import numpy
from matplotlib import pyplot


def finitevalues(data):
    """
    Filter out masked and non-normal values from `data`.
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
