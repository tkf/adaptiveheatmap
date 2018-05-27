"""
Installed modules used for building this documentation
------------------------------------------------------

This script is for recording Python packages and their version for
creating plots.

The filename starts with ``plot_`` for tricking Sphinx-Gallery to
execute it, even though it's not plotting anything.
"""

from __future__ import print_function

import sys
import subprocess

output = subprocess.check_output(
    [sys.executable, '-m', 'pip', 'freeze'],
    universal_newlines=True,
)
print(output, end='')
