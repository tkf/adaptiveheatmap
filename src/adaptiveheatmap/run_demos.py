from matplotlib import pyplot

from . import demos


def find_demos():
    for name, fun in vars(demos).items():
        if name.startswith('demo_'):
            yield fun


def run_all():
    for fun in find_demos():
        yield fun()


if __name__ == '__main__':
    ah_list = list(run_all())
    pyplot.show()
