import csv
import math
import doctest

DEBUG = False
LINE = "=" * 41

class Market:
    """Описывает один фермерский рынок"""

    def __init__(self, data):
        """Создает объект фермерского рынка из строки CSV"""

        self.fmid = data["FMID"]
        self.name = data["MarketName"]
        self.city = data["city"]
        self.state = data["State"]
        self.street = data["street"]
        self.zip = data["zip"]
        self.website = data["Website"]
        self.organic = data["Organic"]
        self.x = data["x"]
        self.y = data["y"]

    def coordinates(self):
        """Возвращает координаты рынка в виде (широта, долгота)"""

        if not self.x or not self.y:
            return None

        return float(self.y), float(self.x)

    def short_info(self):
        """Возвращает краткую информацию о рынке"""

        return f"{self.fmid} - {self.name}"

    def full_info(self):
        """Выводит полную информацию о рынке"""

        print("\n=== Информация о рынке ===")
        print("Название:", self.name)
        print("Город:", self.city)
        print("Штат:", self.state)
        print("Адрес:", self.street)
        print("Индекс:", self.zip)
        print("Сайт:", self.website)
        print("Органический:", self.organic)

    def __str__(self):
        """Возвращает строковое представление объекта"""

        return self.short_info()

class MarketManager:
    """Управляет списком фермерских рынков"""

    def __init__(self, filename):
        self.markets = []
        self.load_data(filename)

    def load_data(self, filename):
        """Загружает рынки из CSV"""
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.markets.append(Market(row))

    def search_by_zip(self, zip_code):
        """
        Ищет рынки по почтовому индексу.

        >>> manager = MarketManager("Export.csv")

        >>> len(manager.search_by_zip("05828")) > 0
        True

        >>> len(manager.search_by_zip("99999"))
        0

        >>> manager.search_by_zip("05828")[0].zip
        '05828'
        """
        result = []

        for market in self.markets:
            if market.zip == zip_code:
                result.append(market)

        return result

    def search_by_city_state(self, city, state):
        """
        Поиск рынков по городу и штату.

        >>> manager = MarketManager("Export.csv")

        >>> len(manager.search_by_city_state("Danville", "Vermont")) > 0
        True

        >>> isinstance(manager.search_by_city_state("Danville", "Vermont"), list)
        True

        >>> manager.search_by_city_state("danville", "vermont")[0].city
        'Danville'

        >>> manager.search_by_city_state("danville", "vermont")[0].state
        'Vermont'
        """
        result = []

        for market in self.markets:
            if (market.city.lower() == city.lower()
                    and market.state.lower() == state.lower()):
                result.append(market)

        return result

    def get_market_by_id(self, fmid):
        """
        Возвращает рынок по его FMID.

        >>> manager = MarketManager("Export.csv")

        >>> manager.get_market_by_id("1018261").city
        'Danville'

        >>> manager.get_market_by_id("1018261").state
        'Vermont'

        >>> manager.get_market_by_id("99999999") is None
        True

        >>> manager.get_market_by_id("1018261").fmid
        '1018261'
        """

        for market in self.markets:

            if market.fmid == fmid:
                return market

        return None

    def sort_markets(self, field, reverse=False):
        """Сортирует список рынков"""

        return sorted(
            self.markets,
            key=lambda market: getattr(market, field),
            reverse=reverse
        )

    @staticmethod
    def calculate_distance(point1, point2):
        """
        Вычисляет расстояние между двумя точками в милях.

        >>> round(MarketManager.calculate_distance((0, 0), (0, 0)), 2)
        0.0

        >>> round(MarketManager.calculate_distance((0, 0), (0, 1)), 2)
        69.1

        >>> round(MarketManager.calculate_distance((40, -70), (41, -71)), 2)
        86.81

        >>> MarketManager.calculate_distance((10, 10), (10, 10)) == 0
        True

        >>> MarketManager.calculate_distance((0, 0), (1, 1)) > 0
        True
        """

        lat1 = math.radians(point1[0])
        lon1 = math.radians(point1[1])

        lat2 = math.radians(point2[0])
        lon2 = math.radians(point2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2)

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a))

        earth_radius = 3959.3
        return earth_radius * c

    def get_coordinates_by_zip(self, zip_code):
        """
        Возвращает координаты первого рынка с указанным ZIP-кодом

        >>> manager = MarketManager("Export.csv")

        >>> isinstance(manager.get_coordinates_by_zip("05828"), tuple)
        True

        >>> manager.get_coordinates_by_zip("99999") is None
        True
        """
        for market in self.markets:

            if market.zip == zip_code:
                return market.coordinates()

        return None

    def search_by_distance(self, zip_code, radius):
        """
        Ищет рынки в заданном радиусе.

        >>> manager = MarketManager("Export.csv")

        >>> len(manager.search_by_distance("05828", 0)) >= 1
        True

        >>> manager.search_by_distance("99999", 30)
        []

        >>> len(manager.search_by_distance("05828", 30)) > 0
        True

        >>> manager.search_by_distance("05828", 30)[0][1] >= 0
        True
        """

        point = self.get_coordinates_by_zip(zip_code)

        if point is None:
            return []

        result = []

        for market in self.markets:
            market_point = market.coordinates()

            if market_point is None:
                continue

            distance = self.calculate_distance(point, market_point)

            if distance <= radius:
                result.append((market, distance))

        result.sort(key=lambda item: item[1])

        return result

    def show_markets(self, page=1, size=10, markets=None):
        """
        Выводит список рынков постранично.
        markets - список рынков.
        page - номер страницы.
        size - количество записей на странице.
        """

        if markets is None:
            markets = self.markets

        total = len(markets)
        total_pages = (total + size - 1) // size

        page = max(1, min(page, total_pages))

        start = (page - 1) * size
        end = start + size
        page_data = markets[start:end]

        print("\n" + "=" * 70)
        print(f"{'FMID':<10} {'NAME':<35} {'CITY':<15} {'STATE':<5}")
        print("-" * 70)

        for m in page_data:
            print(
                f"{m.fmid:<10}"
                f"{m.name[:33]:<35}"
                f"{m.city:<15}"
                f"{m.state:<5}"
            )

        print("-" * 70)
        print(f"Страница {page}/{total_pages} | Всего рынков: {total}")
        print("=" * 70)

