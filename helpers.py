from functools import wraps


def highlight_string(input_string):
    highlight_code = '\033[7;97m'
    reset_code = '\033[0m'
    highlighted_string = f"{highlight_code}{input_string}{reset_code}"
    return highlighted_string


def highlight_print(input_string):
    print(highlight_string(input_string))


def check_arguments(*arg_types):
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
