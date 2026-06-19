from PIL import Image
import doctest

INPUT_FILE = "input.csv"
OUTPUT_FILE = "output.csv"
NUM_OF_GENERATIONS = 50
COLOR = (0, 255, 0)

def load_grid(filename):        # Загрузка начальных данных из input.csv
    with open(filename) as file:
        file.readline() # Пропускаем размер поля
        return [
            list(map(int, line.split(",")))
            for line in file
]
def count_neighbors(grid, x, y): # Подсчет соседей
    """
        Подсчёт живых соседей:
        >>> grid = [[1,1,0],[0,1,0],[0,0,0]]
        >>> count_neighbors(grid,1,1)
        2
        >>> count_neighbors(grid,0,0)
        2

        Проверка пустого поля:
        >>> grid = [[0,0,0],[0,0,0],[0,0,0]]
        >>> count_neighbors(grid,1,1)
        0

        Проверка клетки с 8 соседями:
        >>> grid = [[1,1,1],[1,0,1],[1,1,1]]
        >>> count_neighbors(grid,1,1)
        8
        """
    count = 0
    height = len(grid)
    width = len(grid[0])
    for dy in (-1, 0, 1):               # Движение по вертикали
        for dx in (-1, 0, 1):           # Движение по горизонтали
            if dx == 0 and dy == 0:
                continue                # Пропуск самой клетки
            nx = x + dx                 # Координаты соседа
            ny = y + dy
            if (0 <= nx < width
                and 0 <= ny < height): # Проверка, что сосед внутри поля
                count += grid[ny][nx]
    return count                        # Возвращаем количество соседей

def next_generation(grid, age_grid):    # Создание нового поколения
    """
      Создание следующего поколения.
      >>> grid = [[0,1,0],[1,1,1],[0,0,0]]
      >>> age_grid = [[0,1,0],[1,1,1],[0,0,0]]
      >>> next_generation(grid, age_grid)[0]
      [[1, 1, 1], [1, 1, 1], [0, 1, 0]]

      Проверка пустого поля:
      >>> grid = [[0,0],[0,0]]
      >>> age_grid = [[0,0],[0,0]]
      >>> next_generation(grid, age_grid)[0]
      [[0, 0], [0, 0]]

      Проверка одиночной клетки:
      >>> grid = [[0,0,0],[0,1,0],[0,0,0]]
      >>> age_grid = [[0,0,0],[0,1,0],[0,0,0]]
      >>> next_generation(grid, age_grid)[0]
      [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

      Проверка стабильного блока:
      >>> grid = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
      >>> age_grid = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
      >>> next_generation(grid, age_grid)[0]
      [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]

      Проверка увеличения возраста:
      >>> grid = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
      >>> age_grid = [[0,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,0]]
      >>> next_generation(grid, age_grid)[1]
      [[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0], [0, 0, 0, 0]]
      """
    height = len(grid)
    width = len(grid[0])
    new_grid = [                # Создаем новое поле для след.поколения
        [0] * width
        for _ in range(height)
    ]
    new_age_grid = [            # Создаем таблицу возраста для след.поколения
        [0] * width
        for _ in range(height)
    ]
    for y in range(height):     # Перебираем строки поля
        for x in range(width):  # Перебираем клетки в строке
            neighbors = count_neighbors(grid,x,y)
            if (                                        # Проверяем главное условие игры
                grid[y][x] and neighbors in (2, 3)      # Если клетка живая
            ) or (
                not grid[y][x] and neighbors == 3       # Если клетка мертвая
            ):
                new_grid[y][x] = 1                      # Делаем клетку живой
                new_age_grid[y][x] = age_grid[y][x] + 1 # Увеличиваем возраст
    return new_grid, new_age_grid

def save_output_png(grid, age_grid, filename): # Сохранение изображений в PNG
    height = len(grid)
    width = len(grid[0])
    image = Image.new( # Показалось удобнее ImageDraw. Но, это субъективное мнение.
        "RGB",
        (width, height),
        "black")
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            if grid[y][x]: # Если клетка живая
                brightness = min(
                    age_grid[y][x] / 10,1)
                pixels[x, y] = (
                    int(COLOR[0] * brightness),
                    int(COLOR[1] * brightness),
                    int(COLOR[2] * brightness))
    image.resize(
        (width * 50, height * 50),
        Image.Resampling.NEAREST).save(filename)

def write_output_csv(file, grid, generation): # Запись поколения в CSV
    file.write(
        "Generation "                         # Записываем номер поколения
        + str(generation)
        + "\n")
    for row in grid:
        file.write(
            ",".join(map(str, row))
            + "\n")
    file.write("\n")

def simulate():                     # Запуск игры Жизнь
    grid = load_grid(INPUT_FILE)
    age_grid = [                    # Создание возраста
        [
            1 if cell else 0        # Живая клетка получает возраст 1
            for cell in row
        ]
        for row in grid
    ]
    with open(
        OUTPUT_FILE,
        "w"                         # Запись файла
    ) as file:
        for generation in range(NUM_OF_GENERATIONS + 1): # Цикл поколений до 50
            write_output_csv(
                file,
                grid,
                generation)
            save_output_png(
                grid,
                age_grid,
                "generation_"
                + str(generation)
                + ".png")
            grid, age_grid = next_generation(grid,age_grid)

if __name__ == "__main__":
    doctest.testmod()
    simulate()