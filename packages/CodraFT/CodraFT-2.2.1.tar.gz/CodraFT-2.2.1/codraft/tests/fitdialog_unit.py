# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause or the CeCILL-B License
# (see codraft/__init__.py for details)

"""Curve fitting dialog test

Testing fit dialogs: Gaussian, Lorentzian, Voigt, etc.
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from codraft.core.computation.signal import peak_indexes
from codraft.core.io.signal import read_signal
from codraft.env import execenv
from codraft.tests.data import create_1d_gaussian, get_test_fnames
from codraft.utils.qthelpers import qt_app_context
from codraft.utils.tests import get_default_test_name
from codraft.widgets import fitdialog as fdlg

SHOW = True  # Show test in GUI-based test launcher


def test():
    """Test function"""
    with qt_app_context():

        # Multi-gaussian curve fitting test
        s = read_signal(get_test_fnames("paracetamol.txt")[0])
        peakidx = peak_indexes(s.y)
        execenv.print(
            fdlg.multigaussianfit(s.x, s.y, peakidx, name=get_default_test_name("00"))
        )

        # Gaussian curve fitting test
        size = 500
        x, y = create_1d_gaussian(size=size, noise_sigma=5.0)
        execenv.print(fdlg.gaussianfit(x, y))

        # Lorentzian curve fitting test
        execenv.print(fdlg.lorentzianfit(x, y))

        # Voigt curve fitting test
        execenv.print(fdlg.voigtfit(x, y))

        # Polynomial curve fitting test
        execenv.print(fdlg.polynomialfit(x, y, 4))


if __name__ == "__main__":
    test()
