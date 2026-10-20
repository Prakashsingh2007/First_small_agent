def check_numbers(a, b):
    """Raise TypeError unless both a and b are real numbers."""
    for value in (a, b):
        # bool is a subclass of int in Python, so reject it explicitly
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Expected a number, got {value!r} ({type(value).__name__})")


def add(a, b):
    """Return the sum of a and b."""
    check_numbers(a, b)
    return a + b


def subtract(a, b):
    """Return a minus b."""
    check_numbers(a, b)
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    check_numbers(a, b)
    return a * b


def divide(a, b):
    """Return a divided by b."""
    check_numbers(a, b)
    if b == 0:
        raise ValueError("Division by zero")
    return a / b


TOOLS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}

TOOL_DESCRIPTIONS = [
    {
        "name": "add",
        "description": "Add two numbers and return the sum.",
        "parameters": {"a": "number", "b": "number"},
    },
    {
        "name": "subtract",
        "description": "Subtract two numbers and return the result.",
        "parameters": {"a": "number", "b": "number"},
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers and return the product.",
        "parameters": {"a": "number", "b": "number"},
    },
    {
        "name": "divide",
        "description": "Divide two numbers and return the quotient.",
        "parameters": {"a": "number", "b": "number"},
    },
]