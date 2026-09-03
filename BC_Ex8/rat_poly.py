from rat_num import RatNum


class RatPoly:
    """
    Полином с рациональными коэффициентами.

    Representation fields:
        self._coeffs - tuple коэффициентов RatNum.
        Индекс коэффициента равен степени x.

    Representation invariant:
        1. self._coeffs содержит хотя бы один элемент.
        2. Все коэффициенты имеют тип RatNum.
        3. Старшие нулевые коэффициенты не хранятся.
        4. Нулевой полином хранится как (RatNum(0),).
        5. NaN-полином хранится как (RatNum(0, 0),).

    Abstraction function:
        self._coeffs[0] +
        self._coeffs[1] * x +
        self._coeffs[2] * x^2 + ...
    """

    def __init__(self, coeffs=None):
        """
        Создает полином.

        @requires:
            coeffs должен быть последовательностью RatNum или None.
        @modifies:
            Создаваемый объект.
        @effects:
            Удаляет лишние старшие нулевые коэффициенты.
            При наличии NaN создается NaN-полином.
        @throws:
            TypeError, если коэффициент не RatNum.
        @returns:
            Ничего.
        """
        if coeffs is None:
            coeffs = [RatNum(0)]

        values = list(coeffs)

        if len(values) == 0:
            values = [RatNum(0)]

        for coeff in values:
            if not isinstance(coeff, RatNum):
                raise TypeError("Все коэффициенты должны быть RatNum")

        for coeff in values:
            if coeff.is_nan():
                self._coeffs = (RatNum(0, 0),)
                return

        while len(values) > 1 and values[-1] == RatNum(0):
            values.pop()

        self._coeffs = tuple(values)

    def degree(self):
        """
        Возвращает степень полинома.

        >>> RatPoly([RatNum(1), RatNum(2), RatNum(3)]).degree()
        2

        @requires:
            Полином не должен быть NaN.
        @modifies:
            Ничего.
        @effects:
            Полином не изменяется.
        @throws:
            ValueError для NaN-полинома.
        @returns:
            Степень полинома. Для нулевого полинома 0.
        """
        if self.is_nan():
            raise ValueError("У NaN-полинома нет степени")
        return len(self._coeffs) - 1

    def get_coeff(self, degree):
        """
        Возвращает коэффициент при x в заданной степени.

        @requires:
            degree должен быть целым неотрицательным числом.
        @modifies:
            Ничего.
        @effects:
            Полином не изменяется.
        @throws:
            TypeError для не-int, ValueError для отрицательной степени.
        @returns:
            RatNum-коэффициент. Если степени нет, возвращает RatNum(0).
        """
        if not isinstance(degree, int):
            raise TypeError("Степень должна быть int")
        if degree < 0:
            raise ValueError("Степень не может быть отрицательной")

        if self.is_nan():
            return RatNum(0, 0)

        if degree >= len(self._coeffs):
            return RatNum(0)

        return self._coeffs[degree]

    def is_nan(self):
        """
        Проверяет, является ли полином NaN.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Полином не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            True для NaN-полинома.
        """
        return len(self._coeffs) == 1 and self._coeffs[0].is_nan()

    def scale_coeff(self, scalar):
        """
        Умножает каждый коэффициент на scalar.

        @requires:
            scalar должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Исходный полином не изменяется.
        @throws:
            TypeError, если scalar не RatNum.
        @returns:
            Новый RatPoly.
        """
        if not isinstance(scalar, RatNum):
            raise TypeError("scalar должен быть RatNum")

        if self.is_nan() or scalar.is_nan():
            return RatPoly([RatNum(0, 0)])

        result = []
        for coeff in self._coeffs:
            result.append(coeff * scalar)

        return RatPoly(result)

    def __neg__(self):
        """
        Возвращает полином с противоположными коэффициентами.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Исходный полином не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            Новый RatPoly.
        """
        if self.is_nan():
            return RatPoly([RatNum(0, 0)])

        result = []
        for coeff in self._coeffs:
            result.append(-coeff)

        return RatPoly(result)

    def __add__(self, other):
        """
        Складывает полиномы.

        >>> p = RatPoly([RatNum(1), RatNum(1)])
        >>> q = RatPoly([RatNum(2), RatNum(1)])
        >>> str(p + q)
        '2*x+3'

        @requires:
            other должен быть RatPoly.
        @modifies:
            Ничего.
        @effects:
            Исходные полиномы не изменяются.
        @throws:
            TypeError, если other не RatPoly.
        @returns:
            Новый RatPoly.
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Можно складывать только RatPoly")

        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])

        max_length = max(len(self._coeffs), len(other._coeffs))
        result = []

        for i in range(max_length):
            result.append(self.get_coeff(i) + other.get_coeff(i))

        return RatPoly(result)

    def __sub__(self, other):
        """
        Вычитает полиномы.

        @requires:
            other должен быть RatPoly.
        @modifies:
            Ничего.
        @effects:
            Исходные полиномы не изменяются.
        @throws:
            TypeError, если other не RatPoly.
        @returns:
            Новый RatPoly.
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Можно вычитать только RatPoly")

        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])

        max_length = max(len(self._coeffs), len(other._coeffs))
        result = []

        for i in range(max_length):
            result.append(self.get_coeff(i) - other.get_coeff(i))

        return RatPoly(result)

    def __mul__(self, other):
        """
        Умножает полиномы.

        >>> p = RatPoly([RatNum(1), RatNum(1)])
        >>> q = RatPoly([RatNum(-1), RatNum(1)])
        >>> str(p * q)
        'x^2-1'

        @requires:
            other должен быть RatPoly.
        @modifies:
            Ничего.
        @effects:
            Исходные полиномы не изменяются.
        @throws:
            TypeError, если other не RatPoly.
        @returns:
            Новый RatPoly.
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Можно умножать только RatPoly")

        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])

        result_length = len(self._coeffs) + len(other._coeffs) - 1
        result = []

        for i in range(result_length):
            result.append(RatNum(0))

        for i in range(len(self._coeffs)):
            for j in range(len(other._coeffs)):
                product = self._coeffs[i] * other._coeffs[j]
                result[i + j] = result[i + j] + product

        return RatPoly(result)

    def __truediv__(self, other):
        """
        Делит полиномы и возвращает частное.

        >>> p = RatPoly.value_of("x^2-1")
        >>> q = RatPoly.value_of("x-1")
        >>> str(p / q)
        'x+1'

        @requires:
            other должен быть RatPoly.
        @modifies:
            Ничего.
        @effects:
            Исходные полиномы не изменяются.
        @throws:
            TypeError, если other не RatPoly.
        @returns:
            Частное. При делении на нулевой полином возвращает NaN.
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Можно делить только RatPoly")

        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])

        if other == RatPoly([RatNum(0)]):
            return RatPoly([RatNum(0, 0)])

        if self.degree() < other.degree():
            return RatPoly([RatNum(0)])

        remainder = list(self._coeffs)
        quotient_size = self.degree() - other.degree() + 1
        quotient = []

        for i in range(quotient_size):
            quotient.append(RatNum(0))

        while len(remainder) - 1 >= other.degree():
            # Убираем нули в конце остатка.
            while len(remainder) > 1 and remainder[-1] == RatNum(0):
                remainder.pop()

            if len(remainder) - 1 < other.degree():
                break

            remainder_degree = len(remainder) - 1
            degree_difference = remainder_degree - other.degree()

            lead_remainder = remainder[-1]
            lead_divisor = other.get_coeff(other.degree())
            factor = lead_remainder / lead_divisor

            quotient[degree_difference] = factor

            for i in range(other.degree() + 1):
                index = i + degree_difference
                remainder[index] = remainder[index] - factor * other.get_coeff(i)

        return RatPoly(quotient)

    def eval(self, value):
        """
        Вычисляет значение полинома.

        >>> p = RatPoly.value_of("x^2+2*x+1")
        >>> str(p.eval(RatNum(2)))
        '9'

        @requires:
            value должен быть RatNum, int или float.
        @modifies:
            Ничего.
        @effects:
            Полином не изменяется.
        @throws:
            TypeError для другого типа.
        @returns:
            RatNum для RatNum-аргумента, иначе float.
        """
        if isinstance(value, RatNum):
            if self.is_nan() or value.is_nan():
                return RatNum(0, 0)

            result = RatNum(0)
            power = RatNum(1)

            for coeff in self._coeffs:
                result = result + coeff * power
                power = power * value

            return result

        if not isinstance(value, (int, float)):
            raise TypeError("value должен быть RatNum, int или float")

        if self.is_nan():
            return float("nan")

        result = 0.0
        power = 1.0

        for coeff in self._coeffs:
            result = result + coeff.float_value() * power
            power = power * value

        return result

    def differentiate(self):
        """
        Возвращает производную.

        >>> str(RatPoly.value_of("3*x^2+2*x+1").differentiate())
        '6*x+2'

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Исходный полином не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            Новый RatPoly.
        """
        if self.is_nan():
            return RatPoly([RatNum(0, 0)])

        if self.degree() == 0:
            return RatPoly([RatNum(0)])

        result = []

        for i in range(1, len(self._coeffs)):
            result.append(self._coeffs[i] * RatNum(i))

        return RatPoly(result)

    def anti_differentiate(self, integration_constant):
        """
        Возвращает первообразную.

        @requires:
            integration_constant должен быть RatNum.
        @modifies:
            Ничего.
        @effects:
            Исходный полином не изменяется.
        @throws:
            TypeError, если integration_constant не RatNum.
        @returns:
            Новый RatPoly.
        """
        if not isinstance(integration_constant, RatNum):
            raise TypeError("Константа должна быть RatNum")

        if self.is_nan() or integration_constant.is_nan():
            return RatPoly([RatNum(0, 0)])

        result = [integration_constant]

        for i in range(len(self._coeffs)):
            result.append(self._coeffs[i] / RatNum(i + 1))

        return RatPoly(result)

    def integrate(self, lower_bound, upper_bound):
        """
        Вычисляет определенный интеграл.

        @requires:
            Границы должны быть RatNum, int или float.
        @modifies:
            Ничего.
        @effects:
            Исходный полином не изменяется.
        @throws:
            TypeError для неверного типа границы.
        @returns:
            RatNum, если обе границы RatNum, иначе float.
        """
        valid_types = (RatNum, int, float)

        if not isinstance(lower_bound, valid_types):
            raise TypeError("Неверный тип нижней границы")
        if not isinstance(upper_bound, valid_types):
            raise TypeError("Неверный тип верхней границы")

        primitive = self.anti_differentiate(RatNum(0))

        if isinstance(lower_bound, RatNum) and isinstance(upper_bound, RatNum):
            return primitive.eval(upper_bound) - primitive.eval(lower_bound)

        if isinstance(lower_bound, RatNum):
            lower_bound = lower_bound.float_value()
        if isinstance(upper_bound, RatNum):
            upper_bound = upper_bound.float_value()

        return primitive.eval(float(upper_bound)) - primitive.eval(float(lower_bound))

    @classmethod
    def value_of(cls, text):
        """
        Создает полином из строки.

        >>> str(RatPoly.value_of("3/2*x^3-x+4"))
        '3/2*x^3-x+4'

        @requires:
            text должен быть str в каноническом формате без пробелов.
        @modifies:
            Ничего.
        @effects:
            Создает новый RatPoly.
        @throws:
            TypeError, если text не str.
            ValueError, если строка имеет неверный формат.
        @returns:
            Новый RatPoly.
        """
        if not isinstance(text, str):
            raise TypeError("text должен быть str")

        if text == "NaN":
            return RatPoly([RatNum(0, 0)])

        if text == "0":
            return RatPoly([RatNum(0)])

        if text == "" or " " in text:
            raise ValueError("Неверный формат полинома")

        # Чтобы проще разделить строку на слагаемые,
        # добавляем знак + перед положительным первым членом.
        work = text
        if work[0] != "-":
            work = "+" + work

        terms = []
        start = 0

        for i in range(1, len(work)):
            if work[i] == "+" or work[i] == "-":
                terms.append(work[start:i])
                start = i

        terms.append(work[start:])

        coeff_by_degree = {}
        previous_degree = None

        for term in terms:
            sign = 1
            if term[0] == "-":
                sign = -1

            body = term[1:]

            if body == "":
                raise ValueError("Неверный формат полинома")

            if "x" not in body:
                degree = 0
                coefficient = RatPoly._parse_number(body)
            else:
                if body.count("x") != 1:
                    raise ValueError("Неверный формат полинома")

                if body == "x":
                    coefficient = RatNum(1)
                    degree = 1
                elif body.startswith("x^"):
                    coefficient = RatNum(1)
                    degree_text = body[2:]
                    if not degree_text.isdigit():
                        raise ValueError("Неверная степень")
                    degree = int(degree_text)
                elif "*x" in body:
                    parts = body.split("*x")
                    if len(parts) != 2 or parts[0] == "":
                        raise ValueError("Неверный формат полинома")

                    coefficient = RatPoly._parse_number(parts[0])

                    if parts[1] == "":
                        degree = 1
                    elif parts[1].startswith("^") and parts[1][1:].isdigit():
                        degree = int(parts[1][1:])
                    else:
                        raise ValueError("Неверный формат полинома")
                else:
                    raise ValueError("Неверный формат полинома")

            if degree < 0:
                raise ValueError("Степень не может быть отрицательной")

            if sign == -1:
                coefficient = -coefficient

            if coefficient == RatNum(0) or coefficient.is_nan():
                raise ValueError("Нулевой коэффициент не записывается явно")

            if degree in coeff_by_degree:
                raise ValueError("Степень повторяется")

            if previous_degree is not None and degree >= previous_degree:
                raise ValueError("Члены должны идти по убыванию степени")

            coeff_by_degree[degree] = coefficient
            previous_degree = degree

        max_degree = max(coeff_by_degree.keys())
        coeffs = []

        for i in range(max_degree + 1):
            coeffs.append(RatNum(0))

        for degree in coeff_by_degree:
            coeffs[degree] = coeff_by_degree[degree]

        result = RatPoly(coeffs)

        # Принимаем только тот формат, который формирует __str__.
        if str(result) != text:
            raise ValueError("Строка не в каноническом формате")

        return result

    def __str__(self):
        """
        Возвращает строковое представление полинома.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Полином не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            Строка вида "x^2+2*x+1", "0" или "NaN".
        """
        if self.is_nan():
            return "NaN"

        if self == RatPoly([RatNum(0)]):
            return "0"

        result = ""

        for degree in range(self.degree(), -1, -1):
            coeff = self.get_coeff(degree)

            if coeff == RatNum(0):
                continue

            negative = coeff.is_negative()

            if negative:
                abs_coeff = -coeff
            else:
                abs_coeff = coeff

            if degree == 0:
                term = str(abs_coeff)
            elif degree == 1:
                if abs_coeff == RatNum(1):
                    term = "x"
                else:
                    term = str(abs_coeff) + "*x"
            else:
                if abs_coeff == RatNum(1):
                    term = "x^" + str(degree)
                else:
                    term = str(abs_coeff) + "*x^" + str(degree)

            if result == "":
                if negative:
                    result = "-" + term
                else:
                    result = term
            else:
                if negative:
                    result = result + "-" + term
                else:
                    result = result + "+" + term

        return result

    def __hash__(self):
        """
        Возвращает хеш полинома.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Полином не изменяется.
        @throws:
            Не возбуждает исключений.
        @returns:
            Хеш-значение.
        """
        return hash(self._coeffs)

    def __eq__(self, other):
        """
        Проверяет равенство полиномов.

        @requires:
            Нет.
        @modifies:
            Ничего.
        @effects:
            Полиномы не изменяются.
        @throws:
            Не возбуждает исключений.
        @returns:
            True для равных RatPoly.
        """
        if not isinstance(other, RatPoly):
            return False
        return self._coeffs == other._coeffs

    @staticmethod
    def _parse_number(text):
        """Вспомогательный метод чтения RatNum из строки."""
        if "/" in text:
            parts = text.split("/")
            if len(parts) != 2:
                raise ValueError("Неверная дробь")
            if not parts[0].isdigit() or not parts[1].isdigit():
                raise ValueError("Неверная дробь")
            denominator = int(parts[1])
            if denominator == 0:
                raise ValueError("Знаменатель не может быть 0")
            return RatNum(int(parts[0]), denominator)

        if not text.isdigit():
            raise ValueError("Неверное число")

        return RatNum(int(text))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
