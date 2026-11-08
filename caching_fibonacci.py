from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """return fibonacci finding function with cashing"""
    cashe = {}

    def fibonacci(num: int) -> int:
        """Takes the index of a Fibonacci number and returns the corresponding Fibonacci number"""

        if num in cashe:
            return cashe[num]

        if num <= 0:
            return 0
        if num == 1:
            return 1

        result = fibonacci(num - 1) + fibonacci(num - 2)
        cashe[num] = result
        return result

    return fibonacci
