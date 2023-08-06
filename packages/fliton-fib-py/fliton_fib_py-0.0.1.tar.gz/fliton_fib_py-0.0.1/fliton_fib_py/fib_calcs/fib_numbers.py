import numbers
from typing import List
from .fib_number import recur_fib_num


def calculate_numbers(numbers: List[int]) -> List[int]:
    return [recur_fib_num(number=i) for i in numbers]
