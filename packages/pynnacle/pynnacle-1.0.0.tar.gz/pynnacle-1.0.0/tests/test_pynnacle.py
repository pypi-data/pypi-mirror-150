#!/usr/bin/env python3
"""Tests for package cookietest.py
To use tests either:
    1 - Use pip to install package as "editable"
            pip install -e .
    2 - Import pathmagic.py to enable tests to find the package
"""
# Third party modules
import pytest

# First party modules
from pynnacle import pynnacle


def test_fizzbuzz() -> None:
    result = pynnacle.fizzbuzz(10)
    assert result == [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz"]


def test_fibonacci() -> None:
    result = pynnacle.fibonacci(10)
    assert result == [1, 1, 2, 3, 5, 8]
