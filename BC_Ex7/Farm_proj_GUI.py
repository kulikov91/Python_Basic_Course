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
            * math.sin(dlon / 2) ** 2
        )

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
                f"{rating_text:<8}"
            )

        print("-" * 82)
        print(
            f"Страница {page}/{total_pages} | "
            f"Размер страницы: {size} | Всего рынков: {total}"
        )
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

import tkinter as tk
from tkinter import ttk, messagebox

class FarmMarketGUI:
    """
    Графическое приложение для работы с фермерскими рынками.

    Класс отвечает только за пользовательский интерфейс.
    Работа с рынками и отзывами выполняется через
    MarketManager и ReviewManager.
    """

    PAGE_SIZE = 10

    def __init__(self, root, market_manager, review_manager):
        """
        Создает главное окно приложения.

        Предусловия:
            root — объект tkinter.Tk.
            market_manager — объект MarketManager.
            review_manager — объект ReviewManager.

        Постусловия:
            Создается графический интерфейс и отображается
            первая страница списка рынков.
        """
        self.root = root
        self.market_manager = market_manager
        self.review_manager = review_manager

        self.current_markets = list(self.market_manager.markets)
        self.current_distances = {}
        self.current_page = 1

        self.root.title("Фермерские рынки США")
        self.root.geometry("1120x700")
        self.root.minsize(900, 600)

        self.create_widgets()
        self.show_page(1)

    def create_widgets(self):
        """Создает элементы главного окна."""
        title = ttk.Label(
            self.root,
            text="Фермерские рынки США",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(12, 8))

        search_frame = ttk.LabelFrame(self.root, text="Поиск")
        search_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(search_frame, text="Город:").grid(
            row=0, column=0, padx=5, pady=6, sticky="e"
        )
        self.city_entry = ttk.Entry(search_frame, width=18)
        self.city_entry.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(search_frame, text="Штат:").grid(
            row=0, column=2, padx=5, pady=6, sticky="e"
        )
        self.state_entry = ttk.Entry(search_frame, width=12)
        self.state_entry.grid(row=0, column=3, padx=5, pady=6)

        ttk.Button(
            search_frame,
            text="Город + штат",
            command=self.search_city_state
        ).grid(row=0, column=4, padx=5, pady=6)

        ttk.Label(search_frame, text="ZIP:").grid(
            row=0, column=5, padx=5, pady=6, sticky="e"
        )
        self.zip_entry = ttk.Entry(search_frame, width=10)
        self.zip_entry.grid(row=0, column=6, padx=5, pady=6)

        ttk.Button(
            search_frame,
            text="По ZIP",
            command=self.search_zip
        ).grid(row=0, column=7, padx=5, pady=6)

        ttk.Label(search_frame, text="Радиус, миль:").grid(
            row=1, column=0, padx=5, pady=6, sticky="e"
        )
        self.radius_entry = ttk.Entry(search_frame, width=10)
        self.radius_entry.grid(row=1, column=1, padx=5, pady=6)

        ttk.Button(
            search_frame,
            text="По расстоянию",
            command=self.search_distance
        ).grid(row=1, column=2, padx=5, pady=6)

        ttk.Button(
            search_frame,
            text="Показать все",
            command=self.show_all
        ).grid(row=1, column=3, padx=5, pady=6)

        sort_frame = ttk.LabelFrame(self.root, text="Сортировка")
        sort_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(sort_frame, text="Критерий:").pack(
            side="left", padx=(8, 4), pady=6
        )

        self.sort_combo = ttk.Combobox(
            sort_frame,
            state="readonly",
            width=24,
            values=[
                "Название рынка",
                "Город",
                "Штат",
                "Средний рейтинг",
                "Расстояние от ZIP-кода"
            ]
        )
        self.sort_combo.current(0)
        self.sort_combo.pack(side="left", padx=4, pady=6)

        self.order_combo = ttk.Combobox(
            sort_frame,
            state="readonly",
            width=16,
            values=["По возрастанию", "По убыванию"]
        )
        self.order_combo.current(0)
        self.order_combo.pack(side="left", padx=4, pady=6)

        ttk.Button(
            sort_frame,
            text="Сортировать",
            command=self.sort_markets
        ).pack(side="left", padx=8, pady=6)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=12, pady=6)

        columns = ("FMID", "Name", "City", "State", "Rating", "Distance")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("FMID", text="FMID")
        self.tree.heading("Name", text="Название")
        self.tree.heading("City", text="Город")
        self.tree.heading("State", text="Штат")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.heading("Distance", text="Расстояние")

        self.tree.column("FMID", width=90, anchor="center")
        self.tree.column("Name", width=310)
        self.tree.column("City", width=150)
        self.tree.column("State", width=130)
        self.tree.column("Rating", width=90, anchor="center")
        self.tree.column("Distance", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda event: self.show_details())

        page_frame = ttk.Frame(self.root)
        page_frame.pack(fill="x", padx=12, pady=4)

        ttk.Button(
            page_frame,
            text="Предыдущая",
            command=self.previous_page
        ).pack(side="left")

        self.page_label = ttk.Label(page_frame, text="")
        self.page_label.pack(side="left", padx=12)

        ttk.Button(
            page_frame,
            text="Следующая",
            command=self.next_page
        ).pack(side="left")

        action_frame = ttk.LabelFrame(self.root, text="Действия")
        action_frame.pack(fill="x", padx=12, pady=(6, 12))

        buttons = [
            ("Подробности", self.show_details),
            ("Отзывы", self.show_reviews),
            ("Добавить отзыв", self.add_review),
            ("Удалить отзыв", self.delete_review),
            ("Удалить рынок", self.delete_market)
        ]

        for text, command in buttons:
            ttk.Button(
                action_frame,
                text=text,
                command=command
            ).pack(side="left", padx=5, pady=8)

    def get_selected_market(self):
        """
        Возвращает выбранный в таблице рынок.

        Постусловия:
            Возвращает объект Market или None.
        """
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Не выбран рынок",
                "Выберите рынок в таблице."
            )
            return None

        values = self.tree.item(selected[0], "values")

        if not values:
            return None

        return self.market_manager.get_market_by_id(str(values[0]))

    def show_page(self, page):
        """
        Отображает указанную страницу текущего списка рынков.
        """
        total = len(self.current_markets)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if total == 0:
            self.current_page = 1
            self.page_label.config(text="Рынки не найдены")
            return

        total_pages = (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE
        page = max(1, min(page, total_pages))
        self.current_page = page

        start = (page - 1) * self.PAGE_SIZE
        end = start + self.PAGE_SIZE

        for market in self.current_markets[start:end]:
            rating = self.review_manager.calculate_average_rating(
                market.fmid
            )

            if rating == 0:
                rating_text = "-"
            else:
                rating_text = f"{rating:.1f}/5"

            if market.fmid in self.current_distances:
                distance_text = (
                    f"{self.current_distances[market.fmid]:.2f} миль"
                )
            else:
                distance_text = ""

            self.tree.insert(
                "",
                "end",
                values=(
                    market.fmid,
                    market.name,
                    market.city,
                    market.state,
                    rating_text,
                    distance_text
                )
            )

        self.page_label.config(
            text=(
                f"Страница {page}/{total_pages} | "
                f"Размер страницы: {self.PAGE_SIZE} | "
                f"Всего рынков: {total}"
            )
        )

    def previous_page(self):
        """Показывает предыдущую страницу."""
        if self.current_page > 1:
            self.show_page(self.current_page - 1)

    def next_page(self):
        """Показывает следующую страницу."""
        total_pages = (
            len(self.current_markets) + self.PAGE_SIZE - 1
        ) // self.PAGE_SIZE

        if self.current_page < total_pages:
            self.show_page(self.current_page + 1)

    def show_all(self):
        """Сбрасывает поиск и показывает все рынки."""
        self.current_markets = list(self.market_manager.markets)
        self.current_distances = {}
        self.show_page(1)

    def search_city_state(self):
        """Ищет рынки по городу и штату."""
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()

        if city == "" or state == "":
            messagebox.showwarning(
                "Недостаточно данных",
                "Введите город и штат."
            )
            return

        self.current_markets = self.market_manager.search_by_city_state(
            city,
            state
        )
        self.current_distances = {}
        self.show_page(1)

        if len(self.current_markets) == 0:
            messagebox.showinfo(
                "Результат поиска",
                "Рынки не найдены!"
            )

    def search_zip(self):
        """Ищет рынки по ZIP-коду."""
        zip_code = self.zip_entry.get().strip()

        if zip_code == "":
            messagebox.showwarning(
                "ZIP-код",
                "Введите ZIP-код."
            )
            return

        self.current_markets = self.market_manager.search_by_zip(
            zip_code
        )
        self.current_distances = {}
        self.show_page(1)

        if len(self.current_markets) == 0:
            messagebox.showinfo(
                "Результат поиска",
                "Рынки не найдены!"
            )

    def search_distance(self):
        """Ищет рынки в заданном радиусе от ZIP-кода."""
        zip_code = self.zip_entry.get().strip()

        if self.market_manager.get_user_zip_coordinates(zip_code) is None:
            messagebox.showerror(
                "ZIP-код",
                "Такой ZIP-код отсутствует в справочнике!"
            )
            return

        try:
            radius = float(self.radius_entry.get())
        except ValueError:
            messagebox.showerror(
                "Радиус",
                "Введите радиус числом!"
            )
            return

        if radius < 0:
            messagebox.showerror(
                "Радиус",
                "Радиус не может быть отрицательным!"
            )
            return

        result = self.market_manager.search_by_distance(
            zip_code,
            radius
        )

        self.current_markets = [item[0] for item in result]
        self.current_distances = {
            market.fmid: distance
            for market, distance in result
        }

        self.show_page(1)

        if len(result) == 0:
            messagebox.showinfo(
                "Результат поиска",
                "Рынки не найдены!"
            )

    def sort_markets(self):
        """Сортирует текущий список рынков по выбранному критерию."""
        criterion = self.sort_combo.get()
        reverse = self.order_combo.get() == "По убыванию"

        if criterion == "Название рынка":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market: market.name.lower(),
                reverse=reverse
            )

        elif criterion == "Город":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market: market.city.lower(),
                reverse=reverse
            )

        elif criterion == "Штат":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market: market.state.lower(),
                reverse=reverse
            )

        elif criterion == "Средний рейтинг":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market:
                    self.review_manager.calculate_average_rating(
                        market.fmid
                    ),
                reverse=reverse
            )

        elif criterion == "Расстояние от ZIP-кода":
            zip_code = self.zip_entry.get().strip()
            point = self.market_manager.get_user_zip_coordinates(
                zip_code
            )

            if point is None:
                messagebox.showerror(
                    "ZIP-код",
                    "Такой ZIP-код отсутствует в справочнике!"
                )
                return

            markets_with_distance = []

            for market in self.current_markets:
                market_point = (
                    self.market_manager.get_market_coordinates(market)
                )

                if market_point is None:
                    continue

                distance = self.market_manager.calculate_distance(
                    point,
                    market_point
                )
                markets_with_distance.append((market, distance))

            markets_with_distance.sort(
                key=lambda item: item[1],
                reverse=reverse
            )

            self.current_markets = [
                market
                for market, distance in markets_with_distance
            ]
            self.current_distances = {
                market.fmid: distance
                for market, distance in markets_with_distance
            }

        self.show_page(1)

    def build_details_text(self, market):
        """Возвращает подробную информацию о рынке в виде строки."""
        lines = [
            "=== Информация о рынке ===",
            f"Название: {market.name}",
            f"Город: {market.city}",
            f"Штат: {market.state}",
            f"Адрес: {market.street}",
            f"Индекс: {market.zip}",
            f"Сайт: {market.website}",
            "",
            "=== Категории товаров ==="
        ]

        product_fields = [
            "Organic", "Bakedgoods", "Cheese", "Crafts", "Flowers",
            "Eggs", "Seafood", "Herbs", "Vegetables", "Honey",
            "Jams", "Maple", "Meat", "Nursery", "Nuts", "Plants",
            "Poultry", "Prepared", "Soap", "Trees", "Wine", "Coffee",
            "Beans", "Fruits", "Grains", "Juices", "Mushrooms",
            "PetFood", "Tofu", "WildHarvested"
        ]

        for field in product_fields:
            if field in market.data:
                value = market.data[field].strip()

                if value != "":
                    lines.append(f"{field}: {value}")

        lines.extend(["", "=== Оплата и программы ==="])

        payment_fields = ["Credit", "WIC", "WICcash", "SFMNP", "SNAP"]

        for field in payment_fields:
            if field in market.data:
                value = market.data[field].strip()

                if value != "":
                    lines.append(f"{field}: {value}")

        rating = self.review_manager.calculate_average_rating(
            market.fmid
        )
        reviews = self.review_manager.get_market_reviews(
            market.fmid
        )

        lines.extend(["", "=== Рейтинг ==="])

        if rating == 0:
            lines.append("Средний рейтинг: нет оценок")
        else:
            lines.append(f"Средний рейтинг: {rating:.1f} из 5")

        lines.append(f"Количество отзывов: {len(reviews)}")

        return "\n".join(lines)

    def show_text_window(self, title, text):
        """Открывает окно с многострочным текстом."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("700x600")

        text_widget = tk.Text(
            window,
            wrap="word",
            padx=10,
            pady=10
        )
        scrollbar = ttk.Scrollbar(
            window,
            orient="vertical",
            command=text_widget.yview
        )
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(
            side="left",
            fill="both",
            expand=True
        )
        scrollbar.pack(side="right", fill="y")

        text_widget.insert("1.0", text)
        text_widget.configure(state="disabled")

    def show_details(self):
        """Показывает подробную информацию о выбранном рынке."""
        market = self.get_selected_market()

        if market is None:
            return

        self.show_text_window(
            "Информация о рынке",
            self.build_details_text(market)
        )

    def show_reviews(self):
        """Показывает отзывы о выбранном рынке."""
        market = self.get_selected_market()

        if market is None:
            return

        reviews = self.review_manager.get_market_reviews(
            market.fmid
        )

        if len(reviews) == 0:
            messagebox.showinfo(
                "Отзывы",
                "Для этого рынка пока нет отзывов :("
            )
            return

        average = self.review_manager.calculate_average_rating(
            market.fmid
        )

        lines = [
            f"Средний рейтинг: {average:.1f} из 5",
            "",
            "Отзывы о рынке:",
            "-" * 40
        ]

        for review in reviews:
            lines.append(f"Автор: {review['Name']}")
            lines.append(f"Оценка: {review['Rating']} / 5")

            if review.get("Review", "") != "":
                lines.append("Отзыв:")
                lines.append(review["Review"])

            lines.append("-" * 40)

        self.show_text_window(
            f"Отзывы — {market.name}",
            "\n".join(lines)
        )

    def add_review(self):
        """Открывает окно добавления отзыва."""
        market = self.get_selected_market()

        if market is None:
            return

        window = tk.Toplevel(self.root)
        window.title("Добавление отзыва")
        window.geometry("520x420")
        window.transient(self.root)
        window.grab_set()

        ttk.Label(
            window,
            text=market.name,
            font=("Arial", 12, "bold"),
            wraplength=470
        ).pack(pady=(12, 8))

        form = ttk.Frame(window)
        form.pack(fill="x", padx=12)

        ttk.Label(form, text="Имя и фамилия:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        name_entry = ttk.Entry(form, width=40)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Оценка:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        rating_combo = ttk.Combobox(
            form,
            state="readonly",
            values=["1", "2", "3", "4", "5"],
            width=8
        )
        rating_combo.current(4)
        rating_combo.grid(row=1, column=1, sticky="w", pady=5)

        form.columnconfigure(1, weight=1)

        ttk.Label(window, text="Текст отзыва:").pack(
            anchor="w",
            padx=12,
            pady=(8, 3)
        )

        review_text = tk.Text(window, height=10, wrap="word")
        review_text.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        def save():
            name = name_entry.get().strip()

            if name == "":
                messagebox.showerror(
                    "Ошибка",
                    "Имя и фамилия не могут быть пустыми!",
                    parent=window
                )
                return

            rating = int(rating_combo.get())
            text = review_text.get("1.0", "end-1c")

            self.review_manager.add_review(
                market.fmid,
                name,
                text,
                rating
            )
            self.review_manager.save_reviews()

            messagebox.showinfo(
                "Отзыв",
                "Отзыв успешно сохранён!",
                parent=window
            )
            window.destroy()
            self.show_page(self.current_page)

        ttk.Button(
            window,
            text="Сохранить",
            command=save
        ).pack(pady=(0, 12))

    def delete_review(self):
        """Удаляет выбранный отзыв выбранного рынка."""
        market = self.get_selected_market()

        if market is None:
            return

        reviews = self.review_manager.get_market_reviews(
            market.fmid
        )

        if len(reviews) == 0:
            messagebox.showinfo(
                "Удаление отзыва",
                "Для этого рынка нет отзывов!"
            )
            return

        window = tk.Toplevel(self.root)
        window.title("Удаление отзыва")
        window.geometry("700x450")
        window.transient(self.root)
        window.grab_set()

        ttk.Label(
            window,
            text=f"Отзывы: {market.name}",
            font=("Arial", 12, "bold"),
            wraplength=650
        ).pack(pady=10)

        listbox = tk.Listbox(window, height=14)
        listbox.pack(fill="both", expand=True, padx=12, pady=6)

        for number, review in enumerate(reviews, start=1):
            review_text = review.get("Review", "").replace("\n", " ")
            if len(review_text) > 60:
                review_text = review_text[:57] + "..."

            listbox.insert(
                "end",
                (
                    f"{number}. {review.get('Name', '')} | "
                    f"{review.get('Rating', '')}/5 | {review_text}"
                )
            )

        def remove():
            selection = listbox.curselection()

            if not selection:
                messagebox.showwarning(
                    "Удаление",
                    "Выберите отзыв.",
                    parent=window
                )
                return

            number = selection[0] + 1

            if not messagebox.askyesno(
                "Подтверждение",
                "Вы действительно хотите удалить отзыв?",
                parent=window
            ):
                return

            if self.review_manager.delete_review(
                market.fmid,
                number
            ):
                self.review_manager.save_reviews()
                window.destroy()
                self.show_page(self.current_page)
                messagebox.showinfo(
                    "Удаление",
                    "Отзыв удалён!"
                )

        ttk.Button(
            window,
            text="Удалить выбранный отзыв",
            command=remove
        ).pack(pady=10)

    def delete_market(self):
        """Удаляет выбранный рынок и все связанные отзывы."""
        market = self.get_selected_market()

        if market is None:
            return

        reviews = self.review_manager.get_market_reviews(
            market.fmid
        )

        message = (
            f"Будет удалён рынок:\n\n"
            f"Название: {market.name}\n"
            f"Город: {market.city}\n"
            f"Штат: {market.state}\n"
            f"FMID: {market.fmid}\n"
            f"Связанных отзывов: {len(reviews)}\n\n"
            f"Удалить рынок и все его отзывы?"
        )

        if not messagebox.askyesno(
            "Удаление рынка",
            message
        ):
            return

        if self.market_manager.delete_market(market.fmid):
            reviews_to_delete = []

            for review in self.review_manager.reviews:
                if review.get("FMID") == market.fmid:
                    reviews_to_delete.append(review)

            for review in reviews_to_delete:
                self.review_manager.reviews.remove(review)

            self.market_manager.save_data()
            self.review_manager.save_reviews()

            self.current_markets = [
                item
                for item in self.current_markets
                if item.fmid != market.fmid
            ]
            self.current_distances.pop(market.fmid, None)

            self.show_page(self.current_page)

            messagebox.showinfo(
                "Удаление рынка",
                "Рынок и связанные отзывы удалены!"
            )


def run_gui():
    """Создает менеджеры и запускает GUI-приложение."""
    market_manager = MarketManager("Export.csv")
    review_manager = ReviewManager("reviews.csv")

    root = tk.Tk()
    FarmMarketGUI(root, market_manager, review_manager)
    root.mainloop()


if __name__ == "__main__":

    if DEBUG:
        print(LINE)
        print("Running doctests...")
        print(LINE)

        failures, tests = doctest.testmod()

        print(f"Tests run: {tests}")
        print(f"Failures : {failures}")

    run_gui()