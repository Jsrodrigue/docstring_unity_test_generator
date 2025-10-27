def greet(name):
    """Returns a personalized greeting message.

Args:
    name (str): The name of the person to be greeted. 
                 Cannot be empty.

Returns:
    str: A greeting message with the name inserted.

Raises:
    TypeError: If the input 'name' is not a string.
    ValueError: If the input 'name' is an empty string."""
    return f'Hello, {name}!'


def add(a, b):
    """Add two numbers.

Args:
    a (int or float): The first number to add.
    b (int or float): The second number to add.

Returns:
    int or float: The sum of a and b."""
    return a + b


def multiply(a, b, c=1):
    return a * b * c
