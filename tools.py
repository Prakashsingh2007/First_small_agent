def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a,b):
    return a-b

def multiply(a,b):
    if(a == 0 or b == 0):
        return 0
    else:
        return a*b

def divide(a,b):
    if(b == 0):
        raise ValueError("Division by zero")
    else:
        return a/b

TOOLS ={
    "add": add,
    "subtract" : subtract,
    "multiply" : multiply,
    "divide" : divide,
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
            "description": "multiply two numbers and return the result.",
            "parameters": {"a": "number", "b": "number"},
        },    
    {
            "name": "divide",
            "description": "divide two numbers and return the result.",
            "parameters": {"a": "number", "b": "number"},
        },
]
