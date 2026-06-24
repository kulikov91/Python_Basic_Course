import zip_util
import math
import doctest

zip_codes = zip_util.read_zip_all()

def calculate_distance(location1, location2): # Вычисляем расстояние между двумя точками в милях
    """
    >>> round(calculate_distance((0, 0), (0, 0)), 2)
    0.0

    >>> round(calculate_distance((0, 0), (0, 1)), 2)
    69.1

    >>> round(calculate_distance((40, -70), (41, -71)), 2)
    86.81
    """

    lat1 = math.radians(location1[0])
    lon1 = math.radians(location1[1])

    lat2 = math.radians(location2[0])
    lon2 = math.radians(location2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Формула Хаверсина
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * \
        math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )
    earth_radius = 3959.3
    return earth_radius * c

def location_by_zip(zip_codes, zip_code): #  Поиск информации по почтовому индексу
    """
    >>> location_by_zip(zip_codes, "12180")
    (42.673701, -73.608792, 'Troy', 'NY', 'Rensselaer')

    >>> print(location_by_zip(zip_codes, "99999"))
    None
    """

    for item in zip_codes:
        if item[0] == zip_code:
            return (
                item[1], #lat
                item[2], #lon
                item[3], #city
                item[4], #state
                item[5]  #county
            )
    return None

def zip_by_location(zip_codes, city, state): # Поиск индекса по городу и штату
    """
    >>> zip_by_location(zip_codes, "Troy", "NY")
    ['12179', '12180', '12181', '12182', '12183']

    >>> zip_by_location(zip_codes, "Aguada", "PR")
    ['00602']

    >>> zip_by_location(zip_codes, "Holtsville", "NY")
    ['00501', '00544', '11742']

    >>> zip_by_location(zip_codes, "AAAA", "NY")
    []
    """

    result = []

    for item in zip_codes:
        if item[3].lower() == city.lower() and \
           item[4].lower() == state.lower():
            result.append(item[0])
    return result

def convert_coordinate(value, is_latitude): # Перевод координат в формат вывода
    if is_latitude:
        if value >= 0:
            direction = "N"
        else:
            direction = "S"

    else:
        if value >= 0:
            direction = "E"
        else:
            direction = "W"

    value = abs(value)
    degrees = int(value)
    minutes_full = (value - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return (
        f"{degrees:03d}∘"
        f"{minutes:02d}'"
        f"{seconds:05.2f}\""
        f"{direction}"
    )

def process_loc(zip_codes):
    zip_code = input("Enter a ZIP Code to lookup => ")
    print(zip_code)
    result = location_by_zip(zip_codes, zip_code)

    if result is None:
        print("ZIP Code not found")

    else:
        latitude = result[0]
        longitude = result[1]
        city = result[2]
        state = result[3]
        county = result[4]

        lat = convert_coordinate(latitude, True)

        lon = convert_coordinate(longitude, False)

        print(
            "ZIP Code",
            zip_code,
            "is in",
            city + ",",
            state + ",",
            county,
            "county,"
        )

        print(
            "coordinates:",
            "(" + lat + "," + lon + ")"
        )

def process_zip(zip_codes):
    city = input("Enter a city name to lookup => ")
    print(city)

    state = input("Enter the state name to lookup => ")
    print(state)
    result = zip_by_location(zip_codes, city, state)

    if len(result) == 0:
        print("City or state not found")

    else:
        print(
            "The following ZIP Code(s) found for",
            city.title() + ",",
            state.upper() + ":",
            ", ".join(result)
        )

def process_dist(zip_codes):
    first_zip = input("Enter the first ZIP Code => ")
    print(first_zip)

    second_zip = input("Enter the second ZIP Code => ")
    print(second_zip)

    first_location = location_by_zip(
        zip_codes,
        first_zip
    )

    second_location = location_by_zip(
        zip_codes,
        second_zip
    )

    if first_location is None or second_location is None:
        print("ZIP Code not found")

    else:
        point1 = (
            first_location[0],
            first_location[1]
        )

        point2 = (
            second_location[0],
            second_location[1]
        )

        distance = calculate_distance(
            point1,
            point2
        )

        print(
            "The distance between",
            first_zip,
            "and",
            second_zip,
            "is",
            round(distance, 2),
            "miles"
        )

def main_loop():
    while True:
        cmd = input(
            "Command ('loc', 'zip', 'dist', 'end') => "
        )

        cmd = cmd.lower()

        if cmd == "end":
            print("Done")
            break

        elif cmd == "loc":
            print("loc")
            process_loc(zip_codes)

        elif cmd == "zip":
            print("zip")
            process_zip(zip_codes)

        elif cmd == "dist":
            print("dist")
            process_dist(zip_codes)

        else:
            print(
                "Invalid command, ignoring"
            )

if __name__ == "__main__":
    doctest.testmod()
    main_loop()