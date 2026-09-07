Задание 10. Морской бой

Состав проекта:
    battleship.py        - основная программа
    config.json          - настройки приложения
    scores.json          - лучшие результаты
    run_linux.sh         - запуск в Linux
    run_windows.bat      - запуск в Windows
    docs/                - документация

Запуск в Windows:
    run_windows.bat

Запуск в Linux:
    chmod +x run_linux.sh
    ./run_linux.sh

Также можно запустить напрямую:
    python battleship.py

Проверка doctest:
    python -m doctest -v battleship.py

В doctest проверяется основная логика:
    - создание игрового поля;
    - подсчет клеток кораблей;
    - проверка размещения корабля;
    - размещение корабля;
    - формирование списка кораблей.
