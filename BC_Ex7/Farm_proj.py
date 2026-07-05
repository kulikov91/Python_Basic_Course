import csv
import math
import doctest

def load_data(filename):
    """
    Загружает данные о фермерских рынках из CSV-файла.
    Возвращает список словарей, где каждый словарь
    соответствует одной записи.
    """

    markets = []
    with open(filename, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            markets.append(row)
    return markets

def show_markets(markets, page=1, size=10):
    """
    Выводит список рынков постранично.
    markets - список рынков.
    page - номер страницы.
    size - количество записей на странице.
    """

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
        print(f"{m['FMID']:<10} {m['MarketName'][:33]:<35} {m['city']:<15} {m['State']:<5}")

    print("-" * 70)
    print(f"Страница {page}/{total_pages} | Всего рынков: {total}")
    print("=" * 70)

def search_by_city_state(markets, city, state):
    """
    Поиск рынков по городу и штату.

    >>> markets = load_data("Export.csv")

    >>> len(search_by_city_state(markets, "Danville", "Vermont")) > 0
    True

    >>> isinstance(search_by_city_state(markets, "Danville", "Vermont"), list)
    True

    >>> search_by_city_state(markets, "danville", "vermont")[0]["city"]
    'Danville'

    >>> search_by_city_state(markets, "danville", "vermont")[0]["State"]
    'Vermont'
    """

    result = filter(
        lambda market:
        market['city'].lower() == city.lower()
        and
        market['State'].lower() == state.lower(),markets)
    return list(result)

def search_by_zip(markets, zip_code):
    """
    Ищет рынки по почтовому индексу.

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

def get_coordinates_by_zip(markets, zip_code):
    """
    Возвращает координаты первого рынка с указанным ZIP-кодом.

    >>> markets = load_data("Export.csv")

    >>> isinstance(get_coordinates_by_zip(markets, "05828"), tuple)
    True

    >>> get_coordinates_by_zip(markets, "99999") is None
    True
    """
    for market in markets:

        if market["zip"] == zip_code:
            return (
                float(market["y"]),
                float(market["x"]))
    return None

def search_by_distance(markets, zip_code, radius):
    """
    Ищет рынки в заданном радиусе.

    >>> markets = load_data("Export.csv")

    >>> len(search_by_distance(markets, "05828", 0)) >= 1
    True

    >>> search_by_distance(markets, "99999", 30)
    []

    >>> len(search_by_distance(markets, "05828", 30)) > 0
    True

    >>> search_by_distance(markets, "05828", 30)[0][1] >= 0
    True
    """

    point = get_coordinates_by_zip(markets,zip_code)

    if point is None:
        return []
    result = []

    for market in markets:
        if market["x"] == "" or market["y"] == "":
            continue

        market_point = (
            float(market["y"]),
            float(market["x"]))
        distance = calculate_distance(point,market_point)

        if distance <= radius:
            result.append((market, distance))
    result.sort(key=lambda item: item[1])
    return result

def sort_markets(markets, field, reverse=False):
    """
    Сортирует список рынков.
    """
    return sorted(markets,
        key=lambda market: market[field],
        reverse=reverse)

def calculate_distance(point1, point2):
    """
    Вычисляет расстояние между двумя точками в милях.

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
        * math.sin(dlon / 2) ** 2)

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a))

    earth_radius = 3959.3
    return earth_radius * c

def show_market_details(market):
    """
    Выводит подробную информацию о выбранном рынке.
    """
    print("\n=== Информация о рынке ===")
    print("Название:",market["MarketName"])
    print("Город:",market["city"])
    print("Штат:",market["State"])
    print("Адрес:",market["street"])
    print("Индекс:",market["zip"])
    print("Сайт:",market["Website"])
    print("Органический:",market["Organic"])

def load_reviews(filename):
    """
    Загрузка отзывов
    """
    pass

def add_review(reviews, market_id, name, text, rating):
    """
    Добавление отзыва
    """
    pass

def save_reviews(filename, reviews):
    """
    Сохранение отзывов
    """
    pass

def get_market_reviews(reviews, market_id):
    """
    Получение отзывов рынка
    """
    pass

def delete_market(markets, market_id):
    """
    Удаление рынка
    """
    pass

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

    result = filter(lambda market: market["FMID"] == fmid,markets)
    markets_found = list(result)

    if len(markets_found) > 0:
        return markets_found[0]
    return None

