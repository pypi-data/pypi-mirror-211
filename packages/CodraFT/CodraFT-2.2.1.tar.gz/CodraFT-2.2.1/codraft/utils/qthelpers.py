# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause or the CeCILL-B License
# (see codraft/__init__.py for details)

"""
CodraFT Qt utilities
"""

import faulthandler
import functools
import logging
import os
import os.path as osp
import shutil
import sys
import time
import traceback
from contextlib import contextmanager
from datetime import datetime

import guidata
from guidata.configtools import get_module_data_path
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from codraft.config import APP_NAME, DATETIME_FORMAT, Conf, _, get_old_log_fname
from codraft.env import execenv
from codraft.utils.misc import to_string


def close_widgets_and_quit(screenshot=False):
    """Close Qt top level widgets and quit Qt event loop"""
    for widget in QW.QApplication.instance().topLevelWidgets():
        wname = widget.objectName()
        if screenshot and wname and widget.isVisible():  # pragma: no cover
            grab_save_window(widget, wname.lower())
        assert widget.close()
    QW.QApplication.instance().quit()


QAPP_INSTANCE = None


def get_log_contents(fname):
    """Return True if file exists and something was logged in it"""
    if osp.exists(fname):
        with open(fname, "rb") as fdesc:
            return to_string(fdesc.read()).strip()
    return None


def initialize_log_file(fname):
    """Eventually keep the previous log file
    Returns True if there was a previous log file"""
    contents = get_log_contents(fname)
    if contents:
        try:
            shutil.move(fname, get_old_log_fname(fname))
        except Exception:  # pylint: disable=broad-except
            pass
        return True
    return False


def remove_empty_log_file(fname):
    """Eventually remove empty log files"""
    if not get_log_contents(fname):
        try:
            os.remove(fname)
        except Exception:  # pylint: disable=broad-except
            pass


@contextmanager
def qt_app_context(exec_loop=False, enable_logs=True):
    """Context manager handling Qt application creation and persistance"""
    global QAPP_INSTANCE  # pylint: disable=global-statement
    if QAPP_INSTANCE is None:
        QAPP_INSTANCE = guidata.qapplication()

    if enable_logs:
        # === Create a logger for standard exceptions ----------------------------------
        tb_log_fname = Conf.main.traceback_log_path.get()
        Conf.main.traceback_log_available.set(initialize_log_file(tb_log_fname))
        logger = logging.getLogger(__name__)
        fmt = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
        logging.basicConfig(
            filename=tb_log_fname,
            filemode="w",
            level=logging.CRITICAL,
            format=fmt,
            datefmt=DATETIME_FORMAT,
        )

        def custom_excepthook(exc_type, exc_value, exc_traceback):
            "Custom exception hook"
            logger.critical(
                "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
            )
            return sys.__excepthook__(exc_type, exc_value, exc_traceback)

        sys.excepthook = custom_excepthook

    # === Use faulthandler for other exceptions ------------------------------------
    fh_log_fname = Conf.main.faulthandler_log_path.get()
    Conf.main.faulthandler_log_available.set(initialize_log_file(fh_log_fname))

    with open(fh_log_fname, "w", encoding="utf-8") as fh_log_fn:
        if enable_logs and Conf.main.faulthandler_enabled.get(True):
            faulthandler.enable(file=fh_log_fn)
        try:
            yield QAPP_INSTANCE
        finally:
            if execenv.unattended:  # pragma: no cover
                if execenv.delay > 0:
                    mode = "Screenshot" if execenv.screenshot else "Unattended"
                    message = f"{mode} mode (delay: {execenv.delay}s)"
                    msec = execenv.delay * 1000 - 200
                    for widget in QW.QApplication.instance().topLevelWidgets():
                        if isinstance(widget, QW.QMainWindow):
                            widget.statusBar().showMessage(message, msec)
                QC.QTimer.singleShot(
                    execenv.delay * 1000,
                    lambda: close_widgets_and_quit(screenshot=execenv.screenshot),
                )
            if exec_loop:
                QAPP_INSTANCE.exec()

    if enable_logs and Conf.main.faulthandler_enabled.get():
        faulthandler.disable()
    remove_empty_log_file(fh_log_fname)
    if enable_logs:
        logging.shutdown()
        remove_empty_log_file(tb_log_fname)


def close_dialog_and_quit(widget, screenshot=False):
    """Close QDialog and quit Qt event loop"""
    wname = widget.objectName()
    if screenshot and wname and widget.isVisible():  # pragma: no cover
        grab_save_window(widget, wname.lower())
    widget.done(QW.QDialog.Accepted)
    # QW.QApplication.instance().quit()


