from typing import Optional


def recur_fib_num(number: int) -> Optional[int]:
    if number < 0:
        return None
    elif number <= 1:
        return number
    else:
        return recur_fib_num(number - 1) + recur_fib_num(number - 2)
