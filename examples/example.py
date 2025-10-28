def greet(name):
    """
    Return a greeting message for the given name.
    
    Args:
        name (str): The name to greet.
    
    Returns:
        str: A greeting message.
    """
    return f'Hello, {name}!'


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
    Return the product of three numbers.
    
    Args:
        a (float|int): The first number to multiply.
        b (float|int): The second number to multiply.
        c (float|int, optional): The third number to multiply, defaults to 1.
    """
    return a * b * c