def exec_dialog(dlg):
    """Run QDialog Qt execution loop without blocking,
    depending on environment test mode"""
    if execenv.unattended:
        QC.QTimer.singleShot(
            execenv.delay * 1000,
            lambda: close_dialog_and_quit(dlg, screenshot=execenv.screenshot),
        )
    return dlg.exec()


def qt_wait(timeout, except_unattended=False):  # pragma: no cover
    """Freeze GUI during timeout (seconds) while processing Qt events"""
    if except_unattended and execenv.unattended:
        return
    start = time.time()
    while time.time() <= start + timeout:
        time.sleep(0.01)
        QW.QApplication.processEvents()


@contextmanager
def create_progress_bar(parent, label, max_):
    """Create modal progress bar"""
    prog = QW.QProgressDialog(label, _("Cancel"), 0, max_, parent, QC.Qt.SplashScreen)
    prog.setWindowModality(QC.Qt.WindowModal)
    prog.show()
    QW.QApplication.processEvents()
    try:
        yield prog
    finally:
        prog.close()


def qt_handle_error_message(widget, message):
    """Handles application (QWidget) error message"""
    traceback.print_exc()
    txt = str(message)
    msglines = txt.splitlines()
    if len(msglines) > 10:
        txt = os.linesep.join(msglines[:10] + ["..."])
    title = widget.window().objectName()
    QW.QMessageBox.critical(widget, title, _("Error:") + f"\n{txt}")


def qt_try_except(message=None):
    """Try...except Qt widget method decorator"""

    def qt_try_except_decorator(func):
        """Try...except Qt widget method decorator"""

        @functools.wraps(func)
        def method_wrapper(*args, **kwargs):
            """Decorator wrapper function"""
            self = args[0]  # extracting 'self' from method arguments
            #  If "self" is a BaseProcessor, then we need to get the panel instance
            panel = getattr(self, "panel", self)
            if message is not None:
                panel.SIG_STATUS_MESSAGE.emit(message)
                QW.QApplication.setOverrideCursor(QG.QCursor(QC.Qt.WaitCursor))
                panel.repaint()
            output = None
            try:
                output = func(*args, **kwargs)
            except Exception as msg:  # pylint: disable=broad-except
                qt_handle_error_message(panel.parent(), msg)
            finally:
                panel.SIG_STATUS_MESSAGE.emit("")
                QW.QApplication.restoreOverrideCursor()
            return output

        return method_wrapper

    return qt_try_except_decorator


@contextmanager
def qt_try_loadsave_file(widget: QW.QWidget, filename: str, operation: str):
    """Try and open file (operation: "load" or "save")"""
    if operation == "load":
        text = _("%s could not be opened:")
    elif operation == "save":
        text = _("%s could not be written:")
    else:
        raise ValueError("operation argument must be 'load' or 'save'")
    try:
        yield filename
    except Exception as msg:  # pylint: disable=broad-except
        traceback.print_exc()
        message = (text % osp.basename(filename)) + "\n" + str(msg)
        QW.QMessageBox.critical(widget, APP_NAME, message)
    finally:
        pass


SHOTPATH = osp.join(
    get_module_data_path("codraft"), os.pardir, "doc", "images", "shots"
)


def grab_save_window(widget: QW.QWidget, name: str) -> None:  # pragma: no cover
    """Grab window screenshot and save it"""
    widget.activateWindow()
    widget.raise_()
    QW.QApplication.processEvents()
    pixmap = widget.grab()
    suffix = ""
    if not name[-1].isdigit() and not name.startswith(("s_", "i_")):
        suffix = "_" + datetime.now().strftime("%Y-%m-%d-%H%M%S")
    pixmap.save(osp.join(SHOTPATH, f"{name}{suffix}.png"))


@contextmanager
def save_restore_stds():
    """Save/restore standard I/O before/after doing some things
    (e.g. calling Qt open/save dialogs)"""
    saved_in, saved_out, saved_err = sys.stdin, sys.stdout, sys.stderr
    sys.stdout = None
    try:
        yield
    finally:
        sys.stdin, sys.stdout, sys.stderr = saved_in, saved_out, saved_err


@contextmanager
def block_signals(widget: QW.QWidget, enable: bool):
    """Eventually block/unblock widget Qt signals before/after doing some things
    (enable: True if feature is enabled)"""
    if enable:
        widget.blockSignals(True)
    try:
        yield
    finally:
        if enable:
            widget.blockSignals(False)
