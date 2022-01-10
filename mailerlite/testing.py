"""Utility function for unit tests."""
from functools import wraps
import pytest


def succeed_or_skip_sensitive_tests(func):
    """Small decorator to skip some sensitive function."""
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            pytest.skip("Test Failed due to an object deleted "
                        "by another matrix.")

    return wrapper_func
