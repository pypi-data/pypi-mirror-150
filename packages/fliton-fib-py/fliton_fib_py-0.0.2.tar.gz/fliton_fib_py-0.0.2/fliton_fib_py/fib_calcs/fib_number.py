def recur_fib_num(number: int) -> int:
    if number < 0:
        raise ValueError("Fibonacci has to start from 1")
    elif number <= 1:
        return number
    else:
        return recur_fib_num(number - 1) + recur_fib_num(number - 2)
