from calculator import Calculator
import pytest

def test_addition():
    calc = Calculator()

    # Testing addition
    assert calc.add(2) == 2
    assert calc.add(3) == 5

def test_subtraction():
    calc = Calculator()

    # Testing Subtraction
    assert calc.subtract(10) == -10
    assert calc.subtract(3) == -13

def test_multiplication():
    calc = Calculator()
    calc.add(1)

    # Testing multiplication
    assert calc.multiply(2) == 2
    assert calc.multiply(5) == 10


def test_division():
    calc = Calculator()
    calc.add(20)

    # Testing Division
    assert calc.divide(2) == 10
    assert calc.divide(5) == 2

    with pytest.raises(ZeroDivisionError):
        calc.divide(0)

def test_root():
    calc = Calculator()
    calc.add(36)

    # Testing root
    assert calc.root(2) == 6

    calc.reset_memory()
    calc.add(-8)
    assert calc.root(3) == -2

    with pytest.raises(ValueError):
        calc.root(0)

def test_reset_memory():
    calc = Calculator()
    calc.add(5)
    calc.multiply(2)

    # Testing reset_memory
    assert calc.reset_memory() == 0
    assert calc.memory == 0

def test_invalid_input():
    calc = Calculator()

    # Testing invalid input
    with pytest.raises(TypeError):
        calc.add('string')
    with pytest.raises(TypeError):
        calc.subtract('string')
    with pytest.raises(TypeError):
        calc.multiply('string')
    with pytest.raises(TypeError):
        calc.divide('string')
