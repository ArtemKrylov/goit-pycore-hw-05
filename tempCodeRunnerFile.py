def generator_numbers(text: str) -> Iterator[float]:
    """parses numbers from string and returns iterator"""
    for found in findall(r"\s-?\d+(?:\.\d+)?(?=\s)", text):
        yield float(found)


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """sums all numbers from text using generator function func"""
    result = 0.0
    for num in func(text):
        result += num
    return result
