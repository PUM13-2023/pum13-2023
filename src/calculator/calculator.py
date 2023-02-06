"""This module contains the Calculator class.

It is used to perform basic mathematical operations.
"""
from dataclasses import dataclass


@dataclass
class Calculator:
    """This is an example Calculator class.

    This class illustrates how documentation can be generated using
    sphinx.

    Args:
        result : The result of the operation is stored in this variable.
    """

    result: float

    def add(self, a: float, b: float) -> None:
        """Add two numbers together.

        args:
            a: First number.
            b: Second number.

        """
        self.result = a + b

    def subtract(self, a: float, b: float) -> None:
        """Subtracts two numbers.

        args:
            a: First number.
            b: Second number.

        """
        self.result = a - b

    def multiply(self, a: float, b: float) -> None:
        """Multiplies two numbers.

        args:
            a: First number.
            b: Second number.

        """
        self.result = a * b

    def divide(self, a: float, b: float) -> None:
        """Divides two numbers.

        Args:
            a: First number (dividend).
            b: Second number (divisor).

        Raises:
            ZeroDivisionError: If divisor is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Divisor cannot be zero")
        self.result = a / b
