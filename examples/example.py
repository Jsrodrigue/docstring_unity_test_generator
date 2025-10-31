
import pandas 

def greet(name):
    """
    Generate a greeting message for a given name.
    
    Args:
      name (str): The name of the person to greet.
    Returns:
      str: A greeting message including the provided name.
    """
    return f"Hello, {name}!"


def add(a, b):
    """
    Return the sum of two numbers.
    
    Args:
      a: The first number.
      b: The second number.
    Returns:
      int or float: The sum of a and b.
    """
    return a + b


def multiply(a, b, c=1):
    """
    Return the product of three numbers, with an optional third number.
    
    Args:
      a: The first number.
      b: The second number.
      c (int or float, optional): The third number. Defaults to 1.
    Returns:
      int or float: The product of a, b, and c.
    """
    return a * b * c


class Rectangle:
    """
    Represents a rectangle defined by its width and height.
    
    Attributes:
      width (float): Width of the rectangle.
      height (float): Height of the rectangle.
    """
    def __init__(self, width: float, height: float):
        """
        Initialize a Rectangle instance.
        
        Args:
          width (float): Width of the rectangle.
          height (float): Height of the rectangle.
        """
        self.width = width
        self.height = height

    def area(self) -> float:
        """
        Calculate the area of the rectangle.
        
        Returns:
          float: The area of the rectangle.
        """
        return self.width * self.height

    def perimeter(self) -> float:
        """
        Calculate the perimeter of the rectangle.
        
        Returns:
          float: The perimeter of the rectangle.
        """
        return 2 * (self.width + self.height)

    def scale(self, factor: float):
        """
        Scale the rectangle by a given factor.
        
        Args:
          factor (float): The factor to scale the rectangle by.
        """
        self.width *= factor
        self.height *= factor