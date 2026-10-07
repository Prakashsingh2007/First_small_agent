def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a,b):
    return a-b

def multiple(a,b):
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
    "multiple" : multiple,
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
            "name": "multiple",
            "description": "multiple two numbers and return the result.",
            "parameters": {"a": "number", "b": "number"},
        },    
    {
            "name": "divide",
            "description": "divide two numbers and return the result.",
            "parameters": {"a": "number", "b": "number"},
        },
]

if __name__ == "__main__":
    print(TOOLS["add"](20, 30))
    print(TOOLS["subtract"](50,20))
    print(TOOLS["multiple"](50,0))
    print(TOOLS["divide"](50,20))

try:
    TOOLS["divide"](1, 0)
except ValueError as e:
    print("caught:", e)