def show_welcome():
    """
    Выводит приветственное сообщение и список доступных команд.
    """
    print("""
=========================================
   Добро пожаловать в программу поиска
         фермерских рынков США
=========================================

        === Доступные команды ===

                = SHOW =
    Показывает список фермерских рынков
        с разбивкой по страницам

               = SEARCH =
        Находит фермерский рынок
           по городу и штату
           
                = ZIP =
        Находит фермерский рынок
              по индексу
              
              = DISTANCE =
        Находит фермерский рынок
          в указанном радиусе
         от заданного ZIP-кода

              = DETAILS =
    Показывает подробную информацию
           о выбранном рынке
           
               = SORT =
      Отсортировать список рынков
      по названию, городу или штату

               = END =
      Завершает работу программы
=========================================
""")

def main_loop(markets):
    """
    Основной цикл работы программы.
    Обрабатывает команды, вводимые пользователем.
    """
    show_welcome()

    while True:
        cmd = input(
            "\n\tВведите команду без кавычек:\n"
            "('show', 'search', 'zip', 'distance', 'sort', 'end', 'help') ==> ")

        cmd = cmd.lower()

        if cmd == "end":
            print("Программа завершена!")
            break

        elif cmd == "show":
            try:
                page = int(input("Введите номер страницы: "))

            except ValueError:
                print("Введите номер страницы цифрами!")
                continue

            while True:
                show_markets(markets, page)
                action = input(
                    "\n[n] Следующая  [p] Предыдущая  [номер] Перейти на страницу  [q] Выход ==> "
                ).lower()

                total_pages = (len(markets) + 9) // 10

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

        elif cmd == "search":
            city = input("Введите город: ")
            state = input("Введите штат: ")
            result = search_by_city_state(markets,city,state)

            if len(result) == 0:
                print("Рынки не найдены!")

            else:
                print("Найдено рынков:", len(result))

                for market in result:
                    print(market["FMID"],"-",market["MarketName"])

                fmid = input( "\nВведите ID рынка для просмотра деталей "
                    "(или Enter для выхода): ")

                if fmid != "":
                    market = get_market_by_id(markets, fmid)

                    if market:
                        show_market_details(market)
                    else:
                        print("Рынок с таким FMID не найден!")

        elif cmd == "distance":
            zip_code = input("Введите ZIP-код: ")

            try:
                radius = float(input("Введите радиус (в милях): "))

            except ValueError:
                print("Введите радиус числом!")
                continue

            result = search_by_distance(markets,zip_code,radius)

            if len(result) == 0:
                print("Рынки не найдены!")

            else:
                print("Найдено рынков:",len(result))

                for market, distance in result:
                    print(
                        market["FMID"],
                        "-",
                        market["MarketName"],
                        "-",
                        market["city"],
                        "-",
                        market["State"])

                    print("Расстояние:", round(distance, 2),"миль.")
                    print()

                fmid = input("\nВведите ID рынка для просмотра деталей "
                    "(или Enter для выхода): ")

                if fmid != "":
                    market = get_market_by_id(markets, fmid)

                    if market:
                        show_market_details(market)
                    else:
                        print("Рынок с таким FMID не найден!")

        elif cmd == "zip":
            zip_code = input("Введите ZIP-код: ")
            result = search_by_zip(markets,zip_code)

            if len(result) == 0:
                print("Рынки не найдены!")

            else:
                print("Найдено рынков:",len(result))

                for market in result:
                    print(market["FMID"],
                        "-",
                        market["MarketName"])

                fmid = input(
                    "\nВведите ID рынка для просмотра деталей "
                    "(или Enter для выхода): ")

                if fmid != "":
                    market = get_market_by_id(
                        markets,
                        fmid)

                    if market:
                        show_market_details(market)
                    else:
                        print("Рынок с таким FMID не найден!")

        elif cmd == "help":
            show_welcome()

        elif cmd == "sort":
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
                sorted_markets = sort_markets(markets,"MarketName",reverse)

            elif choice == "2":
                sorted_markets = sort_markets(markets,"city",reverse)

            elif choice == "3":
                sorted_markets = sort_markets(markets,"State",reverse)

            else:
                print("Неверный выбор!")
                continue
            page = int(input("Введите номер страницы: "))
            show_markets(sorted_markets, page)

        else:
            print(
                "Неизвестная команда. "
                "Введите help для отображения списка команд.")

if __name__ == "__main__":
    doctest.testmod()
    markets = load_data("Export.csv")
    main_loop(markets)
