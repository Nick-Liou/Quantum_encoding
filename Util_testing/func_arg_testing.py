def function_1(a, b, c=0):
    return a + b + c

def function_2(x, y, z):
    return x * y - z

def function_3(message="No message"):
    return message

functions_arguments = {
    function_1: (1, 2),
    function_2: {'x': 3, 'y': 4, 'z': 5},
    function_3: {'message': "Hello, World!"}
}

for func, args in functions_arguments.items():
    if isinstance(args, dict):
        result = func(**args)
    else:
        result = func(*args)
    print(f"Result of {func.__name__}:", result)
