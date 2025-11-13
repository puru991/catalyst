from six import PY2
import sys


if PY2:
    from ctypes import py_object, pythonapi

    mappingproxy = pythonapi.PyDictProxy_New
    mappingproxy.argtypes = [py_object]
    mappingproxy.restype = py_object

    def exc_clear():
        sys.exc_clear()

else:
    from types import MappingProxyType as mappingproxy

    def exc_clear():
        # exc_clear was removed in Python 3. The except statement automatically
        # clears the exception.
        pass


unicode = type(u'')

__all__ = [
    'mappingproxy',
    'unicode',
    'normalize_date',
    'iNaT',
]


# Pandas compatibility functions
import pandas as pd


def normalize_date(dt):
    """
    Normalize a datetime to midnight (00:00:00).

    This is a replacement for the removed pandas.tslib.normalize_date function.

    Parameters
    ----------
    dt : datetime-like
        The datetime to normalize

    Returns
    -------
    pd.Timestamp
        The normalized timestamp at midnight
    """
    if dt is None:
        return None
    if isinstance(dt, str):
        dt = pd.Timestamp(dt)
    elif not isinstance(dt, pd.Timestamp):
        dt = pd.Timestamp(dt)
    return dt.normalize()


# pandas.tslib.iNaT moved to pandas._libs.tslibs.nattype.iNaT
try:
    from pandas._libs.tslibs.nattype import iNaT
except ImportError:
    try:
        from pandas.tslib import iNaT  # type: ignore
    except (ImportError, AttributeError):
        # Fallback: use pandas NaT value
        iNaT = pd.NaT.value
