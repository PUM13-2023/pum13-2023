import pytest

from calculator.calculator import Calculator


def test_addition() -> None:
    calculator = Calculator(result=0.0)
    calculator.add(2, 3)
    assert calculator.result == 5


def test_subtraction() -> None:
    calculator = Calculator(result=0.0)
    calculator.subtract(5, 2)
    assert calculator.result == 3


def test_multiplication() -> None:
    calculator = Calculator(result=0.0)
    calculator.multiply(5, 2)
    assert calculator.result == 10


def test_division() -> None:
    calculator = Calculator(result=0.0)
    calculator.divide(8, 4)
    assert calculator.result == 2


def test_divide_by_zero() -> None:
    calculator = Calculator(result=0.0)
    with pytest.raises(ZeroDivisionError):
        calculator.divide(8, 0)
