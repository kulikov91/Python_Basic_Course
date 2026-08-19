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


def load_data(filename):
    """
    Загружает данные о фермерских рынках из CSV-файла.

    Предусловия:
        filename — имя существующего CSV-файла.

    Постусловия:
        Возвращает список словарей, где каждый словарь
        соответствует одной записи CSV.
    """
    markets = []

    with open(filename, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            markets.append(row)

    return markets


def save_markets(filename, markets):
    """
    Сохраняет список рынков в CSV-файл.

    Предусловия:
        markets — список словарей одинаковой структуры.
        filename — имя CSV-файла.

    Постусловия:
        Файл перезаписывается актуальным списком рынков.
    """
    if len(markets) == 0:
        return

    fields = markets[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(markets)


def delete_market(markets, reviews, market_id):
    """
    Удаляет рынок и все связанные с ним отзывы.

    Предусловия:
        markets — список рынков.
        reviews — список отзывов.
        market_id — строка с FMID рынка.

    Постусловия:
        Если рынок найден, он удаляется вместе с отзывами
        и функция возвращает True.
        Если рынок не найден, возвращает False.

    >>> markets = [
    ...     {"FMID": "1", "MarketName": "Market A"},
    ...     {"FMID": "2", "MarketName": "Market B"}
    ... ]
    >>> reviews = [
    ...     {"FMID": "1", "Name": "Иван", "Review": "", "Rating": "5"},
    ...     {"FMID": "2", "Name": "Анна", "Review": "", "Rating": "4"}
    ... ]
    >>> delete_market(markets, reviews, "1")
    True
    >>> len(markets)
    1
    >>> markets[0]["FMID"]
    '2'
    >>> len(reviews)
    1
    >>> delete_market(markets, reviews, "999")
    False
    """
    market = get_market_by_id(markets, market_id)

    if market is None:
        return False

    markets.remove(market)

    reviews_to_delete = []

    for review in reviews:
        if review["FMID"] == market_id:
            reviews_to_delete.append(review)

    for review in reviews_to_delete:
        reviews.remove(review)

    return True


def process_delete_market(markets, reviews):
    """
    Удаляет выбранный рынок и связанные с ним отзывы.

    Предусловия:
        markets — список рынков.
        reviews — список отзывов.

    Постусловия:
        При подтверждении рынок удаляется из Export.csv,
        а связанные отзывы — из reviews.csv.
    """
    market_id = input("Введите FMID рынка (или Enter для выхода): ")

    if market_id == "":
        return

    market = get_market_by_id(markets, market_id)

    if market is None:
        print("Рынок не найден!")
        return

    print("\nБудет удалён рынок:")
    print("Название:", market["MarketName"])
    print("Город:", market["city"])
    print("Штат:", market["State"])
    print("FMID:", market["FMID"])

    market_reviews = get_market_reviews(reviews, market_id)
    print("Связанных отзывов:", len(market_reviews))

    confirm = input("Удалить рынок и все его отзывы? (y/n): ").lower()

    if confirm != "y":
        print("Удаление отменено.")
        return

    deleted = delete_market(markets, reviews, market_id)

    if deleted:
        save_markets("Export.csv", markets)
        save_reviews("reviews.csv", reviews)
        print("Рынок и связанные отзывы удалены!")
    else:
        print("Не удалось удалить рынок.")


def process_delete(markets, reviews):
    """
    Позволяет выбрать тип удаляемой записи.
    """
    print("\nЧто удалить?")
    print("1 - Отзыв")
    print("2 - Рынок")
    print("0 - Отмена")

    choice = input("Ваш выбор: ")

    if choice == "1":
        process_delete_review(markets, reviews)
    elif choice == "2":
        process_delete_market(markets, reviews)
    elif choice == "0":
        return
    else:
        print("Неверный выбор!")


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


def calculate_average_rating(reviews, market_id):
    """
    Вычисляет средний рейтинг рынка.

    Предусловия:
        reviews — список отзывов.
        market_id — строка с FMID рынка.

    Постусловия:
        Возвращает средний рейтинг в виде числа float.
        Если оценок нет, возвращает 0.

    >>> reviews = [
    ...     {"FMID": "1", "Name": "Иван", "Review": "", "Rating": "5"},
    ...     {"FMID": "1", "Name": "Петр", "Review": "", "Rating": "3"},
    ...     {"FMID": "2", "Name": "Анна", "Review": "", "Rating": "4"}
    ... ]
    >>> calculate_average_rating(reviews, "1")
    4.0
    >>> calculate_average_rating(reviews, "2")
    4.0
    >>> calculate_average_rating(reviews, "999")
    0
    """
    ratings = []

    for review in reviews:
        if review["FMID"] == market_id:
            try:
                ratings.append(int(review["Rating"]))
            except (ValueError, TypeError):
                continue

    if len(ratings) == 0:
        return 0

    return sum(ratings) / len(ratings)


def show_markets(markets, reviews, page=1, size=10):
    """
    Выводит список рынков постранично.

    Предусловия:
        markets — список рынков.
        reviews — список отзывов.
        page — номер страницы, начиная с 1.
        size — количество записей на странице.

    Постусловия:
        Выводит выбранную страницу списка рынков.
    """
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
        rating = calculate_average_rating(reviews, market["FMID"])

        if rating == 0:
            rating_text = "-"
        else:
            rating_text = f"{rating:.1f}/5"

        print(
            f"{market['FMID']:<10} "
            f"{market['MarketName'][:30]:<32} "
            f"{market['city'][:13]:<15} "
            f"{market['State'][:10]:<12} "
            f"{rating_text:<8}"
        )

    print("-" * 82)
    print(
        f"Страница {page}/{total_pages} | "
        f"Размер страницы: {size} | "
        f"Всего рынков: {total}"
    )
    print("=" * 82)


def search_by_city_state(markets, city, state):
    """
    Поиск рынков по городу и штату.
    Штат можно вводить полным названием или двухбуквенным кодом.

    Предусловия:
        markets — список рынков.
        city — строка с названием города.
        state — полное название штата или его код.

    Постусловия:
        Возвращает список найденных рынков.
        Исходный список markets не изменяется.

    >>> markets = load_data("Export.csv")
    >>> len(search_by_city_state(markets, "Danville", "Vermont")) > 0
    True
    >>> len(search_by_city_state(markets, "Danville", "VT")) > 0
    True
    >>> search_by_city_state(markets, "danville", "vt")[0]["State"]
    'Vermont'
    >>> search_by_city_state(markets, "Unknown City", "VT")
    []
    """
    required_state_code = normalize_state(state)

    result = filter(
        lambda market:
        market["city"].lower() == city.lower()
        and normalize_state(market["State"]) == required_state_code,
        markets
    )

    return list(result)


def search_by_zip(markets, zip_code):
    """
    Ищет рынки по почтовому индексу.

    Предусловия:
        markets — список рынков.
        zip_code — ZIP-код в виде строки.

    Постусловия:
        Возвращает список найденных рынков.

    >>> markets = load_data("Export.csv")
    >>> len(search_by_zip(markets, "05828")) > 0
    True
    >>> len(search_by_zip(markets, "99999"))
    0
    >>> search_by_zip(markets, "05828")[0]["zip"]
    '05828'
    """
    result = []

    for market in markets:
        if market["zip"] == zip_code:
            result.append(market)

    return result


def get_coordinates_by_zip(zip_coordinates, zip_code):
    """
    Возвращает координаты указанного ZIP-кода.

    Предусловия:
        zip_coordinates — словарь координат ZIP-кодов.
        zip_code — строка с ZIP-кодом.

    Постусловия:
        Возвращает кортеж (широта, долгота),
        либо None, если ZIP-код отсутствует.

    >>> coordinates = {"05828": (44.4111, -72.1428)}
    >>> get_coordinates_by_zip(coordinates, "05828")
    (44.4111, -72.1428)
    >>> get_coordinates_by_zip(coordinates, "99999") is None
    True
    """
    return zip_coordinates.get(zip_code)


def get_market_coordinates(market, zip_coordinates):
    """
    Возвращает координаты рынка.
    Если координаты x/y отсутствуют, пытается получить их по ZIP-коду.

    Предусловия:
        market — словарь с данными рынка.
        zip_coordinates — словарь координат ZIP-кодов.

    Постусловия:
        Возвращает кортеж (широта, долгота) либо None.

    >>> market = {"x": "-72.14", "y": "44.41", "zip": "05828"}
    >>> get_market_coordinates(market, {})
    (44.41, -72.14)
    >>> market = {"x": "", "y": "", "zip": "05828"}
    >>> get_market_coordinates(market, {"05828": (44.41, -72.14)})
    (44.41, -72.14)
    """
    try:
        if market["x"] != "" and market["y"] != "":
            return float(market["y"]), float(market["x"])
    except (ValueError, TypeError):
        pass

    return get_coordinates_by_zip(zip_coordinates, market.get("zip", ""))


def search_by_distance(markets, zip_coordinates, zip_code, radius):
    """
    Ищет рынки в заданном радиусе.

    Предусловия:
        markets — список рынков.
        zip_coordinates — словарь координат ZIP-кодов.
        zip_code — строка.
        radius — неотрицательное число.

    Постусловия:
        Возвращает список кортежей (рынок, расстояние).
        Результат отсортирован по расстоянию.

    >>> markets = [
    ...     {"FMID": "1", "x": "-72.1428", "y": "44.4111", "zip": "05828"}
    ... ]
    >>> coordinates = {"05828": (44.4111, -72.1428)}
    >>> len(search_by_distance(markets, coordinates, "05828", 0))
    1
    >>> search_by_distance(markets, coordinates, "99999", 30)
    []
    >>> search_by_distance(markets, coordinates, "05828", -1)
    []
    """
    if radius < 0:
        return []

    point = get_coordinates_by_zip(zip_coordinates, zip_code)

    if point is None:
        return []

    result = []

    for market in markets:
        market_point = get_market_coordinates(market, zip_coordinates)

        if market_point is None:
            continue

        distance = calculate_distance(point, market_point)

        if distance <= radius:
            result.append((market, distance))

    result.sort(key=lambda item: item[1])

    return result


def sort_markets(markets, field, reverse=False):
    """
    Сортирует список рынков по выбранному полю.

    Предусловия:
        markets — список рынков.
        field — имя существующего поля.
        reverse — направление сортировки.

    Постусловия:
        Возвращает новый отсортированный список.
        Исходный список не изменяется.

    >>> markets = [
    ...     {"city": "Boston"},
    ...     {"city": "Albany"}
    ... ]
    >>> [market["city"] for market in sort_markets(markets, "city")]
    ['Albany', 'Boston']
    >>> [market["city"] for market in sort_markets(markets, "city", True)]
    ['Boston', 'Albany']
    """
    return sorted(
        markets,
        key=lambda market: market[field].lower(),
        reverse=reverse
    )


def sort_markets_by_rating(markets, reviews, reverse=False):
    """
    Сортирует рынки по среднему рейтингу.

    Предусловия:
        markets — список рынков.
        reviews — список отзывов.

    Постусловия:
        Возвращает новый список рынков,
        отсортированный по среднему рейтингу.

    >>> markets = [{"FMID": "1"}, {"FMID": "2"}]
    >>> reviews = [
    ...     {"FMID": "1", "Rating": "5"},
    ...     {"FMID": "2", "Rating": "3"}
    ... ]
    >>> [m["FMID"] for m in sort_markets_by_rating(markets, reviews)]
    ['2', '1']
    >>> [m["FMID"] for m in sort_markets_by_rating(markets, reviews, True)]
    ['1', '2']
    """
    return sorted(
        markets,
        key=lambda market: calculate_average_rating(reviews, market["FMID"]),
        reverse=reverse
    )


def calculate_distance(point1, point2):
    """
    Вычисляет расстояние между двумя точками в милях.

    Предусловия:
        point1 и point2 — кортежи (широта, долгота).

    Постусловия:
        Возвращает неотрицательное расстояние в милях.

    >>> round(calculate_distance((0, 0), (0, 0)), 2)
    0.0
    >>> round(calculate_distance((0, 0), (0, 1)), 2)
    69.1
    >>> round(calculate_distance((40, -70), (41, -71)), 2)
    86.81
    >>> calculate_distance((10, 10), (10, 10)) == 0
    True
    >>> calculate_distance((0, 0), (1, 1)) > 0
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


def show_market_details(market, reviews):
    """
    Выводит подробную информацию о выбранном рынке.

    Предусловия:
        market — словарь с данными рынка.
        reviews — список отзывов.

    Постусловия:
        Выводит подробную информацию о рынке,
        категории товаров и средний рейтинг.
    """
    print("\n=== Информация о рынке ===")
    print("Название:", market["MarketName"])
    print("Город:", market["city"])
    print("Штат:", market["State"])
    print("Адрес:", market["street"])
    print("Индекс:", market["zip"])
    print("Сайт:", market["Website"])

    print("\n=== Категории товаров ===")

    product_fields = [
        "Organic", "Bakedgoods", "Cheese", "Crafts", "Flowers", "Eggs",
        "Seafood", "Herbs", "Vegetables", "Honey", "Jams", "Maple",
        "Meat", "Nursery", "Nuts", "Plants", "Poultry", "Prepared",
        "Soap", "Trees", "Wine", "Coffee", "Beans", "Fruits", "Grains",
        "Juices", "Mushrooms", "PetFood", "Tofu", "WildHarvested"
    ]

    for field in product_fields:
        if field in market:
            value = market[field].strip()

            if value != "":
                print(field + ":", value)

    print("\n=== Оплата и программы ===")

    payment_fields = ["Credit", "WIC", "WICcash", "SFMNP", "SNAP"]

    for field in payment_fields:
        if field in market:
            value = market[field].strip()

            if value != "":
                print(field + ":", value)

    average_rating = calculate_average_rating(reviews, market["FMID"])
    market_reviews = get_market_reviews(reviews, market["FMID"])

    print("\n=== Рейтинг ===")

    if average_rating == 0:
        print("Средний рейтинг: нет оценок")
    else:
        print(f"Средний рейтинг: {average_rating:.1f} из 5")

    print("Количество отзывов:", len(market_reviews))


def load_reviews(filename):
    """
    Загружает отзывы из CSV-файла.

    Предусловия:
        filename — имя файла с отзывами.

    Постусловия:
        Возвращает список словарей.
        Если файл отсутствует, возвращает пустой список.
        Служебный BOM и старое поле ReviewID удаляются.
    """
    reviews = []

    try:
        with open(filename, encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                clean_row = {}

                for key, value in row.items():
                    if key is None:
                        continue

                    clean_key = key.lstrip("\ufeff")

                    if clean_key != "ReviewID":
                        clean_row[clean_key] = value

                reviews.append(clean_row)

    except FileNotFoundError:
        reviews = []

    return reviews


def add_review(reviews, market_id, name, text, rating):
    """
    Добавляет отзыв в список.

    Предусловия:
        reviews — список отзывов.
        market_id — FMID рынка.
        name — имя и фамилия пользователя.
        rating — число от 1 до 5.

    Постусловия:
        В конец списка добавляется новый отзыв.

    >>> reviews = []
    >>> add_review(reviews, "1", "Иван Иванов", "Хорошо", 5)
    >>> reviews[0]["Rating"]
    '5'
    >>> reviews[0]["FMID"]
    '1'
    """
    review = {
        "FMID": market_id,
        "Name": name,
        "Review": text,
        "Rating": str(rating)
    }
    reviews.append(review)


def save_reviews(filename, reviews):
    """
    Сохраняет отзывы в CSV-файл.

    Предусловия:
        reviews — список отзывов.

    Постусловия:
        Файл перезаписывается актуальным списком отзывов.
        Лишние служебные поля в словарях отзывов игнорируются.
    """
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        fields = ["FMID", "Name", "Review", "Rating"]
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            extrasaction="ignore"
        )
        writer.writeheader()

        for review in reviews:
            writer.writerow(review)


def get_market_reviews(reviews, market_id):
    """
    Получает отзывы выбранного рынка.

    Предусловия:
        reviews — список отзывов.
        market_id — FMID рынка.

    Постусловия:
        Возвращает новый список отзывов данного рынка.

    >>> reviews = [
    ...     {"FMID": "1", "Rating": "5"},
    ...     {"FMID": "2", "Rating": "4"},
    ...     {"FMID": "1", "Rating": "3"}
    ... ]
    >>> len(get_market_reviews(reviews, "1"))
    2
    >>> get_market_reviews(reviews, "999")
    []
    """
    result = []

    for review in reviews:
        if review["FMID"] == market_id:
            result.append(review)

    return result


def get_market_by_id(markets, fmid):
    """
    Возвращает рынок по его FMID.

    >>> markets = load_data("Export.csv")
    >>> get_market_by_id(markets, "1018261")["city"]
    'Danville'
    >>> get_market_by_id(markets, "1018261")["State"]
    'Vermont'
    >>> get_market_by_id(markets, "99999999") is None
    True
    >>> "FMID" in get_market_by_id(markets, "1018261")
    True
    >>> get_market_by_id(markets, "1018261")["FMID"]
    '1018261'
    """
    result = filter(lambda market: market["FMID"] == fmid, markets)
    markets_found = list(result)

    if len(markets_found) > 0:
        return markets_found[0]

    return None


def process_show(markets, reviews):
    """
    Показывает список фермерских рынков с разбивкой по страницам.
    """
    if len(markets) == 0:
        print("Нет рынков для отображения.")
        return

    page_size = 10
    total_pages = (len(markets) + page_size - 1) // page_size

    print("\n=== Просмотр фермерских рынков ===")
    print("Всего рынков:", len(markets))
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
        show_markets(markets, reviews, page, page_size)

        action = input(
            "\n[n] Следующая  [p] Предыдущая  "
            "[номер] Перейти на страницу  [q] Выход ==> "
        ).lower()

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


def process_search(markets, reviews):
    """
    Находит фермерский рынок по городу и штату.
    """
    city = input("Введите город: ").strip()
    state = input("Введите штат: ").strip()
    result = search_by_city_state(markets, city, state)

    if len(result) == 0:
        print("Рынки не найдены!")
    else:
        print("Найдено рынков:", len(result))

        for market in result:
            rating = calculate_average_rating(reviews, market["FMID"])
            rating_text = "нет оценок" if rating == 0 else f"{rating:.1f}/5"
            print(market["FMID"], "-", market["MarketName"], "-", rating_text)

        process_details(markets, reviews)


def process_zip(markets, reviews):
    """
    Находит фермерский рынок по индексу.
    """
    zip_code = input("Введите ZIP-код: ").strip()
    result = search_by_zip(markets, zip_code)

    if len(result) == 0:
        print("Рынки не найдены!")
    else:
        print("Найдено рынков:", len(result))

        for market in result:
            rating = calculate_average_rating(reviews, market["FMID"])
            rating_text = "нет оценок" if rating == 0 else f"{rating:.1f}/5"
            print(market["FMID"], "-", market["MarketName"], "-", rating_text)

        process_details(markets, reviews)


def process_details(markets, reviews):
    """
    Показывает подробную информацию о рынке по введенному FMID.
    """
    fmid = input(
        "\nВведите ID рынка для просмотра деталей "
        "(или Enter для выхода): "
    )

    if fmid == "":
        return

    market = get_market_by_id(markets, fmid)

    if market:
        show_market_details(market, reviews)
    else:
        print("Рынок с таким FMID не найден!")


def process_distance(markets, reviews, zip_coordinates):
    """
    Поиск рынков в заданном радиусе.
    """
    zip_code = input("Введите ZIP-код: ").strip()

    if get_coordinates_by_zip(zip_coordinates, zip_code) is None:
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

    result = search_by_distance(markets, zip_coordinates, zip_code, radius)

    if len(result) == 0:
        print("Рынки не найдены!")
    else:
        print("Найдено рынков:", len(result))

        for market, distance in result:
            rating = calculate_average_rating(reviews, market["FMID"])
            rating_text = "нет оценок" if rating == 0 else f"{rating:.1f}/5"

            print(
                market["FMID"], "-",
                market["MarketName"], "-",
                market["city"], "-",
                market["State"], "-",
                rating_text
            )
            print(f"Расстояние: {distance:.2f} миль.\n")

        process_details(markets, reviews)


def input_multiline_review():
    """
    Считывает многострочный текст отзыва.

    Предусловия:
        Пользователь вводит текст построчно.

    Постусловия:
        Возвращает строку с сохранением переносов строк.
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


def process_review(markets, reviews):
    """
    Добавляет отзыв о рынке.
    """
    market_id = input("Введите FMID рынка (или Enter для выхода): ")

    if market_id == "":
        return

    market = get_market_by_id(markets, market_id)

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

    text = input_multiline_review()
    add_review(reviews, market_id, name, text, rating)
    save_reviews("reviews.csv", reviews)

    print("Отзыв успешно сохранён!")


def process_reviews(markets, reviews):
    """
    Показывает отзывы о рынке.
    """
    market_id = input("Введите FMID рынка: ")
    market = get_market_by_id(markets, market_id)

    if market is None:
        print("Рынок не найден!")
        return

    market_reviews = get_market_reviews(reviews, market_id)

    if len(market_reviews) == 0:
        print("Для этого рынка пока нет отзывов :(")
    else:
        average_rating = calculate_average_rating(reviews, market_id)
        print(f"\nСредний рейтинг: {average_rating:.1f} из 5")
        print("Отзывы о рынке:")
        print("-" * 40)

        for review in market_reviews:
            print("Автор:", review["Name"])
            print("Оценка:", review["Rating"], "/ 5")

            if review["Review"] != "":
                print("Отзыв:")
                print(review["Review"])

            print("-" * 40)


def delete_review(reviews, market_id, review_number):
    """
    Удаляет отзыв выбранного рынка по его порядковому номеру.

    Предусловия:
        reviews — список отзывов.
        market_id — строка с FMID рынка.
        review_number — номер отзыва, начиная с 1.

    Постусловия:
        Если отзыв найден, он удаляется и возвращается True.
        Если отзыв не найден, возвращается False.

    >>> reviews = [
    ...     {"FMID": "1", "Name": "Иван", "Review": "Хорошо", "Rating": "5"},
    ...     {"FMID": "1", "Name": "Петр", "Review": "Нормально", "Rating": "4"},
    ...     {"FMID": "2", "Name": "Анна", "Review": "", "Rating": "3"}
    ... ]
    >>> delete_review(reviews, "1", 2)
    True
    >>> len(reviews)
    2
    >>> reviews[0]["Name"]
    'Иван'
    >>> delete_review(reviews, "1", 10)
    False
    """
    market_reviews = []

    for review in reviews:
        if review["FMID"] == market_id:
            market_reviews.append(review)

    if review_number < 1 or review_number > len(market_reviews):
        return False

    review_to_delete = market_reviews[review_number - 1]
    reviews.remove(review_to_delete)

    return True


def process_delete_review(markets, reviews):
    """
    Удаляет выбранный отзыв о рынке.
    """
    market_id = input("Введите FMID рынка (или Enter для выхода): ")

    if market_id == "":
        return

    market = get_market_by_id(markets, market_id)

    if market is None:
        print("Рынок не найден!")
        return

    market_reviews = get_market_reviews(reviews, market_id)

    if len(market_reviews) == 0:
        print("Для этого рынка нет отзывов!")
        return

    print("\nОтзывы о рынке:")
    print("-" * 40)

    for number, review in enumerate(market_reviews, start=1):
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

    deleted = delete_review(reviews, market_id, review_number)

    if deleted:
        save_reviews("reviews.csv", reviews)
        print("Отзыв удалён!")
    else:
        print("Отзыва с таким номером нет!")


def process_sort(markets, reviews, zip_coordinates):
    """
    Производит сортировку рынков по выбранному критерию.
    """
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
        sorted_markets = sort_markets(markets, "MarketName", reverse)
    elif choice == "2":
        sorted_markets = sort_markets(markets, "city", reverse)
    elif choice == "3":
        sorted_markets = sort_markets(markets, "State", reverse)
    elif choice == "4":
        sorted_markets = sort_markets_by_rating(markets, reviews, reverse)
    elif choice == "5":
        zip_code = input("Введите ZIP-код: ").strip()
        point = get_coordinates_by_zip(zip_coordinates, zip_code)

        if point is None:
            print("Такой ZIP-код отсутствует в справочнике!")
            return

        markets_with_distance = []

        for market in markets:
            market_point = get_market_coordinates(market, zip_coordinates)

            if market_point is None:
                continue

            distance = calculate_distance(point, market_point)
            markets_with_distance.append((market, distance))

        markets_with_distance.sort(
            key=lambda item: item[1],
            reverse=reverse)

        print("\nРынки, отсортированные по расстоянию:")

        for market, distance in markets_with_distance[:20]:
            print(
                market["FMID"], "-",
                market["MarketName"], "-",
                f"{distance:.2f} миль")

        print("Показаны первые 20 результатов.")
        return
    else:
        print("Неверный выбор!")
        return

    total_pages = (len(sorted_markets) + 9) // 10

    try:
        page = int(input(f"Введите номер страницы (1-{total_pages}): "))
    except ValueError:
        print("Введите номер страницы цифрами!")
        return

    if page < 1 or page > total_pages:
        print("Такой страницы нет!")
        return

    show_markets(sorted_markets, reviews, page)


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


def main_loop(markets, reviews, zip_coordinates):
    """
    Основной цикл работы программы.
    Обрабатывает команды, вводимые пользователем.
    """
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
            process_show(markets, reviews)
        elif cmd == "search":
            process_search(markets, reviews)
        elif cmd == "distance":
            process_distance(markets, reviews, zip_coordinates)
        elif cmd == "details":
            process_details(markets, reviews)
        elif cmd == "review":
            process_review(markets, reviews)
        elif cmd == "reviews":
            process_reviews(markets, reviews)
        elif cmd == "delete":
            process_delete(markets, reviews)
        elif cmd == "zip":
            process_zip(markets, reviews)
        elif cmd == "help":
            show_welcome()
        elif cmd == "sort":
            process_sort(markets, reviews, zip_coordinates)
        else:
            print(
                "Неизвестная команда. "
                "Введите help для отображения списка команд.")


def create_zip_coordinates(zip_codes):
    """
    Создает словарь координат ZIP-кодов.

    Предусловия:
        zip_codes — список записей, полученный из zip_util.read_zip_all().

    Постусловия:
        Возвращает словарь вида {ZIP: (широта, долгота)}.

    >>> data = [
    ...     ["05828", 44.4111, -72.1428, "Danville", "VT", "Caledonia"],
    ...     ["10001", 40.7506, -73.9972, "New York", "NY", "New York"]
    ... ]
    >>> result = create_zip_coordinates(data)
    >>> result["05828"]
    (44.4111, -72.1428)
    >>> result["10001"]
    (40.7506, -73.9972)
    """
    result = {}

    for zip_data in zip_codes:
        zip_code = zip_data[0]
        latitude = zip_data[1]
        longitude = zip_data[2]

        result[zip_code] = (latitude, longitude)

    return result


if __name__ == "__main__":

    if DEBUG:
        print(LINE)
        print("Running doctests...")
        print(LINE)

        failures, tests = doctest.testmod()

        print(f"Tests run: {tests}")
        print(f"Failures : {failures}")

    markets = load_data("Export.csv")
    reviews = load_reviews("reviews.csv")

    zip_codes = zip_util.read_zip_all()
    zip_coordinates = create_zip_coordinates(zip_codes)

    main_loop(markets, reviews, zip_coordinates)
