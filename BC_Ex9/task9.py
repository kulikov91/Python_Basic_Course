class Fibo:
    """
    Итератор, который возвращает числа Фибоначчи:
    0, 1, 1, 2, 3, 5, 8, ...

    Для получения следующего числа используется только сложение.
    """

    def __init__(self):
        """
        Создает новый итератор Фибоначчи.
        """
        self.first = 0
        self.second = 1

    def __iter__(self):
        """
        Возвращает сам объект-итератор.
        """
        return self

    def __next__(self):
        """
        Возвращает следующее число Фибоначчи.
        """
        result = self.first

        next_number = self.first + self.second
        self.first = self.second
        self.second = next_number

        return result


def integers():
    """
    Генератор неотрицательных целых чисел:
    0, 1, 2, 3, 4, ...
    """
    number = 0

    while True:
        yield number
        number += 1


def primes():
    """
    Генератор простых чисел:
    2, 3, 5, 7, 11, 13, ...

    Простое число делится без остатка только на 1 и само себя.
    """
    number = 2

    while True:
        is_prime = True

        for divisor in range(2, number):
            if number % divisor == 0:
                is_prime = False
                break

        if is_prime:
            yield number

        number += 1


if __name__ == "__main__":
    # Несколько простых примеров работы.

    print("Первые 10 чисел Фибоначчи:")
    fibo = Fibo()

    for i in range(10):
        print(next(fibo), end=" ")

    print("\n")

    print("Первые 10 неотрицательных целых чисел:")
    numbers = integers()

    for i in range(10):
        print(next(numbers), end=" ")

    print("\n")

    print("Первые 10 простых чисел:")
    prime_numbers = primes()

    for i in range(10):
        print(next(prime_numbers), end=" ")

    print()
