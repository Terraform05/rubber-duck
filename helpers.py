from functools import wraps


def highlight_string(input_string):
    """
    Highlights the provided string using ANSI escape codes for terminal styling.

    Args:
        input_string (str): The string to be highlighted.

    Returns:
        str: The highlighted string.
    """
    highlight_code = '\033[7;97m'
    reset_code = '\033[0m'
    highlighted_string = f"{highlight_code}{input_string}{reset_code}"
    return highlighted_string


def highlight_print(input_string):
    """
    Prints the highlighted version of the provided string using ANSI escape codes for terminal styling.

    Args:
        input_string (str): The string to be highlighted.

    Returns:
        None
    """
    print(highlight_string(input_string))


def check_arguments(*arg_types):
    """
    Decorator that checks the types of arguments passed to the wrapped function.

    Args:
        *arg_types: Variable-length argument types to check against the corresponding function arguments.

    Raises:
        ValueError: If the number of provided arguments does not match the expected number.
        TypeError: If any argument's type does not match the expected type.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != len(arg_types):
                raise ValueError(
                    f"Function requires {len(arg_types)} arguments, but {len(args)} were provided")

            for arg_index, (arg, arg_type) in enumerate(zip(args, arg_types), 1):
                if not isinstance(arg, arg_type):
                    raise TypeError(
                        # f"Argument {arg_index} of type {type(arg).__name__} must be of type {arg_type.__name__}")
                        f"Argument {arg_index} of type {type(arg)} must be of type {arg_type}")

            return func(*args, **kwargs)

        return wrapper
    return decorator
