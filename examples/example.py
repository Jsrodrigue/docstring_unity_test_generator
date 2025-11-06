
def greet(name):
  """
  Greets a person by name.
  
  Args:
    name (str): The name of the person to greet.
  Returns:
    str: A greeting message.
  """
  return f"Hello, {name}!"


def add(a, b):
    """
    Return the sum of two numbers.
    
    Args:
      a (int or float): The first number.
      b (int or float): The second number.
    Returns:
      int or float: The sum of the two numbers.
    """
    return a + b


def multiply(a, b, c=1):
    """
    Multiply three numbers together, with the third number being optional and defaulting to 1.
    
    Args:
      a (int or float): The first number.
      b (int or float): The second number.
      c (int or float, optional): The third number, default is 1.
    Returns:
      int or float: The product of the three numbers.
    """
    return a * b * c


class Rectangle:
    """
    Represents a rectangle with a given width and height.
    
    This class provides methods to calculate the area and perimeter of the rectangle, as well as a method to scale its dimensions.
    
    Attributes:
      width (float): The width of the rectangle.
      height (float): The height of the rectangle.
    """
    def __init__(self, width: float, height: float):
      
        """
        Initialize a new Rectangle instance with the specified width and height.
        
        Args:
          width (float): The width of the rectangle.
          height (float): The height of the rectangle.
        """
        self.width = width
        self.height = height

    def area(self) -> float:
        """
        Calculate the area of the rectangle.
        
        Returns:
          float: The area of the rectangle (width multiplied by height).
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
        Scale the rectangle's dimensions by the given factor.
        
        Args:
          factor (float): The factor to scale the rectangle's dimensions by.
        """
        self.width *= factor
        self.height *= factor