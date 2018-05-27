import pytest

from ..run_demos import find_demos


@pytest.mark.parametrize('demo', list(find_demos()))
def test_smoke(demo):
    demo()
