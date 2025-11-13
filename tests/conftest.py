"""
Pytest configuration and compatibility fixes for the test suite.
"""
import inspect

# Monkey-patch inspect.getargspec for nose-parameterized compatibility
# nose-parameterized uses inspect.getargspec which was removed in Python 3.11
# This provides a compatibility shim
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec
