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
    'information_ratio',
]


# Pandas compatibility functions
import pandas as pd
import numpy as np


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


# Empyrical compatibility - information_ratio was removed in empyrical-reloaded
def information_ratio(returns, factor_returns):
    """
    Calculate the information ratio (IR) of a strategy.

    The information ratio is the annualized excess return divided by the
    tracking error (standard deviation of excess returns).

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Daily returns of the strategy
    factor_returns : pd.Series or np.ndarray
        Daily returns of the benchmark/factor

    Returns
    -------
    float
        The information ratio
    """
    if len(returns) == 0 or len(factor_returns) == 0:
        return np.nan

    # Calculate excess returns
    excess_returns = np.asarray(returns) - np.asarray(factor_returns)

    # Tracking error (std of excess returns)
    tracking_error = np.std(excess_returns, ddof=1)

    if tracking_error == 0 or np.isnan(tracking_error):
        return np.nan

    # Annualized excess return / tracking error
    # Assuming daily returns, annualize with sqrt(252)
    mean_excess = np.mean(excess_returns)
    annualized_excess = mean_excess * 252
    annualized_tracking_error = tracking_error * np.sqrt(252)

    return annualized_excess / annualized_tracking_error
