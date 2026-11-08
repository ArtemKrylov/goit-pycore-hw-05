from functools import wraps
from typing import Callable

from colorama import Fore


def input_error(func: Callable):
    @wraps(func)
    def inner(*args, **qwargs):
        try:
            return func(*args, **qwargs)
        except KeyError as error:
            contact_name = error.args[0]
            return f"Contact {Fore.BLUE}{contact_name}{Fore.RESET} does not exist."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"

    return inner
