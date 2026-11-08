from functools import wraps
from typing import Callable

from colorama import Fore


def handle_file_errors(func):
    """Handle file reading and parsing errors."""
    @wraps(func)
    def inner(*args, **qwargs):
        """Return an empty list if loading fails."""
        try:
            return func(*args, **qwargs)
        except FileNotFoundError:
            print("File not found")
            return []
        except (ValueError, UnicodeDecodeError):
            print("Invalid file data")
            return []
        except OSError as error:
            print(f"Could not read the file: {error}")
            return []

    return inner


def input_error(func: Callable):
    """Report missing keys as unknown log levels."""
    @wraps(func)
    def inner(*args, **qwargs):
        """Call the wrapped function and handle KeyError."""
        try:
            return func(*args, **qwargs)
        except KeyError as error:
            entered_level = error.args[0]
            print(f"Level {Fore.RED}{entered_level}{Fore.RESET} does not exist.")

    return inner
