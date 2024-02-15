def function_1(a, b, c=0):
    return a + b + c

def function_2(x, y, z):
    return x * y - z

def function_3(message="No message"):
    return message

functions_arguments = {
    function_1: {'args': (1, 2)},
    function_2: {'x': 3, 'y': 4, 'z': 5},
    function_3: {'message': "Hello, World!"}
}

for func, kwargs in functions_arguments.items():
    args = kwargs.pop('args', ())  # Extracting 'args' if present, otherwise empty tuple
    result = func(*args, **kwargs)
    print(f"Result of {func.__name__}:", result)
