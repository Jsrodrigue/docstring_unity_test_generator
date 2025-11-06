from examples.example import add, greet, multiply
import pytest


def test_greet_basic():
    assert greet("World") == "Hello, World!"


def test_greet_empty_string():
    assert greet("") == "Hello, !"


def test_add_integers():
    assert add(2, 3) == 5


def test_add_floats():
    assert add(2.5, 0.5) == 3.0


def test_add_mixed():
    assert add(1, 2.5) == 3.5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_multiply_two_numbers_default_c():
    assert multiply(2, 3) == 6


def test_multiply_three_numbers():
    assert multiply(2, 3, 4) == 24


def test_multiply_with_zero():
    assert multiply(0, 5) == 0


def test_multiply_negative_and_float():
    assert multiply(-2, 3.5) == -7.0