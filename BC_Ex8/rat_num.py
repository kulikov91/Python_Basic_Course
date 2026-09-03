class RatNum:
    """
    Неизменяемое рациональное число.

    Representation fields:
        self._num - числитель.
        self._den - знаменатель.

    Representation invariant:
        1. Знаменатель обычного числа всегда больше 0.
        2. Дробь всегда сокращена.
        3. Ноль хранится как 0/1.
        4. NaN хранится как 0/0.
        5. После создания объекта поля нельзя изменить.

    Abstraction function:
        Если self._den == 0, объект представляет NaN.
        Иначе объект представляет число self._num / self._den.
    """

    def __init__(self, numerator=0, denominator=1):
        """
        Создает рациональное число.

        @requires:
            numerator и denominator должны быть int.
        @modifies:
            Создаваемый объект.
        @effects:
            Сокращает дробь и приводит знак к числителю.
            При denominator == 0 создается NaN.
        @throws:
            TypeError, если numerator или denominator не int.
        @returns:
            Ничего.
        """
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("Числитель и знаменатель должны быть int")

        object.__setattr__(self, "_initialized", False)

        if denominator == 0:
            numerator = 0
            denominator = 0
        elif numerator == 0:
            denominator = 1
        else:
            if denominator < 0:
                numerator = -numerator
                denominator = -denominator

            divisor = RatNum.gcd(abs(numerator), denominator)
            numerator = numerator // divisor
            denominator = denominator // divisor

        object.__setattr__(self, "_num", numerator)
        object.__setattr__(self, "_den", denominator)
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name, value):
        """
        Вспомогательный механизм неизменяемости RatNum.
        """
        if getattr(self, "_initialized", False):
            raise AttributeError("RatNum является неизменяемым")
        object.__setattr__(self, name, value)

    def is_nan(self):
        """
        Проверяет, является ли число NaN.

        >>> RatNum(1, 0).is_nan()
        True
        >>> RatNum(1, 2).is_nan()
        False

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            True для NaN, иначе False.
        """
        return self._den == 0

    def is_negative(self):
        """
        Проверяет, является ли число отрицательным.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            True, если число меньше 0. Для NaN возвращает False.
        """
        if self.is_nan():
            return False
        return self._num < 0

    def is_positive(self):
        """
        Проверяет, является ли число положительным.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            True, если число больше 0. Для NaN возвращает False.
        """
        if self.is_nan():
            return False
        return self._num > 0

    def compare_to(self, other):
        """
        Сравнивает два RatNum.
        NaN равен NaN и больше любого обычного RatNum.

        >>> RatNum(1, 2).compare_to(RatNum(2, 3))
        -1
        >>> RatNum(1, 0).compare_to(RatNum(100))
        1

        @requires:
            other должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Объекты не изменяются.
        @throws:
            TypeError, если other не RatNum.
        @returns:
            -1, 0 или 1.
        """
        if not isinstance(other, RatNum):
            raise TypeError("Можно сравнивать только с RatNum")

        if self.is_nan() and other.is_nan():
            return 0
        if self.is_nan():
            return 1
        if other.is_nan():
            return -1

        left = self._num * other._den
        right = other._num * self._den

        if left < right:
            return -1
        if left > right:
            return 1
        return 0

    def float_value(self):
        """
        Возвращает значение как float.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            float-значение или float('nan') для NaN.
        """
        if self.is_nan():
            return float("nan")
        return self._num / self._den

    def int_value(self):
        """
        Возвращает целую часть с усечением к нулю.

        @requires:
            self не должен быть NaN.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            ValueError для NaN.
        @returns:
            Целое число.
        """
        if self.is_nan():
            raise ValueError("NaN нельзя преобразовать в int")

        result = abs(self._num) // self._den
        if self._num < 0:
            result = -result
        return result

    def __neg__(self):
        """
        Возвращает число с противоположным знаком.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            self не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            Новый RatNum, равный -self.
        """
        if self.is_nan():
            return RatNum(0, 0)
        return RatNum(-self._num, self._den)

    def __add__(self, other):
        """
        Складывает два RatNum.

        >>> str(RatNum(1, 2) + RatNum(1, 3))
        '5/6'

        @requires:
            other должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Операнды не изменяются.
        @throws:
            TypeError, если other не RatNum.
        @returns:
            Новый RatNum. При NaN возвращается NaN.
        """
        if not isinstance(other, RatNum):
            raise TypeError("Можно складывать только RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)

        numerator = self._num * other._den + other._num * self._den
        denominator = self._den * other._den
        return RatNum(numerator, denominator)

    def __sub__(self, other):
        """
        Вычитает два RatNum.

        @requires:
            other должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Операнды не изменяются.
        @throws:
            TypeError, если other не RatNum.
        @returns:
            Новый RatNum. При NaN возвращается NaN.
        """
        if not isinstance(other, RatNum):
            raise TypeError("Можно вычитать только RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)

        numerator = self._num * other._den - other._num * self._den
        denominator = self._den * other._den
        return RatNum(numerator, denominator)

    def __mul__(self, other):
        """
        Умножает два RatNum.

        @requires:
            other должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Операнды не изменяются.
        @throws:
            TypeError, если other не RatNum.
        @returns:
            Новый RatNum. При NaN возвращается NaN.
        """
        if not isinstance(other, RatNum):
            raise TypeError("Можно умножать только RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)

        return RatNum(self._num * other._num, self._den * other._den)

    def __truediv__(self, other):
        """
        Делит два RatNum.

        >>> str(RatNum(2, 3) / RatNum(4, 5))
        '5/6'
        >>> str(RatNum(1) / RatNum(0))
        'NaN'

        @requires:
            other должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Операнды не изменяются.
        @throws:
            TypeError, если other не RatNum.
        @returns:
            Новый RatNum. Деление на 0 и операции с NaN дают NaN.
        """
        if not isinstance(other, RatNum):
            raise TypeError("Можно делить только RatNum")

        if self.is_nan() or other.is_nan() or other._num == 0:
            return RatNum(0, 0)

        return RatNum(self._num * other._den, self._den * other._num)

    @staticmethod
    def gcd(a, b):
        """
        Находит наибольший общий делитель.

        >>> RatNum.gcd(12, 8)
        4

        @requires:
            a и b должны быть int.
        @modifies:
            Ничего.
        @effects:
            Аргументы не изменяются.
        @throws:
            TypeError, если a или b не int.
        @returns:
            Неотрицательный НОД.
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("gcd принимает только int")

        a = abs(a)
        b = abs(b)

        while b != 0:
            temp = a % b
            a = b
            b = temp

        return a

    def __str__(self):
        """
        Возвращает строковое представление.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            "NaN", целое число или дробь вида "n/d".
        """
        if self.is_nan():
            return "NaN"
        if self._den == 1:
            return str(self._num)
        return str(self._num) + "/" + str(self._den)

    def __hash__(self):
        """
        Возвращает хеш RatNum.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объект не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            Хеш-значение RatNum.
        """
        return hash((self._num, self._den))

    def __eq__(self, other):
        """
        Проверяет равенство.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Объекты не изменяются.
        @throws:
            Не возбуждает исключений.
        @returns:
            True для равных RatNum. NaN равен NaN.
        """
        if not isinstance(other, RatNum):
            return False
        return self._num == other._num and self._den == other._den


if __name__ == "__main__":
    import doctest
    doctest.testmod()
