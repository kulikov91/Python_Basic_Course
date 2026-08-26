import csv
import math
import doctest
import os
import json
import psycopg2

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


class Database:
    """Выполняет простые операции с PostgreSQL."""

    def __init__(self):
        """
        Создает подключение к PostgreSQL.

        Предусловия:
            PostgreSQL запущен, база данных существует.
            Параметры подключения переданы через переменные окружения
            или используются значения по умолчанию.

        Постусловия:
            Создано соединение self.connection.
        """
        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "farm_market"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        self.create_tables()

    def create_tables(self):
        """Создает таблицы приложения, если они еще не существуют."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS markets (
                    fmid VARCHAR(30) PRIMARY KEY,
                    data JSONB NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id SERIAL PRIMARY KEY,
                    fmid VARCHAR(30) NOT NULL
                        REFERENCES markets(fmid) ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    review TEXT NOT NULL DEFAULT '',
                    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS zip_coordinates (
                    zip_code VARCHAR(10) PRIMARY KEY,
                    latitude DOUBLE PRECISION NOT NULL,
                    longitude DOUBLE PRECISION NOT NULL
                )
            """)
        self.connection.commit()

    def table_is_empty(self, table_name):
        """Возвращает True, если указанная таблица пуста."""
        allowed = {"markets", "reviews", "zip_coordinates"}
        if table_name not in allowed:
            raise ValueError("Неизвестная таблица")
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0] == 0

    def import_initial_data(self):
        """
        Один раз переносит исходные CSV-данные в пустую базу PostgreSQL.

        Постусловия:
            Если таблицы пусты и соответствующие CSV-файлы существуют,
            данные добавляются в PostgreSQL.
        """
        if self.table_is_empty("markets") and os.path.exists("Export.csv"):
            with open("Export.csv", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                with self.connection.cursor() as cursor:
                    for row in reader:
                        cursor.execute(
                            "INSERT INTO markets (fmid, data) VALUES (%s, %s) "
                            "ON CONFLICT (fmid) DO NOTHING",
                            (row["FMID"], json.dumps(row))
                        )
            self.connection.commit()

        if self.table_is_empty("reviews") and os.path.exists("reviews.csv"):
            with open("reviews.csv", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                with self.connection.cursor() as cursor:
                    for row in reader:
                        fmid = row.get("FMID", "")
                        if not fmid:
                            continue
                        try:
                            rating = int(row.get("Rating", ""))
                        except (ValueError, TypeError):
                            continue
                        cursor.execute(
                            """INSERT INTO reviews (fmid, name, review, rating)
                               VALUES (%s, %s, %s, %s)
                               ON CONFLICT DO NOTHING""",
                            (fmid, row.get("Name", ""), row.get("Review", ""), rating)
                        )
            self.connection.commit()

        if (self.table_is_empty("zip_coordinates")
                and os.path.exists("zip_codes_states.csv")):
            with open("zip_codes_states.csv", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                with self.connection.cursor() as cursor:
                    for row in reader:
                        try:
                            cursor.execute(
                                """INSERT INTO zip_coordinates
                                   (zip_code, latitude, longitude)
                                   VALUES (%s, %s, %s)
                                   ON CONFLICT (zip_code) DO NOTHING""",
                                (row["zip_code"], float(row["latitude"]),
                                 float(row["longitude"]))
                            )
                        except (ValueError, TypeError):
                            continue
            self.connection.commit()

    def close(self):
        """Закрывает соединение с PostgreSQL."""
        self.connection.close()


class MarketManager:
    """Управляет фермерскими рынками, хранящимися в PostgreSQL."""

    def __init__(self, database):
        self.database = database
        self.markets = []
        self.zip_coordinates = {}
        self.load_data()
        self.load_zip_coordinates()

    def load_data(self):
        """Загружает рынки из PostgreSQL."""
        self.markets = []
        with self.database.connection.cursor() as cursor:
            cursor.execute("SELECT data FROM markets ORDER BY fmid")
            for row in cursor.fetchall():
                data = row[0]
                if isinstance(data, str):
                    data = json.loads(data)
                self.markets.append(Market(data))

    def save_data(self):
        """Синхронизирует текущий список рынков с PostgreSQL."""
        current_ids = [market.fmid for market in self.markets]
        with self.database.connection.cursor() as cursor:
            if current_ids:
                cursor.execute(
                    "DELETE FROM markets WHERE NOT (fmid = ANY(%s))",
                    (current_ids,)
                )
            else:
                cursor.execute("DELETE FROM markets")
            for market in self.markets:
                cursor.execute(
                    """INSERT INTO markets (fmid, data) VALUES (%s, %s)
                       ON CONFLICT (fmid) DO UPDATE SET data = EXCLUDED.data""",
                    (market.fmid, json.dumps(market.data))
                )
        self.database.connection.commit()

    def load_zip_coordinates(self):
        """Загружает координаты ZIP-кодов из PostgreSQL."""
        self.zip_coordinates = {}
        with self.database.connection.cursor() as cursor:
            cursor.execute(
                "SELECT zip_code, latitude, longitude FROM zip_coordinates"
            )
            for zip_code, latitude, longitude in cursor.fetchall():
                self.zip_coordinates[zip_code] = (latitude, longitude)

    def get_user_zip_coordinates(self, zip_code):
        """Возвращает координаты ZIP-кода или None."""
        return self.zip_coordinates.get(zip_code)

    def get_market_coordinates(self, market):
        """Возвращает координаты рынка или координаты его ZIP-кода."""
        point = market.coordinates()
        if point is not None:
            return point
        return self.zip_coordinates.get(market.zip)

    def search_by_zip(self, zip_code):
        """Ищет рынки по ZIP-коду."""
        return [market for market in self.markets if market.zip == zip_code]

    def search_by_city_state(self, city, state):
        """Ищет рынки по городу и штату."""
        required_state = normalize_state(state)
        return [
            market for market in self.markets
            if market.city.lower() == city.lower()
            and normalize_state(market.state) == required_state
        ]

    def get_market_by_id(self, fmid):
        """Возвращает рынок по FMID или None."""
        for market in self.markets:
            if market.fmid == fmid:
                return market
        return None

    def delete_market(self, fmid):
        """
        Удаляет рынок из списка.

        >>> manager = MarketManager.__new__(MarketManager)
        >>> manager.markets = [Market({"FMID":"1", "MarketName":"A", "city":"X", "State":"VT", "street":"", "zip":"1", "Website":"", "x":"", "y":""})]
        >>> manager.delete_market("1")
        True
        >>> manager.delete_market("999")
        False
        """
        market = self.get_market_by_id(fmid)
        if market is None:
            return False
        self.markets.remove(market)
        return True

    def sort_markets(self, field, reverse=False):
        """Возвращает новый список рынков, отсортированный по атрибуту."""
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
        """
        lat1 = math.radians(point1[0])
        lon1 = math.radians(point1[1])
        lat2 = math.radians(point2[0])
        lon2 = math.radians(point2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (math.sin(dlat / 2) ** 2
             + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 3959.3 * c

    def search_by_distance(self, zip_code, radius):
        """Ищет рынки в заданном радиусе."""
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
        """Выводит список рынков постранично вместе со средним рейтингом."""
        if markets is None:
            markets = self.markets
        if len(markets) == 0:
            print("Нет рынков для отображения.")
            return
        total = len(markets)
        total_pages = (total + size - 1) // size
        page = max(1, min(page, total_pages))
        page_data = markets[(page - 1) * size:page * size]
        print("\n" + "=" * 82)
        print(f"{'FMID':<10} {'NAME':<32} {'CITY':<15} {'STATE':<12} {'RATING':<8}")
        print("-" * 82)
        for market in page_data:
            rating = review_manager.calculate_average_rating(market.fmid)
            rating_text = "-" if rating == 0 else f"{rating:.1f}/5"
            print(f"{market.fmid:<10} {market.name[:30]:<32} "
                  f"{market.city[:13]:<15} {market.state[:10]:<12} {rating_text:<8}")
        print("-" * 82)
        print(f"Страница {page}/{total_pages} | Размер страницы: {size} | Всего рынков: {total}")
        print("=" * 82)


class ReviewManager:
    """Управляет отзывами, хранящимися в PostgreSQL."""

    def __init__(self, database):
        self.database = database
        self.reviews = []
        self.load_reviews()

    def load_reviews(self):
        """Загружает отзывы из PostgreSQL."""
        self.reviews = []
        with self.database.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, fmid, name, review, rating FROM reviews ORDER BY id"
            )
            for review_id, fmid, name, text, rating in cursor.fetchall():
                self.reviews.append({
                    "ReviewID": review_id,
                    "FMID": fmid,
                    "Name": name,
                    "Review": text,
                    "Rating": str(rating)
                })

    def save_reviews(self):
        """Синхронизирует текущий список отзывов с PostgreSQL."""
        with self.database.connection.cursor() as cursor:
            cursor.execute("DELETE FROM reviews")
            for review in self.reviews:
                cursor.execute(
                    """INSERT INTO reviews (fmid, name, review, rating)
                       VALUES (%s, %s, %s, %s)""",
                    (review["FMID"], review["Name"], review.get("Review", ""),
                     int(review["Rating"]))
                )
        self.database.connection.commit()
        self.load_reviews()

    def add_review(self, market_id, name, text, rating):
        """
        Добавляет отзыв в список.

        >>> manager = ReviewManager.__new__(ReviewManager)
        >>> manager.reviews = []
        >>> manager.add_review("1", "Иван Иванов", "Хорошо", 5)
        >>> manager.reviews[0]["Rating"]
        '5'
        """
        self.reviews.append({
            "FMID": market_id,
            "Name": name,
            "Review": text,
            "Rating": str(rating)
        })

    def get_market_reviews(self, market_id):
        """Возвращает отзывы выбранного рынка."""
        return [review for review in self.reviews if review["FMID"] == market_id]

    def calculate_average_rating(self, market_id):
        """
        Вычисляет средний рейтинг рынка.

        >>> manager = ReviewManager.__new__(ReviewManager)
        >>> manager.reviews = [{"FMID":"1", "Rating":"5"}, {"FMID":"1", "Rating":"3"}]
        >>> manager.calculate_average_rating("1")
        4.0
        """
        ratings = []
        for review in self.reviews:
            if review.get("FMID") == market_id:
                try:
                    ratings.append(int(review.get("Rating", 0)))
                except (ValueError, TypeError):
                    continue
        if not ratings:
            return 0
        return sum(ratings) / len(ratings)

    def delete_review(self, market_id, review_number):
        """Удаляет отзыв по его порядковому номеру для выбранного рынка."""
        market_reviews = self.get_market_reviews(market_id)
        if review_number < 1 or review_number > len(market_reviews):
            return False
        self.reviews.remove(market_reviews[review_number - 1])
        return True



import tkinter as tk
from tkinter import ttk, messagebox



class FarmMarketGUI:
    """
    Графическое приложение для работы с фермерскими рынками.

    Класс отвечает за оконный интерфейс.
    Работа с рынками выполняется через MarketManager,
    работа с отзывами — через ReviewManager.
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
            Создается графический интерфейс.
            В таблице отображается первая страница всех рынков.
        """
        self.root = root
        self.market_manager = market_manager
        self.review_manager = review_manager

        self.current_markets = list(self.market_manager.markets)
        self.current_distances = {}
        self.current_page = 1

        self.root.title("Фермерские рынки США")
        self.root.geometry("1180x760")
        self.root.minsize(960, 640)

        self.create_widgets()
        self.show_page(1)
        self.set_status(
            f"Загружено рынков: {len(self.market_manager.markets)}"
        )

    def create_widgets(self):
        """Создает элементы главного окна."""
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=12, pady=(12, 4))

        ttk.Label(
            title_frame,
            text="Фермерские рынки США",
            font=("Arial", 18, "bold")
        ).pack(side="left")

        ttk.Label(
            title_frame,
            text="GUI • ООП • CSV",
            font=("Arial", 10)
        ).pack(side="right", pady=(8, 0))

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

        ttk.Button(
            search_frame,
            text="Очистить поля",
            command=self.clear_search_fields
        ).grid(row=1, column=4, padx=5, pady=6)

        search_frame.columnconfigure(8, weight=1)

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

        columns = (
            "FMID", "Name", "City", "State", "Rating", "Distance"
        )

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

        self.tree.column("FMID", width=95, anchor="center", stretch=False)
        self.tree.column("Name", width=350)
        self.tree.column("City", width=160)
        self.tree.column("State", width=140)
        self.tree.column("Rating", width=90, anchor="center", stretch=False)
        self.tree.column("Distance", width=115, anchor="center", stretch=False)

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<Double-1>", lambda event: self.show_details())

        page_frame = ttk.Frame(self.root)
        page_frame.pack(fill="x", padx=12, pady=4)

        ttk.Button(
            page_frame,
            text="Предыдущая",
            command=self.previous_page
        ).pack(side="left")

        ttk.Button(
            page_frame,
            text="Следующая",
            command=self.next_page
        ).pack(side="left", padx=(6, 0))

        self.page_label = ttk.Label(page_frame, text="")
        self.page_label.pack(side="left", padx=14)

        ttk.Label(page_frame, text="Страница:").pack(side="left")
        self.page_entry = ttk.Entry(page_frame, width=6)
        self.page_entry.pack(side="left", padx=4)

        ttk.Button(
            page_frame,
            text="Перейти",
            command=self.go_to_page
        ).pack(side="left")

        action_frame = ttk.LabelFrame(self.root, text="Действия")
        action_frame.pack(fill="x", padx=12, pady=(6, 6))

        buttons = [
            ("Подробности", self.show_details),
            ("Отзывы", self.show_reviews),
            ("Добавить отзыв", self.add_review),
            ("Удалить отзыв", self.delete_review),
            ("Удалить рынок", self.delete_market)
        ]

        for button_text, command in buttons:
            ttk.Button(
                action_frame,
                text=button_text,
                command=command
            ).pack(side="left", padx=5, pady=8)

        self.status_label = ttk.Label(
            self.root,
            text="",
            anchor="w",
            relief="sunken"
        )
        self.status_label.pack(fill="x", side="bottom")

    def set_status(self, text):
        """Выводит сообщение в строке состояния."""
        self.status_label.config(text=" " + text)

    def clear_search_fields(self):
        """Очищает поля поиска."""
        self.city_entry.delete(0, "end")
        self.state_entry.delete(0, "end")
        self.zip_entry.delete(0, "end")
        self.radius_entry.delete(0, "end")
        self.set_status("Поля поиска очищены")

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
        """Отображает указанную страницу текущего списка рынков."""
        total = len(self.current_markets)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if total == 0:
            self.current_page = 1
            self.page_label.config(text="Рынки не найдены")
            self.page_entry.delete(0, "end")
            self.page_entry.insert(0, "1")
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
            rating_text = "-" if rating == 0 else f"{rating:.1f}/5"

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

        self.page_entry.delete(0, "end")
        self.page_entry.insert(0, str(page))

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

    def go_to_page(self):
        """Переходит к введенному номеру страницы."""
        if len(self.current_markets) == 0:
            return

        total_pages = (
            len(self.current_markets) + self.PAGE_SIZE - 1
        ) // self.PAGE_SIZE

        try:
            page = int(self.page_entry.get())
        except ValueError:
            messagebox.showerror(
                "Страница",
                "Введите номер страницы цифрами!"
            )
            return

        if page < 1 or page > total_pages:
            messagebox.showerror(
                "Страница",
                "Такой страницы нет!"
            )
            return

        self.show_page(page)

    def show_all(self):
        """Сбрасывает результаты поиска и показывает все рынки."""
        self.current_markets = list(self.market_manager.markets)
        self.current_distances = {}
        self.show_page(1)
        self.set_status(
            f"Показаны все рынки: {len(self.current_markets)}"
        )

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

        self.set_status(
            f"Поиск {city}, {state}: найдено {len(self.current_markets)}"
        )

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

        self.set_status(
            f"Поиск ZIP {zip_code}: найдено {len(self.current_markets)}"
        )

        if len(self.current_markets) == 0:
            messagebox.showinfo(
                "Результат поиска",
                "Рынки не найдены!"
            )

    def search_distance(self):
        """Ищет рынки в заданном радиусе от ZIP-кода."""
        zip_code = self.zip_entry.get().strip()

        if zip_code == "":
            messagebox.showwarning(
                "ZIP-код",
                "Введите ZIP-код."
            )
            return

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

        self.current_markets = [market for market, distance in result]
        self.current_distances = {
            market.fmid: distance
            for market, distance in result
        }

        self.show_page(1)
        self.set_status(
            f"ZIP {zip_code}, радиус {radius:g} миль: найдено {len(result)}"
        )

        if len(result) == 0:
            messagebox.showinfo(
                "Результат поиска",
                "Рынки не найдены!"
            )

    def sort_markets(self):
        """Сортирует текущий список рынков по выбранному критерию."""
        if len(self.current_markets) == 0:
            messagebox.showinfo(
                "Сортировка",
                "Нет рынков для сортировки."
            )
            return

        criterion = self.sort_combo.get()
        reverse = self.order_combo.get() == "По убыванию"

        if criterion == "Название рынка":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market: market.name.lower(),
                reverse=reverse
            )
            self.current_distances = {}

        elif criterion == "Город":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market: market.city.lower(),
                reverse=reverse
            )
            self.current_distances = {}

        elif criterion == "Штат":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market: market.state.lower(),
                reverse=reverse
            )
            self.current_distances = {}

        elif criterion == "Средний рейтинг":
            self.current_markets = sorted(
                self.current_markets,
                key=lambda market:
                    self.review_manager.calculate_average_rating(
                        market.fmid
                    ),
                reverse=reverse
            )
            self.current_distances = {}

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
                market for market, distance in markets_with_distance
            ]

            self.current_distances = {
                market.fmid: distance
                for market, distance in markets_with_distance
            }

        self.show_page(1)

        direction = (
            "по убыванию" if reverse else "по возрастанию"
        )
        self.set_status(
            f"Сортировка: {criterion}, {direction}"
        )

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
        window.geometry("720x600")
        window.transient(self.root)

        frame = ttk.Frame(window)
        frame.pack(fill="both", expand=True)

        text_widget = tk.Text(
            frame,
            wrap="word",
            padx=10,
            pady=10
        )

        scrollbar = ttk.Scrollbar(
            frame,
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

        ttk.Button(
            window,
            text="Закрыть",
            command=window.destroy
        ).pack(pady=8)

    def show_details(self):
        """Показывает подробную информацию о выбранном рынке."""
        market = self.get_selected_market()

        if market is None:
            return

        self.show_text_window(
            "Информация о рынке",
            self.build_details_text(market)
        )

        self.set_status(
            f"Открыта информация о рынке FMID {market.fmid}"
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
            lines.append(f"Автор: {review.get('Name', '')}")
            lines.append(f"Оценка: {review.get('Rating', '')} / 5")

            if review.get("Review", "") != "":
                lines.append("Отзыв:")
                lines.append(review["Review"])

            lines.append("-" * 40)

        self.show_text_window(
            f"Отзывы — {market.name}",
            "\n".join(lines)
        )

        self.set_status(
            f"Открыты отзывы рынка FMID {market.fmid}"
        )

    def add_review(self):
        """Открывает окно добавления многострочного отзыва."""
        market = self.get_selected_market()

        if market is None:
            return

        window = tk.Toplevel(self.root)
        window.title("Добавление отзыва")
        window.geometry("540x430")
        window.transient(self.root)
        window.grab_set()

        ttk.Label(
            window,
            text=market.name,
            font=("Arial", 12, "bold"),
            wraplength=490
        ).pack(pady=(12, 8))

        form = ttk.Frame(window)
        form.pack(fill="x", padx=12)

        ttk.Label(form, text="Имя и фамилия:").grid(
            row=0, column=0, sticky="w", pady=5
        )

        name_entry = ttk.Entry(form, width=40)
        name_entry.grid(
            row=0, column=1, sticky="ew", pady=5
        )

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
        rating_combo.grid(
            row=1, column=1, sticky="w", pady=5
        )

        form.columnconfigure(1, weight=1)

        ttk.Label(
            window,
            text="Текст отзыва (можно оставить пустым):"
        ).pack(
            anchor="w",
            padx=12,
            pady=(8, 3)
        )

        review_text = tk.Text(
            window,
            height=10,
            wrap="word"
        )
        review_text.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 8)
        )

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

            window.destroy()
            self.show_page(self.current_page)

            messagebox.showinfo(
                "Отзыв",
                "Отзыв успешно сохранён!"
            )

            self.set_status(
                f"Добавлен отзыв для рынка FMID {market.fmid}"
            )

        button_frame = ttk.Frame(window)
        button_frame.pack(pady=(0, 12))

        ttk.Button(
            button_frame,
            text="Сохранить",
            command=save
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=window.destroy
        ).pack(side="left", padx=5)

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
        window.geometry("720x460")
        window.transient(self.root)
        window.grab_set()

        ttk.Label(
            window,
            text=f"Отзывы: {market.name}",
            font=("Arial", 12, "bold"),
            wraplength=670
        ).pack(pady=10)

        listbox = tk.Listbox(
            window,
            height=14,
            exportselection=False
        )
        listbox.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=6
        )

        for number, review in enumerate(reviews, start=1):
            review_text_value = review.get(
                "Review", ""
            ).replace("\n", " ")

            if len(review_text_value) > 65:
                review_text_value = (
                    review_text_value[:62] + "..."
                )

            listbox.insert(
                "end",
                (
                    f"{number}. {review.get('Name', '')} | "
                    f"{review.get('Rating', '')}/5 | "
                    f"{review_text_value}"
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

                self.set_status(
                    f"Удалён отзыв рынка FMID {market.fmid}"
                )

        button_frame = ttk.Frame(window)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Удалить выбранный отзыв",
            command=remove
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=window.destroy
        ).pack(side="left", padx=5)

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

            self.set_status(
                f"Удалён рынок FMID {market.fmid}"
            )


def run_gui():
    """Подключается к PostgreSQL, создает менеджеры и запускает GUI."""
    try:
        database = Database()
        database.import_initial_data()
        market_manager = MarketManager(database)
        review_manager = ReviewManager(database)
    except psycopg2.Error as error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Ошибка PostgreSQL",
            "Не удалось подключиться к базе данных.\n\n" + str(error)
        )
        root.destroy()
        return

    root = tk.Tk()
    FarmMarketGUI(
        root,
        market_manager,
        review_manager
    )
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
