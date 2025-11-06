import pytest
from examples.example import greet, add, multiply, Rectangle

def test_greet():
    assert greet('Alice') == 'Hello, Alice!'
    assert greet('Bob') == 'Hello, Bob!'
    assert greet('') == 'Hello, !'

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(1.5, 2.5) == 4.0
    assert add(0, 0) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(2, 3, 2) == 12
    assert multiply(1, 0) == 0
    assert multiply(5, 5) == 25

def test_rectangle():
    rect = Rectangle(3, 4)
    assert rect.area() == 12
    assert rect.perimeter() == 14
    rect.scale(2)
    assert rect.width == 6
    assert rect.height == 8
    assert rect.area() == 48