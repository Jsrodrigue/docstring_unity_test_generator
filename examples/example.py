def greet(name):

    """
    Return a friendly greeting for the given name.
    
    Args:
        name (str): The name of the person to greet.
    
    Returns:
        str: A greeting message containing the given name.
    """

    return f'Hello, {name}!'


def add(a, b):

    """
    Return the sum of two numeric values.
    
    Args:
        a (int, float): The first value to add.
        b (int, float): The second value to add.
    
    Returns:
        int, float: The sum of a and b.
    """

    return a + b


def multiply(a, b, c=1):

    """
    Return the product of two or three numeric values.
    
    Args:
        a (int, float): The first multiplier.
        b (int, float): The second multiplier.
        c (int, float, optional): The optional third multiplier. Defaults to 1.
    
    Returns:
        int, float: The product of a, b, and c.
    """

    return a * b * c