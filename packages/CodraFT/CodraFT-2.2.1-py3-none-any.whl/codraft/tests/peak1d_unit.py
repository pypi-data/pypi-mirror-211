# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause or the CeCILL-B License
# (see codraft/__init__.py for details)

"""
Signal peak detection test

Testing peak detection dialog box.
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...


from codraft.core.io.signal import read_signal
from codraft.env import execenv
from codraft.utils.qthelpers import exec_dialog, qt_app_context
from codraft.utils.tests import get_test_fnames
from codraft.widgets.signalpeakdialog import SignalPeakDetectionDialog

SHOW = True  # Show test in GUI-based test launcher


def test():
    """Signal peak dialog test"""
    with qt_app_context():
        s = read_signal(get_test_fnames("paracetamol.txt")[0])
        dlg = SignalPeakDetectionDialog()
        dlg.resize(640, 300)
        dlg.setup_data(s.x, s.y)
        plot = dlg.get_plot()
        plot.set_axis_limits(plot.xBottom, 16, 30)
        dlg.setObjectName(dlg.objectName() + "_00")  # to avoid timestamp suffix
        exec_dialog(dlg)
    execenv.print("peaks:")
    execenv.pprint(dlg.get_peaks())
    execenv.pprint(dlg.get_min_dist())


if __name__ == "__main__":
    test()
