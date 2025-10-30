

def greet(name):
    """
    Return a greeting message for the given name.

    Args:
        name (str): The name to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"


def add(a, b):
    """
    Return the sum of two numbers.

    Args:
        a (float|int): The first number to add.
        b (float|int): The second number to add.

    Returns:
        float|int: The sum of a and b.
    """
    return a + b


def multiply(a, b, c=1):
    """
    Return the product of two or three numbers.
    
    Args:
        a (float | int): The first number to multiply.
        b (float | int): The second number to multiply.
        c (float | int, optional): The third number to multiply. Defaults to 1.
    
    Returns:
        float | int: The product of a, b, and c.
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
        Initialize a Rectangle.
        
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
        Scale the dimensions of the rectangle by a given factor.
        
        Args:
            factor (float): The scaling factor to apply to width and height.
        """
        self.width *= factor
        self.height *= factor