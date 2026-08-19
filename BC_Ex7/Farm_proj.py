import csv
import math
import doctest
import zip_util

DEBUG = False
LINE = "=" * 35

STATE_CODES = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC"
}

def normalize_state(state):
    """
    Приводит название штата или его код к двухбуквенному коду.

    Предусловия:
        state — строка с названием штата или его кодом.

    Постусловия:
        Возвращает двухбуквенный код штата в верхнем регистре.
        Если штат не найден, возвращает нормализованную исходную строку.

    >>> normalize_state("Vermont")
    'VT'
    >>> normalize_state("vermont")
    'VT'
    >>> normalize_state("vt")
    'VT'
    >>> normalize_state("New York")
    'NY'
    >>> normalize_state("Puerto Rico")
    'PR'
    >>> normalize_state("XX")
    'XX'
    """
    state = state.strip()

    if len(state) == 2:
        return state.upper()

    for full_name, code in STATE_CODES.items():
        if full_name.lower() == state.lower():
            return code

    return state.upper()

class Market:
    """Описывает один фермерский рынок."""

    def __init__(self, data):
        """
        Создает объект фермерского рынка из строки CSV.

        Предусловия:
            data — словарь, содержащий как минимум поля FMID, MarketName,
            city, State, street, zip, Website, x и y.

        Постусловия:
            Создается объект Market с данными одной записи CSV.
        """
        self.data = data.copy()
        self.fmid = data["FMID"]
        self.name = data["MarketName"]
        self.city = data["city"]
        self.state = data["State"]
        self.street = data["street"]
        self.zip = data["zip"]
        self.website = data["Website"]
        self.organic = data.get("Organic", "")
        self.x = data.get("x", "")
        self.y = data.get("y", "")
        self.credit = data.get("Credit", "")
        self.wic = data.get("WIC", "")
        self.wiccash = data.get("WICcash", "")
        self.sfmnp = data.get("SFMNP", "")
        self.snap = data.get("SNAP", "")

    def coordinates(self):
        """
        Возвращает координаты рынка в виде (широта, долгота).

        Постусловия:
            Возвращает кортеж из двух чисел float или None,
            если координаты отсутствуют или некорректны.

        >>> m = Market({"FMID":"1", "MarketName":"A", "city":"X", "State":"VT", "street":"", "zip":"05828", "Website":"", "x":"-72.1", "y":"44.4"})
        >>> m.coordinates()
        (44.4, -72.1)
        >>> m2 = Market({"FMID":"2", "MarketName":"B", "city":"X", "State":"VT", "street":"", "zip":"05828", "Website":"", "x":"", "y":""})
        >>> m2.coordinates() is None
        True
        """
        try:
            if self.x == "" or self.y == "":
                return None
            return float(self.y), float(self.x)
        except (ValueError, TypeError):
            return None

    def short_info(self):
        """Возвращает краткую информацию о рынке."""
        return f"{self.fmid} - {self.name}"

    def full_info(self, average_rating=0, reviews_count=0):
        """
        Выводит полную информацию о рынке, категории товаров и рейтинг.

        Предусловия:
            average_rating — средняя оценка рынка или 0.
            reviews_count — количество отзывов.

        Постусловия:
            Информация выводится в консоль.
        """
        print("\n=== Информация о рынке ===")
        print("Название:", self.name)
        print("Город:", self.city)
        print("Штат:", self.state)
        print("Адрес:", self.street)
        print("Индекс:", self.zip)
        print("Сайт:", self.website)

        print("\n=== Категории товаров ===")

        product_fields = [
            "Organic", "Bakedgoods", "Cheese", "Crafts", "Flowers", "Eggs",
            "Seafood", "Herbs", "Vegetables", "Honey", "Jams", "Maple",
            "Meat", "Nursery", "Nuts", "Plants", "Poultry", "Prepared",
            "Soap", "Trees", "Wine", "Coffee", "Beans", "Fruits", "Grains",
            "Juices", "Mushrooms", "PetFood", "Tofu", "WildHarvested"
        ]

        for field in product_fields:
            if field in self.data:
                value = self.data[field].strip()

                if value != "":
                    print(field + ":", value)

        print("\n=== Оплата и программы ===")

        payment_fields = ["Credit", "WIC", "WICcash", "SFMNP", "SNAP"]

        for field in payment_fields:
            if field in self.data:
                value = self.data[field].strip()

                if value != "":
                    print(field + ":", value)

        print("\n=== Рейтинг ===")

        if average_rating == 0:
            print("Средний рейтинг: нет оценок")
        else:
            print(f"Средний рейтинг: {average_rating:.1f} из 5")

        print("Количество отзывов:", reviews_count)

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return self.short_info()

