import argparse

from fliton_fib_py.fib_calcs.fib_number import recur_fib_num


def fib_numb() -> None:
    parser = argparse.ArgumentParser(description='Calculate Fibonacci numbers')
    parser.add_argument('--number', action='store', type=int,
                        required=True, help='Fibonacci number to be calculated')
    args = parser.parse_args()
    print(f"You fibonacci number is: " f"{recur_fib_num(number=args.number)}")