class ReviewManager:
    """Управляет отзывами пользователей"""

    def __init__(self, filename):
        self.filename = filename
        self.reviews = []
        self.load_reviews()

    def load_reviews(self):
        """Загружает отзывы из CSV-файла"""

        self.reviews = []

        try:
            with open(self.filename, encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.reviews.append(row)

        except FileNotFoundError:
            pass

    def save_reviews(self):
        """ Сохранение отзывов в CSV-файл"""

        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            fields = ["FMID", "Name", "Review", "Rating"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for review in self.reviews:
                writer.writerow(review)

    def add_review(self, market_id, name, text, rating):
        """ Добавление отзыва"""

        review = {
            "FMID": market_id,
            "Name": name,
            "Review": text,
            "Rating": str(rating)
        }
        self.reviews.append(review)

    def get_market_reviews(self, market_id):
        """Получение отзывов для выбранного рынка"""

        result = []

        for review in self.reviews:
            if review["FMID"] == market_id:
                result.append(review)
        return result

class FarmMarketApp:

    def __init__(self, market_manager, review_manager):
        """Создает объект приложения"""

        self.market_manager = market_manager
        self.review_manager = review_manager

    def process_details(self):
        """Показывает подробную информацию о рынке по введенному FMID"""

        fmid = input(
            "\nВведите ID рынка для просмотра деталей "
            "(или Enter для выхода): "
        )

        if fmid == "":
            return

        market = self.market_manager.get_market_by_id(fmid)

        if market:
            market.full_info()
        else:
            print("Рынок с таким FMID не найден!")

    def process_show(self):
        """
        Показывает список фермерских рынков
        с разбивкой по страницам
        """
        try:
            page = int(input("Введите номер страницы: "))
        except ValueError:
            print("Введите номер страницы цифрами!")
            return

        while True:
            self.market_manager.show_markets(page)
            action = input(
                "\n[n] Следующая  [p] Предыдущая  "
                "[номер] Перейти на страницу  [q] Выход ==> ").lower()

            total_pages = (len(self.market_manager.markets) + 9) // 10

            if action == "n":
                if page < total_pages:
                    page += 1
                else:
                    print("Это последняя страница.")

            elif action == "p":
                if page > 1:
                    page -= 1
                else:
                    print("Это первая страница.")

            elif action.isdigit():
                new_page = int(action)

                if 1 <= new_page <= total_pages:
                    page = new_page
                else:
                    print("Такой страницы нет!")

            elif action == "q":
                break
            else:
                print("Неизвестная команда.")

    def process_search(self):
        """
        Находит фермерский рынок
        по городу и штату
        """
        city = input("Введите город: ")
        state = input("Введите штат: ")

        result = self.market_manager.search_by_city_state(city, state)

        if len(result) == 0:
            print("Рынки не найдены!")

        else:
            print("Найдено рынков:", len(result))

            for market in result:
                print(market)

            self.process_details()

    def process_zip(self):
        """Находит фермерский рынок по индексу"""

        zip_code = input("Введите ZIP-код: ")
        result = self.market_manager.search_by_zip(zip_code)

        if len(result) == 0:
            print("Рынки не найдены!")
        else:
            print("Найдено рынков:", len(result))

            for market in result:
                print(market)

            self.process_details()

    def process_distance(self):
        """Поиск рынков в заданном радиусе"""

        zip_code = input("Введите ZIP-код: ")

        try:
            radius = float(input("Введите радиус (в милях): "))
        except ValueError:
            print("Введите радиус числом!")
            return

        result = self.market_manager.search_by_distance(zip_code, radius)

        if len(result) == 0:
            print("Рынки не найдены!")
        else:
            print("Найдено рынков:", len(result))

            for market, distance in result:
                print(
                    market.fmid,
                    "-",
                    market.name,
                    "-",
                    market.city,
                    "-",
                    market.state
                )

                print(f"Расстояние: {distance:.2f} миль.\n")

            self.process_details()

    def process_review(self):
        """ Добавляет отзыв о рынке"""

        market_id = input("Введите FMID рынка (или Enter для выхода): ")
        market = self.market_manager.get_market_by_id(market_id)

        if market is None:
            print("Рынок не найден!")
            return

        name = input("Введите имя и фамилию: ")

        while True:
            try:
                rating = int(input("Оценка (1-5): "))

                if 1 <= rating <= 5:
                    break

                print("Оценка должна быть от 1 до 5.")

            except ValueError:
                print("Введите число!")

        text = input("Введите отзыв (можно оставить пустым): ")
        self.review_manager.add_review(market_id, name, text, rating)
        self.review_manager.save_reviews()
        print("Отзыв успешно сохранён!")

    def process_reviews(self):
        """ Показывает отзывы о рынке"""

        market_id = input("Введите FMID рынка: ")
        market = self.market_manager.get_market_by_id(market_id)

        if market is None:
            print("Рынок не найден!")
            return

        reviews = self.review_manager.get_market_reviews(market_id)

        if len(reviews) == 0:
            print("Для этого рынка пока нет отзывов :(")
        else:
            print("\nОтзывы о рынке:")
            print("-" * 40)

            for review in reviews:
                print("Автор:", review["Name"])
                print("Оценка:", review["Rating"], "/ 5")

                if review["Review"] != "":
                    print("Отзыв:", review["Review"])

                print("-" * 40)

    def process_sort(self):
        """
        Производит сортировку рынков
        по выбранному полю
        """
        print("\nВыберите поле для сортировки:")
        print("1 - Название рынка")
        print("2 - Город")
        print("3 - Штат")

        choice = input("Ваш выбор: ")
        order = input("По возрастанию (a) или убыванию (d)? ").lower()
        reverse = False

        if order == "d":
            reverse = True

        if choice == "1":
            markets = self.market_manager.sort_markets("name", reverse)

        elif choice == "2":
            markets = self.market_manager.sort_markets("city", reverse)

        elif choice == "3":
            markets = self.market_manager.sort_markets("state", reverse)

        else:
            print("Неверный выбор!")
            return

        page = int(input("Введите номер страницы: "))
        self.market_manager.show_markets(
            markets=markets,
            page=page
        )

    def run(self):
        """
        Основной цикл работы программы.
        Обрабатывает команды, вводимые пользователем.
        """
        show_welcome()

        while True:
            cmd = input(
                "\033[31m\nВВЕДИТЕ КОМАНДУ БЕЗ КАВЫЧЕК:\n\033[0m"
                "('show', 'search', 'zip', 'distance','review', 'sort', 'reviews', 'end', 'help') ==> "
            ).lower()

            if cmd == "end":
                print("Программа завершена!")
                break

            elif cmd == "show":
                self.process_show()

            elif cmd == "search":
                self.process_search()

            elif cmd == "distance":
                self.process_distance()

            elif cmd == "review":
                self.process_review()

            elif cmd == "reviews":
                self.process_reviews()

            elif cmd == "zip":
                self.process_zip()

            elif cmd == "help":
                show_welcome()

            elif cmd == "sort":
               self.process_sort()

            else:
                print(
                    "Неизвестная команда. "
                    "Введите help для отображения списка команд.")


def show_welcome():
    """
    Выводит приветственное сообщение и список доступных команд.
    """
    print(f"""{LINE}
   \033[31mДобро пожаловать в программу поиска
         фермерских рынков США\033[0m
{LINE}

        === \033[31mДоступные команды\033[0m ===

                = \033[31mSHOW\033[0m =
    Показывает список фермерских рынков
        с разбивкой по страницам

               = \033[31mSEARCH\033[0m =
        Находит фермерский рынок
            по городу и штату

                 = \033[31mZIP\033[0m =
        Находит фермерский рынок
               по индексу

              = \033[31mDISTANCE\033[0m =
        Находит фермерский рынок
          в указанном радиусе
         от заданного ZIP-кода

               = \033[31mDETAILS\033[0m =
     Показывает подробную информацию
            о выбранном рынке

               = \033[31mREVIEW\033[0m =
         Оставить отзыв о рынке

                = \033[31mSORT\033[0m =
       Отсортировать список рынков
      по названию, городу или штату

               = \033[31mREVIEWS\033[0m =
        Просмотреть отзывы о рынке

                = \033[31mEND\033[0m =
        Завершает работу программы
{LINE}
""")

if __name__ == "__main__":

    if DEBUG:
        print(f"{LINE}")
        print("Running doctests...")
        print(f"{LINE}")

        failures, tests = doctest.testmod()

        print(f"Tests run: {tests}")
        print(f"Failures : {failures}")

    market_manager = MarketManager("Export.csv")

    review_manager = ReviewManager("reviews.csv")

    app = FarmMarketApp(market_manager,review_manager)

    app.run()