class MarketManager:
    """Управляет списком фермерских рынков."""

    def __init__(self, filename):
        """
        Предусловия:
            filename — имя существующего CSV-файла с рынками.

        Постусловия:
            Загружает рынки и полный справочник координат ZIP-кодов.
        """
        self.filename = filename
        self.markets = []
        self.zip_coordinates = {}
        self.load_data(filename)
        self.load_zip_coordinates()

    def load_data(self, filename):
        """Загружает рынки из CSV."""
        self.markets = []

        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.markets.append(Market(row))

    def save_data(self):
        """
        Сохраняет актуальный список рынков в исходный CSV-файл.

        Постусловия:
            CSV-файл перезаписывается текущим содержимым self.markets.
        """
        if len(self.markets) == 0:
            return

        fields = list(self.markets[0].data.keys())

        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for market in self.markets:
                writer.writerow(market.data)

    def load_zip_coordinates(self):
        """Загружает полный справочник координат ZIP-кодов."""
        self.zip_coordinates = {}
        zip_codes = zip_util.read_zip_all()

        for zip_data in zip_codes:
            self.zip_coordinates[zip_data[0]] = (zip_data[1], zip_data[2])

    def get_user_zip_coordinates(self, zip_code):
        """
        Возвращает координаты ZIP-кода из полного справочника.

        >>> manager = MarketManager("Export.csv")
        >>> isinstance(manager.get_user_zip_coordinates("05828"), tuple)
        True
        >>> manager.get_user_zip_coordinates("00000") is None
        True
        """
        return self.zip_coordinates.get(zip_code)

    def get_market_coordinates(self, market):
        """
        Возвращает координаты рынка.
        Если x/y отсутствуют, использует координаты ZIP-кода рынка.

        Предусловия:
            market — объект Market.

        Постусловия:
            Возвращает (широта, долгота) или None.
        """
        point = market.coordinates()

        if point is not None:
            return point

        return self.zip_coordinates.get(market.zip)

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
        Штат можно вводить полным названием или двухбуквенным кодом.

        >>> manager = MarketManager("Export.csv")
        >>> len(manager.search_by_city_state("Danville", "Vermont")) > 0
        True
        >>> len(manager.search_by_city_state("Danville", "VT")) > 0
        True
        >>> manager.search_by_city_state("danville", "vt")[0].city
        'Danville'
        >>> manager.search_by_city_state("danville", "vt")[0].state
        'Vermont'
        """
        result = []
        required_state = normalize_state(state)

        for market in self.markets:
            if (market.city.lower() == city.lower()
                    and normalize_state(market.state) == required_state):
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

    def delete_market(self, fmid):
        """
        Удаляет рынок из списка.

        Постусловия:
            Возвращает True при успешном удалении, иначе False.

        >>> manager = MarketManager.__new__(MarketManager)
        >>> manager.markets = [Market({"FMID":"1", "MarketName":"A", "city":"X", "State":"VT", "street":"", "zip":"1", "Website":"", "x":"", "y":""})]
        >>> manager.delete_market("1")
        True
        >>> len(manager.markets)
        0
        >>> manager.delete_market("999")
        False
        """
        market = self.get_market_by_id(fmid)

        if market is None:
            return False

        self.markets.remove(market)
        return True

    def sort_markets(self, field, reverse=False):
        """
        Сортирует список рынков по атрибуту.

        Предусловия:
            field — имя существующего атрибута Market.

        Постусловия:
            Возвращает новый отсортированный список.
            Исходный self.markets не изменяется.
        """
        return sorted(
            self.markets,
            key=lambda market: str(getattr(market, field)).lower(),
            reverse=reverse)

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

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        earth_radius = 3959.3
        return earth_radius * c

    def search_by_distance(self, zip_code, radius):
        """
        Ищет рынки в заданном радиусе от любого ZIP-кода из справочника.

        Предусловия:
            zip_code — строка с ZIP-кодом.
            radius — неотрицательное число.

        Постусловия:
            Возвращает список кортежей (рынок, расстояние),
            отсортированный по расстоянию.

        >>> manager = MarketManager("Export.csv")
        >>> len(manager.search_by_distance("05828", 5)) >= 1
        True
        >>> manager.search_by_distance("00000", 30)
        []
        >>> len(manager.search_by_distance("05828", 30)) > 0
        True
        >>> manager.search_by_distance("05828", 30)[0][1] >= 0
        True
        """
        if radius < 0:
            return []

        point = self.get_user_zip_coordinates(zip_code)

        if point is None:
            return []

        result = []

        for market in self.markets:
            market_point = self.get_market_coordinates(market)

            if market_point is None:
                continue

            distance = self.calculate_distance(point, market_point)

            if distance <= radius:
                result.append((market, distance))

        result.sort(key=lambda item: item[1])
        return result

    def show_markets(self, review_manager, page=1, size=10, markets=None):
        """
        Выводит список рынков постранично вместе со средним рейтингом.

        Предусловия:
            review_manager — объект ReviewManager.
            page — номер страницы.
            size — количество записей на странице.

        Постусловия:
            Выводит выбранную страницу списка рынков.
        """
        if markets is None:
            markets = self.markets

        if len(markets) == 0:
            print("Нет рынков для отображения.")
            return

        total = len(markets)
        total_pages = (total + size - 1) // size
        page = max(1, min(page, total_pages))
        start = (page - 1) * size
        end = start + size
        page_data = markets[start:end]

        print("\n" + "=" * 82)
        print(
            f"{'FMID':<10} "
            f"{'NAME':<32} "
            f"{'CITY':<15} "
            f"{'STATE':<12} "
            f"{'RATING':<8}"
        )
        print("-" * 82)

        for market in page_data:
            rating = review_manager.calculate_average_rating(market.fmid)
            rating_text = "-" if rating == 0 else f"{rating:.1f}/5"

            print(
                f"{market.fmid:<10} "
                f"{market.name[:30]:<32} "
                f"{market.city[:13]:<15} "
                f"{market.state[:10]:<12} "
                f"{rating_text:<8}")

        print("-" * 82)
        print(
            f"Страница {page}/{total_pages} | "
            f"Размер страницы: {size} | Всего рынков: {total}")
        print("=" * 82)

class ReviewManager:
    """Управляет отзывами пользователей."""

    def __init__(self, filename):
        self.filename = filename
        self.reviews = []
        self.load_reviews()

    def load_reviews(self):
        """
        Загружает отзывы из CSV-файла.

        Постусловия:
            BOM и старое служебное поле ReviewID удаляются автоматически.
        """
        self.reviews = []

        try:
            with open(self.filename, encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    clean_row = {}

                    for key, value in row.items():
                        clean_key = key.lstrip("\ufeff") if key else key
                        clean_row[clean_key] = value

                    clean_row.pop("ReviewID", None)
                    self.reviews.append(clean_row)

        except FileNotFoundError:
            pass

    def save_reviews(self):
        """Сохраняет отзывы в CSV-файл."""
        with open(self.filename, "w", newline="", encoding="utf-8-sig") as file:
            fields = ["FMID", "Name", "Review", "Rating"]
            writer = csv.DictWriter(
                file,
                fieldnames=fields,
                extrasaction="ignore"
            )
            writer.writeheader()

            for review in self.reviews:
                writer.writerow(review)

    def add_review(self, market_id, name, text, rating):
        """
        Добавляет отзыв.

        Предусловия:
            rating — целое число от 1 до 5.

        Постусловия:
            Новый отзыв добавляется в self.reviews.

        >>> manager = ReviewManager.__new__(ReviewManager)
        >>> manager.reviews = []
        >>> manager.add_review("1", "Иван Иванов", "Хорошо", 5)
        >>> manager.reviews[0]["Rating"]
        '5'
        >>> manager.reviews[0]["FMID"]
        '1'
        """
        review = {
            "FMID": market_id,
            "Name": name,
            "Review": text,
            "Rating": str(rating)
        }
        self.reviews.append(review)

    def get_market_reviews(self, market_id):
        """
        Получает отзывы для выбранного рынка.

        >>> manager = ReviewManager.__new__(ReviewManager)
        >>> manager.reviews = [{"FMID":"1", "Rating":"5"}, {"FMID":"2", "Rating":"4"}]
        >>> len(manager.get_market_reviews("1"))
        1
        >>> manager.get_market_reviews("999")
        []
        """
        result = []

        for review in self.reviews:
            if review["FMID"] == market_id:
                result.append(review)

        return result

    def calculate_average_rating(self, market_id):
        """
        Вычисляет средний рейтинг рынка.

        Постусловия:
            Возвращает float. Если оценок нет, возвращает 0.

        >>> manager = ReviewManager.__new__(ReviewManager)
        >>> manager.reviews = [{"FMID":"1", "Rating":"5"}, {"FMID":"1", "Rating":"3"}, {"FMID":"2", "Rating":"4"}]
        >>> manager.calculate_average_rating("1")
        4.0
        >>> manager.calculate_average_rating("999")
        0
        """
        ratings = []

        for review in self.reviews:
            if review.get("FMID") == market_id:
                try:
                    ratings.append(int(review.get("Rating", 0)))
                except (ValueError, TypeError):
                    continue

        if len(ratings) == 0:
            return 0

        return sum(ratings) / len(ratings)

    def delete_review(self, market_id, review_number):
        """
        Удаляет отзыв выбранного рынка по порядковому номеру.

        Постусловия:
            Возвращает True при успешном удалении, иначе False.

        >>> manager = ReviewManager.__new__(ReviewManager)
        >>> manager.reviews = [{"FMID":"1", "Name":"A"}, {"FMID":"1", "Name":"B"}, {"FMID":"2", "Name":"C"}]
        >>> manager.delete_review("1", 2)
        True
        >>> len(manager.reviews)
        2
        >>> manager.delete_review("1", 10)
        False
        """
        market_reviews = self.get_market_reviews(market_id)

        if review_number < 1 or review_number > len(market_reviews):
            return False

        review_to_delete = market_reviews[review_number - 1]
        self.reviews.remove(review_to_delete)
        return True

class FarmMarketApp:
    """Консольное приложение для работы с фермерскими рынками."""

    def __init__(self, market_manager, review_manager):
        """Создает объект приложения."""
        self.market_manager = market_manager
        self.review_manager = review_manager


    def process_details(self):
        """Показывает подробную информацию о рынке по введенному FMID."""
        fmid = input(
            "\nВведите ID рынка для просмотра деталей "
            "(или Enter для выхода): ")

        if fmid == "":
            return

        market = self.market_manager.get_market_by_id(fmid)

        if market:
            reviews = self.review_manager.get_market_reviews(fmid)
            rating = self.review_manager.calculate_average_rating(fmid)
            market.full_info(rating, len(reviews))
        else:
            print("Рынок с таким FMID не найден!")

    def process_show(self):
        """Показывает список рынков с разбивкой по страницам."""
        page_size = 10
        total = len(self.market_manager.markets)

        if total == 0:
            print("Нет рынков для отображения.")
            return

        total_pages = (total + page_size - 1) // page_size

        print("\n=== Просмотр фермерских рынков ===")
        print("Всего рынков:", total)
        print("Размер страницы:", page_size)
        print(f"Доступные страницы: от 1 до {total_pages}")

        try:
            page = int(input(f"Введите номер страницы (1-{total_pages}): "))
        except ValueError:
            print("Введите номер страницы цифрами!")
            return

        if page < 1 or page > total_pages:
            print("Такой страницы нет!")
            return

        while True:
            self.market_manager.show_markets(
                self.review_manager,
                page,
                page_size
            )

            action = input(
                "\n[n] Следующая  [p] Предыдущая  "
                "[номер] Перейти на страницу  [q] Выход ==> ").lower()

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
        """Находит фермерский рынок по городу и штату."""
        city = input("Введите город: ").strip()
        state = input("Введите штат: ").strip()
        result = self.market_manager.search_by_city_state(city, state)

        if len(result) == 0:
            print("Рынки не найдены!")
        else:
            print("Найдено рынков:", len(result))

            for market in result:
                rating = self.review_manager.calculate_average_rating(market.fmid)
                rating_text = "нет оценок" if rating == 0 else f"{rating:.1f}/5"
                print(market.fmid, "-", market.name, "-", rating_text)

            self.process_details()

    def process_zip(self):
        """Находит фермерский рынок по индексу."""
        zip_code = input("Введите ZIP-код: ").strip()
        result = self.market_manager.search_by_zip(zip_code)

        if len(result) == 0:
            print("Рынки не найдены!")
        else:
            print("Найдено рынков:", len(result))

            for market in result:
                rating = self.review_manager.calculate_average_rating(market.fmid)
                rating_text = "нет оценок" if rating == 0 else f"{rating:.1f}/5"
                print(market.fmid, "-", market.name, "-", rating_text)

            self.process_details()

    def process_distance(self):
        """Поиск рынков в заданном радиусе."""
        zip_code = input("Введите ZIP-код: ").strip()

        if self.market_manager.get_user_zip_coordinates(zip_code) is None:
            print("Такой ZIP-код отсутствует в справочнике!")
            return

        try:
            radius = float(input("Введите радиус (в милях): "))
        except ValueError:
            print("Введите радиус числом!")
            return

        if radius < 0:
            print("Радиус не может быть отрицательным!")
            return

        result = self.market_manager.search_by_distance(zip_code, radius)

        if len(result) == 0:
            print("Рынки не найдены!")
        else:
            print("Найдено рынков:", len(result))

            for market, distance in result:
                rating = self.review_manager.calculate_average_rating(market.fmid)
                rating_text = "нет оценок" if rating == 0 else f"{rating:.1f}/5"

                print(
                    market.fmid, "-",
                    market.name, "-",
                    market.city, "-",
                    market.state, "-",
                    rating_text
                )
                print(f"Расстояние: {distance:.2f} миль.\n")

            self.process_details()

    @staticmethod
    def input_multiline_review():
        """
        Считывает многострочный отзыв.
        Точка в отдельной строке завершает ввод.
        """
        print(
            "Введите текст отзыва.\n"
            "Чтобы завершить ввод, введите точку в отдельной строке.")

        lines = []

        while True:
            line = input()
            if line == ".":
                break
            lines.append(line)

        return "\n".join(lines)

    def process_review(self):
        """Добавляет отзыв о рынке."""
        market_id = input("Введите FMID рынка (или Enter для выхода): ")

        if market_id == "":
            return

        market = self.market_manager.get_market_by_id(market_id)

        if market is None:
            print("Рынок не найден!")
            return

        name = input("Введите имя и фамилию: ").strip()

        if name == "":
            print("Имя и фамилия не могут быть пустыми!")
            return

        while True:
            try:
                rating = int(input("Оценка (1-5): "))
                if 1 <= rating <= 5:
                    break
                print("Оценка должна быть от 1 до 5.")
            except ValueError:
                print("Введите число!")

        text = self.input_multiline_review()
        self.review_manager.add_review(market_id, name, text, rating)
        self.review_manager.save_reviews()
        print("Отзыв успешно сохранён!")

    def process_reviews(self):
        """Показывает отзывы о рынке."""
        market_id = input("Введите FMID рынка: ")
        market = self.market_manager.get_market_by_id(market_id)

        if market is None:
            print("Рынок не найден!")
            return

        reviews = self.review_manager.get_market_reviews(market_id)

        if len(reviews) == 0:
            print("Для этого рынка пока нет отзывов :(")
        else:
            average = self.review_manager.calculate_average_rating(market_id)
            print(f"\nСредний рейтинг: {average:.1f} из 5")
            print("Отзывы о рынке:")
            print("-" * 40)

            for review in reviews:
                print("Автор:", review["Name"])
                print("Оценка:", review["Rating"], "/ 5")

                if review["Review"] != "":
                    print("Отзыв:")
                    print(review["Review"])

                print("-" * 40)

    def process_delete_review(self):
        """Удаляет выбранный отзыв о рынке."""
        market_id = input("Введите FMID рынка (или Enter для выхода): ")

        if market_id == "":
            return

        market = self.market_manager.get_market_by_id(market_id)

        if market is None:
            print("Рынок не найден!")
            return

        reviews = self.review_manager.get_market_reviews(market_id)

        if len(reviews) == 0:
            print("Для этого рынка нет отзывов!")
            return

        print("\nОтзывы о рынке:")
        print("-" * 40)

        for number, review in enumerate(reviews, start=1):
            print("Номер:", number)
            print("Автор:", review["Name"])
            print("Оценка:", review["Rating"], "/ 5")

            if review["Review"] != "":
                print("Отзыв:")
                print(review["Review"])

            print("-" * 40)

        try:
            review_number = int(input("Введите номер отзыва для удаления: "))
        except ValueError:
            print("Введите номер цифрами!")
            return

        confirm = input(
            "Вы действительно хотите удалить отзыв? (y/n): "
        ).lower()

        if confirm != "y":
            print("Удаление отменено.")
            return

        if self.review_manager.delete_review(market_id, review_number):
            self.review_manager.save_reviews()
            print("Отзыв удалён!")
        else:
            print("Отзыва с таким номером нет!")

    def process_delete_market(self):
        """Удаляет рынок и все связанные отзывы."""
        market_id = input("Введите FMID рынка (или Enter для выхода): ")

        if market_id == "":
            return

        market = self.market_manager.get_market_by_id(market_id)

        if market is None:
            print("Рынок не найден!")
            return

        reviews = self.review_manager.get_market_reviews(market_id)

        print("\nБудет удалён рынок:")
        print("Название:", market.name)
        print("Город:", market.city)
        print("Штат:", market.state)
        print("FMID:", market.fmid)
        print("Связанных отзывов:", len(reviews))

        confirm = input("Удалить рынок и все его отзывы? (y/n): ").lower()

        if confirm != "y":
            print("Удаление отменено.")
            return

        if self.market_manager.delete_market(market_id):
            reviews_to_delete = []

            for review in self.review_manager.reviews:
                if review["FMID"] == market_id:
                    reviews_to_delete.append(review)

            for review in reviews_to_delete:
                self.review_manager.reviews.remove(review)

            self.market_manager.save_data()
            self.review_manager.save_reviews()
            print("Рынок и связанные отзывы удалены!")
        else:
            print("Не удалось удалить рынок.")

    def process_delete(self):
        """Позволяет выбрать тип удаляемой записи."""
        print("\nЧто удалить?")
        print("1 - Отзыв")
        print("2 - Рынок")
        print("0 - Отмена")

        choice = input("Ваш выбор: ")

        if choice == "1":
            self.process_delete_review()
        elif choice == "2":
            self.process_delete_market()
        elif choice == "0":
            return
        else:
            print("Неверный выбор!")

    def process_sort(self):
        """Производит сортировку рынков по выбранному критерию."""
        print("\nВыберите поле для сортировки:")
        print("1 - Название рынка")
        print("2 - Город")
        print("3 - Штат")
        print("4 - Средний рейтинг")
        print("5 - Расстояние от ZIP-кода")

        choice = input("Ваш выбор: ")
        order = input("По возрастанию (a) или убыванию (d)? ").lower()

        if order not in ("a", "d"):
            print("Неверно указано направление сортировки!")
            return

        reverse = order == "d"

        if choice == "1":
            markets = self.market_manager.sort_markets("name", reverse)
        elif choice == "2":
            markets = self.market_manager.sort_markets("city", reverse)
        elif choice == "3":
            markets = self.market_manager.sort_markets("state", reverse)
        elif choice == "4":
            markets = sorted(
                self.market_manager.markets,
                key=lambda market: self.review_manager.calculate_average_rating(market.fmid),
                reverse=reverse)

        elif choice == "5":
            zip_code = input("Введите ZIP-код: ").strip()
            point = self.market_manager.get_user_zip_coordinates(zip_code)

            if point is None:
                print("Такой ZIP-код отсутствует в справочнике!")
                return

            markets_with_distance = []

            for market in self.market_manager.markets:
                market_point = self.market_manager.get_market_coordinates(market)

                if market_point is None:
                    continue

                distance = self.market_manager.calculate_distance(
                    point, market_point)

                markets_with_distance.append((market, distance))

            markets_with_distance.sort(
                key=lambda item: item[1],
                reverse=reverse)

            print("\nРынки, отсортированные по расстоянию:")

            for market, distance in markets_with_distance[:20]:
                print(
                    market.fmid, "-",
                    market.name, "-",
                    f"{distance:.2f} миль")

            print("Показаны первые 20 результатов.")
            return
        else:
            print("Неверный выбор!")
            return

        total_pages = (len(markets) + 9) // 10

        try:
            page = int(input(f"Введите номер страницы (1-{total_pages}): "))
        except ValueError:
            print("Введите номер страницы цифрами!")
            return

        if page < 1 or page > total_pages:
            print("Такой страницы нет!")
            return

        self.market_manager.show_markets(
            self.review_manager,
            markets=markets,
            page=page)

    def run(self):
        """Основной цикл работы программы."""
        show_welcome()

        while True:
            cmd = input(
                "\033[31mВВЕДИТЕ КОМАНДУ БЕЗ КАВЫЧЕК:\n\033[0m"
                "('show', 'search', 'zip', 'distance', 'details', 'delete', "
                "'review', 'sort', 'reviews', 'end', 'help') ==> "
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
            elif cmd == "details":
                self.process_details()
            elif cmd == "review":
                self.process_review()
            elif cmd == "reviews":
                self.process_reviews()
            elif cmd == "delete":
                self.process_delete()
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
\033[31mДоступные команды:\033[0m

\033[31mSHOW\033[0m - Показывает список фермерских
рынков с разбивкой по страницам

\033[31mSEARCH\033[0m - Находит фермерский рынок
по городу и штату

\033[31mZIP\033[0m - Находит фермерский рынок
по индексу

\033[31mDISTANCE\033[0m - Находит фермерский рынок
в указанном радиусе от заданного ZIP-кода

\033[31mDETAILS\033[0m - Показывает подробную информацию
о выбранном рынке

\033[31mDELETE\033[0m - Удалить рынок либо отзыв о рынке

\033[31mREVIEW\033[0m - Оставить отзыв о рынке

\033[31mSORT\033[0m - Отсортировать список рынков
по названию, городу, штату, рейтингу или расстоянию

\033[31mREVIEWS\033[0m - Просмотреть отзывы о рынке

\033[31mEND\033[0m - Завершает работу программы
{LINE}
""")


if __name__ == "__main__":
    if DEBUG:
        print(LINE)
        print("Running doctests...")
        print(LINE)

        failures, tests = doctest.testmod()

        print(f"Tests run: {tests}")
        print(f"Failures : {failures}")

    market_manager = MarketManager("Export.csv")
    review_manager = ReviewManager("reviews.csv")
    app = FarmMarketApp(market_manager, review_manager)
    app.run()
