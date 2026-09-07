import json
import os
import random
import tkinter as tk
from tkinter import messagebox


CONFIG_FILE = "config.json"
SCORES_FILE = "scores.json"


DEFAULT_CONFIG = {
    "player_name": "Player",
    "board_size": 10,
    "cell_size": 32,
    "ship_count": 10,
    "difficulty": "easy",
    "water_color": "#bde0fe",
    "hit_color": "#e63946",
    "miss_color": "#eeeeee",
    "ship_color": "#457b9d",
    "font_size": 10
}


def load_config():
    """
    Загружает настройки из JSON.
    Если файла нет, возвращает настройки по умолчанию.
    """
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)

        result = DEFAULT_CONFIG.copy()

        for key in DEFAULT_CONFIG:
            if key in config:
                result[key] = config[key]

        return result

    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """
    Сохраняет настройки в JSON-файл.
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)


def load_scores():
    """
    Загружает таблицу результатов из JSON.
    """
    if not os.path.exists(SCORES_FILE):
        return []

    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_scores(scores):
    """
    Сохраняет таблицу результатов в JSON.
    """
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, ensure_ascii=False, indent=4)


def make_empty_board(size):
    """
    Создает пустое игровое поле.
    0 - вода
    1 - корабль
    2 - промах
    3 - попадание

    >>> make_empty_board(2)
    [[0, 0], [0, 0]]
    """
    board = []

    for row in range(size):
        line = []

        for col in range(size):
            line.append(0)

        board.append(line)

    return board


def count_ship_cells(board):
    """
    Считает количество оставшихся клеток кораблей.

    >>> board = [[0, 1, 1], [2, 3, 1]]
    >>> count_ship_cells(board)
    3
    """
    count = 0

    for row in board:
        for cell in row:
            if cell == 1:
                count += 1

    return count


def can_place_ship(board, row, col, length, horizontal):
    """
    Проверяет, можно ли поставить корабль.

    >>> board = make_empty_board(5)
    >>> can_place_ship(board, 0, 0, 3, True)
    True
    >>> place_ship(board, 0, 0, 3, True)
    >>> can_place_ship(board, 0, 0, 2, False)
    False
    """
    size = len(board)

    if horizontal:
        if col + length > size:
            return False
    else:
        if row + length > size:
            return False

    for i in range(length):
        if horizontal:
            r = row
            c = col + i
        else:
            r = row + i
            c = col

        if board[r][c] != 0:
            return False

    return True


def place_ship(board, row, col, length, horizontal):
    """
    Ставит корабль на поле.

    >>> board = make_empty_board(4)
    >>> place_ship(board, 1, 1, 2, True)
    >>> board[1]
    [0, 1, 1, 0]
    """
    for i in range(length):
        if horizontal:
            board[row][col + i] = 1
        else:
            board[row + i][col] = 1


def make_ship_lengths(ship_count):
    """
    Создает простой набор кораблей.
    Для учебной версии используются корабли длиной 1-4 клетки.

    >>> make_ship_lengths(5)
    [4, 3, 3, 2, 2]
    >>> make_ship_lengths(2)
    [4, 3]
    """
    pattern = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    result = []

    for i in range(ship_count):
        result.append(pattern[i % len(pattern)])

    return result


def place_ships_randomly(board, ship_count):
    """
    Расставляет корабли случайным образом.
    """
    lengths = make_ship_lengths(ship_count)

    for length in lengths:
        placed = False
        attempts = 0

        while not placed and attempts < 1000:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board) - 1)
            horizontal = random.choice([True, False])

            if can_place_ship(board, row, col, length, horizontal):
                place_ship(board, row, col, length, horizontal)
                placed = True

            attempts += 1


class SettingsWindow:
    """
    Окно настроек приложения.
    """

    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Настройки")
        self.window.geometry("360x430")
        self.window.resizable(False, False)

        self.name_entry = None
        self.size_entry = None
        self.cell_entry = None
        self.ship_entry = None
        self.difficulty_var = None
        self.font_entry = None

        self.create_widgets()

    def create_widgets(self):
        row = 0

        tk.Label(self.window, text="Имя игрока:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8
        )
        self.name_entry = tk.Entry(self.window)
        self.name_entry.insert(0, self.app.config["player_name"])
        self.name_entry.grid(row=row, column=1, padx=10, pady=8)

        row += 1
        tk.Label(self.window, text="Размер поля:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8
        )
        self.size_entry = tk.Entry(self.window)
        self.size_entry.insert(0, str(self.app.config["board_size"]))
        self.size_entry.grid(row=row, column=1, padx=10, pady=8)

        row += 1
        tk.Label(self.window, text="Размер клетки:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8
        )
        self.cell_entry = tk.Entry(self.window)
        self.cell_entry.insert(0, str(self.app.config["cell_size"]))
        self.cell_entry.grid(row=row, column=1, padx=10, pady=8)

        row += 1
        tk.Label(self.window, text="Количество кораблей:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8
        )
        self.ship_entry = tk.Entry(self.window)
        self.ship_entry.insert(0, str(self.app.config["ship_count"]))
        self.ship_entry.grid(row=row, column=1, padx=10, pady=8)

        row += 1
        tk.Label(self.window, text="Сложность:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8
        )
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set(self.app.config["difficulty"])

        difficulties = ["easy", "normal"]

        option = tk.OptionMenu(
            self.window,
            self.difficulty_var,
            *difficulties
        )
        option.grid(row=row, column=1, sticky="w", padx=10, pady=8)

        row += 1
        tk.Label(self.window, text="Размер шрифта:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8
        )
        self.font_entry = tk.Entry(self.window)
        self.font_entry.insert(0, str(self.app.config["font_size"]))
        self.font_entry.grid(row=row, column=1, padx=10, pady=8)

        row += 1
        text = (
            "Настройки сохраняются в config.json.\n"
            "После сохранения начинается новая игра."
        )
        tk.Label(
            self.window,
            text=text,
            justify="left",
            fg="gray"
        ).grid(row=row, column=0, columnspan=2, padx=10, pady=12)

        row += 1
        tk.Button(
            self.window,
            text="Сохранить",
            command=self.save
        ).grid(row=row, column=0, padx=10, pady=12)

        tk.Button(
            self.window,
            text="Отмена",
            command=self.window.destroy
        ).grid(row=row, column=1, padx=10, pady=12)

    def save(self):
        try:
            board_size = int(self.size_entry.get())
            cell_size = int(self.cell_entry.get())
            ship_count = int(self.ship_entry.get())
            font_size = int(self.font_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Размеры и количество кораблей должны быть числами."
            )
            return

        if board_size < 6 or board_size > 12:
            messagebox.showerror(
                "Ошибка",
                "Размер поля должен быть от 6 до 12."
            )
            return

        if cell_size < 24 or cell_size > 45:
            messagebox.showerror(
                "Ошибка",
                "Размер клетки должен быть от 24 до 45."
            )
            return

        if ship_count < 3 or ship_count > 12:
            messagebox.showerror(
                "Ошибка",
                "Количество кораблей должно быть от 3 до 12."
            )
            return

        if font_size < 8 or font_size > 20:
            messagebox.showerror(
                "Ошибка",
                "Размер шрифта должен быть от 8 до 20."
            )
            return

        self.app.config["player_name"] = self.name_entry.get().strip()

        if self.app.config["player_name"] == "":
            self.app.config["player_name"] = "Player"

        self.app.config["board_size"] = board_size
        self.app.config["cell_size"] = cell_size
        self.app.config["ship_count"] = ship_count
        self.app.config["difficulty"] = self.difficulty_var.get()
        self.app.config["font_size"] = font_size

        save_config(self.app.config)
        self.window.destroy()
        self.app.new_game()
        messagebox.showinfo(
            "Настройки",
            "Настройки сохранены и применены."
        )


class ScoresWindow:
    """
    Окно лучших результатов.
    """

    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Лучшие результаты")
        self.window.geometry("480x360")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self.window,
            text="Лучшие результаты",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        text = tk.Text(self.window, width=55, height=15)
        text.pack(padx=10, pady=8)

        scores = load_scores()

        win_scores = []

        for score in scores:
            if score.get("result") == "Победа":
                win_scores.append(score)

        win_scores.sort(key=lambda item: item.get("moves", 999999))

        if len(win_scores) == 0:
            text.insert("end", "Пока нет победных результатов.")
        else:
            number = 1

            for score in win_scores[:10]:
                line = (
                    str(number) + ". " +
                    score.get("name", "Player") +
                    " | ходов: " + str(score.get("moves", 0)) +
                    " | поле: " + str(score.get("board_size", "")) +
                    " | сложность: " + score.get("difficulty", "") +
                    "\n"
                )
                text.insert("end", line)
                number += 1

        text.config(state="disabled")

        tk.Button(
            self.window,
            text="Закрыть",
            command=self.window.destroy
        ).pack(pady=8)


class HelpWindow:
    """
    Окно с краткими правилами игры.
    """

    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Правила")
        self.window.geometry("520x420")

        self.create_widgets()

    def create_widgets(self):
        text = tk.Text(self.window, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)

        rules = (
            "Морской бой\n\n"
            "Слева находится поле игрока, справа поле компьютера.\n"
            "Корабли игрока показаны синим цветом.\n\n"
            "Чтобы сделать ход, нажмите на клетку поля компьютера.\n"
            "Красный цвет означает попадание.\n"
            "Серый цвет означает промах.\n\n"
            "После хода игрока компьютер делает ответный ход.\n"
            "Побеждает тот, кто первым уничтожит все корабли противника.\n\n"
            "Настройки игры сохраняются в файл config.json.\n"
            "Лучшие результаты сохраняются в файл scores.json."
        )

        text.insert("end", rules)
        text.config(state="disabled")

        tk.Button(
            self.window,
            text="Закрыть",
            command=self.window.destroy
        ).pack(pady=8)


class BattleshipGame:
    """
    Главное окно игры Морской бой.
    """

    def __init__(self, root):
        self.root = root
        self.config = load_config()

        self.player_board = []
        self.computer_board = []
        self.computer_shots = []
        self.moves = 0
        self.game_over = False

        self.root.title("Морской бой")
        self.root.geometry("1000x620")

        self.create_menu()
        self.create_interface()
        self.new_game()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Новая игра", command=self.new_game)
        game_menu.add_command(label="Настройки", command=self.open_settings)
        game_menu.add_command(label="Лучшие результаты", command=self.open_scores)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.destroy)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="Правила", command=self.open_help)

    def create_interface(self):
        self.title_label = tk.Label(
            self.root,
            text="Морской бой",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=8)

        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", self.config["font_size"])
        )
        self.info_label.pack(pady=4)

        boards_frame = tk.Frame(self.root)
        boards_frame.pack(pady=8)

        left_frame = tk.Frame(boards_frame)
        left_frame.grid(row=0, column=0, padx=20)

        right_frame = tk.Frame(boards_frame)
        right_frame.grid(row=0, column=1, padx=20)

        self.player_title_label = tk.Label(
            left_frame,
            text="Ваше поле",
            font=("Arial", 12, "bold")
        )
        self.player_title_label.pack()

        self.computer_title_label = tk.Label(
            right_frame,
            text="Поле компьютера",
            font=("Arial", 12, "bold")
        )
        self.computer_title_label.pack()

        self.player_canvas = tk.Canvas(
            left_frame,
            highlightthickness=0
        )
        self.player_canvas.pack()

        self.computer_canvas = tk.Canvas(
            right_frame,
            highlightthickness=0
        )
        self.computer_canvas.pack()

        self.computer_canvas.bind(
            "<Button-1>",
            self.computer_canvas_click
        )

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=8)

        self.new_game_button = tk.Button(
            button_frame,
            text="Новая игра",
            command=self.new_game
        )
        self.new_game_button.grid(row=0, column=0, padx=5)

        self.settings_button = tk.Button(
            button_frame,
            text="Настройки",
            command=self.open_settings
        )
        self.settings_button.grid(row=0, column=1, padx=5)

        self.scores_button = tk.Button(
            button_frame,
            text="Лучшие результаты",
            command=self.open_scores
        )
        self.scores_button.grid(row=0, column=2, padx=5)

        self.help_button = tk.Button(
            button_frame,
            text="Правила",
            command=self.open_help
        )
        self.help_button.grid(row=0, column=3, padx=5)

    def apply_font_settings(self):
        """
        Применяет размер шрифта к основным элементам окна.
        """
        font_size = self.config["font_size"]

        self.info_label.config(font=("Arial", font_size))
        self.player_title_label.config(font=("Arial", font_size + 2, "bold"))
        self.computer_title_label.config(font=("Arial", font_size + 2, "bold"))

        self.new_game_button.config(font=("Arial", font_size))
        self.settings_button.config(font=("Arial", font_size))
        self.scores_button.config(font=("Arial", font_size))
        self.help_button.config(font=("Arial", font_size))

    def new_game(self):
        """
        Начинает новую игру.
        """
        self.config = load_config()
        self.apply_font_settings()
        self.moves = 0
        self.game_over = False

        size = self.config["board_size"]
        ship_count = self.config["ship_count"]

        self.player_board = make_empty_board(size)
        self.computer_board = make_empty_board(size)

        place_ships_randomly(self.player_board, ship_count)
        place_ships_randomly(self.computer_board, ship_count)

        self.computer_shots = []

        for row in range(size):
            for col in range(size):
                self.computer_shots.append((row, col))

        random.shuffle(self.computer_shots)

        self.draw_boards()
        self.update_info("Игра началась. Сделайте ход по полю компьютера.")

    def draw_boards(self):
        """
        Создает игровые поля.
        """
        size = self.config["board_size"]
        cell_size = self.config["cell_size"]

        board_size = size * cell_size

        self.player_canvas.config(
            width=board_size,
            height=board_size
        )

        self.computer_canvas.config(
            width=board_size,
            height=board_size
        )

        self.update_boards()

    def computer_canvas_click(self, event):
        """
        Определяет клетку по месту клика мышью.
        """
        cell_size = self.config["cell_size"]

        col = event.x // cell_size
        row = event.y // cell_size

        size = self.config["board_size"]

        if row < size and col < size:
            self.player_shoot(row, col)

    def update_boards(self):
        """
        Перерисовывает игровые поля.
        """
        self.player_canvas.delete("all")
        self.computer_canvas.delete("all")

        size = self.config["board_size"]
        cell_size = self.config["cell_size"]
        font_size = self.config["font_size"]

        for row in range(size):
            for col in range(size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                player_cell = self.player_board[row][col]

                player_color = self.config["water_color"]
                player_text = ""

                if player_cell == 1:
                    player_color = self.config["ship_color"]

                if player_cell == 2:
                    player_color = self.config["miss_color"]
                    player_text = "•"

                if player_cell == 3:
                    player_color = self.config["hit_color"]
                    player_text = "X"

                self.player_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=player_color,
                    outline="black"
                )

                if player_text != "":
                    self.player_canvas.create_text(
                        x1 + cell_size / 2,
                        y1 + cell_size / 2,
                        text=player_text,
                        font=("Arial", font_size, "bold")
                    )

                computer_cell = self.computer_board[row][col]

                computer_color = self.config["water_color"]
                computer_text = ""

                if computer_cell == 2:
                    computer_color = self.config["miss_color"]
                    computer_text = "•"

                if computer_cell == 3:
                    computer_color = self.config["hit_color"]
                    computer_text = "X"

                self.computer_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=computer_color,
                    outline="black"
                )

                if computer_text != "":
                    self.computer_canvas.create_text(
                        x1 + cell_size / 2,
                        y1 + cell_size / 2,
                        text=computer_text,
                        font=("Arial", font_size, "bold")
                    )

    def player_shoot(self, row, col):
        """
        Выполняет ход игрока.
        """
        if self.game_over:
            return

        cell = self.computer_board[row][col]

        if cell == 2 or cell == 3:
            messagebox.showinfo("Ход", "В эту клетку уже стреляли.")
            return

        self.moves += 1

        if cell == 1:
            self.computer_board[row][col] = 3
            self.update_info("Попадание!")
        else:
            self.computer_board[row][col] = 2
            self.update_info("Промах.")

        self.update_boards()

        if count_ship_cells(self.computer_board) == 0:
            self.finish_game("Победа")
            return

        self.computer_move()

    def computer_move(self):
        """
        Выполняет ход компьютера.
        """
        if self.game_over:
            return

        if len(self.computer_shots) == 0:
            return

        if self.config["difficulty"] == "normal":
            shot = self.choose_normal_computer_shot()
        else:
            shot = self.computer_shots.pop()

        row = shot[0]
        col = shot[1]

        cell = self.player_board[row][col]

        if cell == 1:
            self.player_board[row][col] = 3
            self.update_info("Компьютер попал.")
        else:
            self.player_board[row][col] = 2
            self.update_info("Компьютер промахнулся.")

        self.update_boards()

        if count_ship_cells(self.player_board) == 0:
            self.finish_game("Поражение")

    def choose_normal_computer_shot(self):
        """
        Более внимательный ход компьютера.
        Если рядом с попаданием есть неизвестная клетка,
        компьютер старается стрелять туда.
        """
        size = self.config["board_size"]

        for row in range(size):
            for col in range(size):
                if self.player_board[row][col] == 3:
                    variants = [
                        (row - 1, col),
                        (row + 1, col),
                        (row, col - 1),
                        (row, col + 1)
                    ]

                    for shot in variants:
                        if shot in self.computer_shots:
                            self.computer_shots.remove(shot)
                            return shot

        return self.computer_shots.pop()

    def finish_game(self, result):
        """
        Завершает игру и сохраняет результат.
        """
        self.game_over = True
        self.update_boards()

        scores = load_scores()

        score = {
            "name": self.config["player_name"],
            "result": result,
            "moves": self.moves,
            "board_size": self.config["board_size"],
            "difficulty": self.config["difficulty"]
        }

        scores.append(score)
        save_scores(scores)

        if result == "Победа":
            messagebox.showinfo(
                "Игра окончена",
                "Вы победили! Ходов: " + str(self.moves)
            )
        else:
            messagebox.showinfo(
                "Игра окончена",
                "Вы проиграли. Ходов: " + str(self.moves)
            )

    def update_info(self, text):
        """
        Обновляет информационную строку.
        """
        player_left = count_ship_cells(self.player_board)
        computer_left = count_ship_cells(self.computer_board)

        info = (
            text +
            "   Ходов: " + str(self.moves) +
            "   Ваши клетки кораблей: " + str(player_left) +
            "   Клетки компьютера: " + str(computer_left)
        )

        self.info_label["text"] = info

    def open_settings(self):
        """
        Открывает окно настроек.
        """
        SettingsWindow(self)

    def open_scores(self):
        """
        Открывает окно лучших результатов.
        """
        ScoresWindow(self)

    def open_help(self):
        """
        Открывает окно правил.
        """
        HelpWindow(self)


def main():
    config = load_config()
    save_config(config)

    if not os.path.exists(SCORES_FILE):
        save_scores([])

    root = tk.Tk()
    BattleshipGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
