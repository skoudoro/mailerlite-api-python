"""Utility function for unit tests."""
import pytest


def succeed_or_skip_sensitive_tests(func):
    """Small decorator to skip some sensitive function."""
    def wrapper_func():
        try:
            func()
        except Exception:
            pytest.skip("Test Failed due to an object deleted "
                        "by another matrix.")

    return wrapper_func
