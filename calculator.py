def calculate(a: float, op: str, b: float) -> float:
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError('Cannot divide by zero')
        return a / b
    raise ValueError('Unsupported operation')


def read_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print('Please enter a valid number.')


def main() -> None:
    print('Very Simple Calculator')
    print("Operations: '+', '-', '*', '/'  | type 'q' to quit")
    while True:
        op = input('Choose operation (+ - * / or q): ').strip().lower()
        if op in {'q', 'quit', 'exit'}:
            print('Goodbye!')
            break
        if op not in {'+', '-', '*', '/'}:
            print('Unsupported operation. Try again.')
            continue

        a = read_number('Enter first number: ')
        b = read_number('Enter second number: ')

        try:
            result = calculate(a, op, b)
            print(f'Result: {result}')
        except ZeroDivisionError as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    main()
