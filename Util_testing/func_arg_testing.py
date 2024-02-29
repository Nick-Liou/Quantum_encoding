from typing import Callable, Any

def function_1(a: int, b: int, c: int = 0) -> int:
    return a + b + c

def function_2(x: int, y: int, z: int) -> int:
    return x * y - z

def function_3(message: str = "No message") -> str:
    return message

functions_arguments: dict[Callable, dict[str, Any]] = {
    function_1: {'args': (1, 2)},
    function_2: {'x': 3, 'y': 4, 'z': 5},
    function_3: {'message': "Hello, World!"}
}

for func, kwargs in functions_arguments.items():
    args: tuple[Any, ...] = kwargs.pop('args', ())  # Explicitly annotate args as Tuple
    result = func(*args, **kwargs)
    print(f"Result of {func.__name__}:", result)
