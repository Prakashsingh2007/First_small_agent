from tools import add, subtract, multiply, divide, TOOLS


def raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


# normal values
assert add(20, 30) == 50
assert subtract(50, 20) == 30
assert multiply(4, 5) == 20
assert divide(50, 20) == 2.5

# negatives and floats
assert add(-2, -3) == -5
assert multiply(-2, 3) == -6
assert add(0.5, 0.25) == 0.75

# multiply by zero
assert multiply(50, 0) == 0

# divide by zero
assert raises(ValueError, divide, 1, 0)

# bad types: strings, None, booleans
assert raises(TypeError, add, "2", 3)
assert raises(TypeError, add, None, 3)
assert raises(TypeError, add, True, 1)

# missing argument
assert raises(TypeError, add, 1)

# registry matches the functions
assert set(TOOLS) == {"add", "subtract", "multiply", "divide"}

print("All tool tests passed")