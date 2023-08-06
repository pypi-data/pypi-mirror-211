import math
import doctest
__version__ = "0.0.1"




class Calculator:
    """
    Welcome to  JustCalc, a simple calculator to support your mathematical needs.
    When creating an instance of this calculator, by default, the memory starts at 0.
    This calculator can perform Addition, Subtraction, Multiplication, Division, and Take the nth root of the current number in memory.
    Lastly, there is also a function to reset memory back to 0.
    The Calculator only accepts integers and floats as input.

    Usage:
    - Calculator().add(number) >>> Adds a number to the current memory value
    - Calculator().subtract(number) >>> Subtracts a number from the current memory value
    - Calculator().multiply(number) >>> Multiplies the current memory value by a number
    - Calculator().root(root) >>> Takes the nth root of the current memory value
    - Calculator().divide(number) >>> Divides the current memory value by a number
    - Calculator().current_memory() >>> Returns current value in memory
    - Calculator().reset_memory() >>> Resets the memory back to 0

    Example:
    >>> calc = Calculator()
    >>> calc.add(5)
    5
    >>> calc.subtract(2)
    3
    >>> calc.multiply(3)
    9
    >>> calc.divide(3)
    3.0
    >>> calc.root(2)
    1.7320508075688772
    >>> calc.current_memory()
    1.7320508075688772
    >>> calc.reset_memory()
    0
    """

    def __init__(self) -> None:
        """Instaiate our class and set our memory to 0"""
        self.memory : float = 0

    def check_number(self,number):
        """Checking if our input is valid int or floatq"""
        if not isinstance(number,(int,float)):
            raise TypeError('Input should be an integer or a float')


    def add(self,number: float) -> float:
        """Perform addition to current memory"""
        self.check_number(number)
        self.memory += number
        return self.memory


    def subtract(self,number: float) -> float:
        """Perform subtraction to current memory"""
        self.check_number(number)
        self.memory -= number
        return self.memory


    def multiply(self,number : float) -> float:
        """Perform multiplication to current memory"""
        self.check_number(number)
        self.memory *= number
        return self.memory

    def divide(self,number: float) -> float:
        """Perform division to current memory"""
        self.check_number(number)
        if number == 0 :
            raise ZeroDivisionError("Division by zero is not allowed")
        else:
            self.memory /= number
        return self.memory

    def root(self, root: float) -> float:
        """Taking the nth root of the current memory"""
        if not isinstance(root, (int, float)) or root <= 0:
            raise ValueError('Root should be a positive number')

        if self.memory < 0 and root % 2 != 0: # Checking if num is less than 0 and root is odd
            self.memory = -((-self.memory) ** (1/root)) # take the absolute value calculate nth root then convert back to negative
        else:
            self.memory = self.memory ** (1/root)
        return self.memory

    def current_memory(self):
        """Returns current memory value"""
        return self.memory

    def reset_memory(self):
        """Resets memory back to 0 """
        self.memory = 0
        return self.memory
