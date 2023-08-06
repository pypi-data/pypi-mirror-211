# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause or the CeCILL-B License
# (see codraft/__init__.py for details)

"""
CodraFT Miscelleneous utilities
"""

import numpy as np


def to_string(obj):
    """Convert to string, trying utf-8 then latin-1 codec"""
    if isinstance(obj, bytes):
        try:
            return obj.decode()
        except UnicodeDecodeError:
            return obj.decode("latin-1")
    try:
        return str(obj)
    except UnicodeDecodeError:
        return str(obj, encoding="latin-1")


def is_integer_dtype(dtype):
    """Return True if data type is an integer type"""
    return issubclass(np.dtype(dtype).type, np.integer)


def is_complex_dtype(dtype):
    """Return True if data type is a complex type"""
    return issubclass(np.dtype(dtype).type, complex)
