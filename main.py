from typing import Callable

from caching_fibonacci import caching_fibonacci
from text_analisis import generator_numbers, sum_profit

if __name__ == "__main__":
    # Завдання 1
    fib = caching_fibonacci()
    print(fib(10))
    print(fib(15))

    # Завдання 2
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
