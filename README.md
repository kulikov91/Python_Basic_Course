Farm Market — (GUI + OOP + PostgreSQL)

1. Установить PostgreSQL.
2. Создать базу данных:
   CREATE DATABASE farm_market;
3. Установить:
   pip install -r requirements.txt
4. По умолчанию программа использует:
   host=localhost
   port=5432
   dbname=farm_market
   user=postgres
   password=postgres

5. При первом запуске таблицы создаются автоматически.
   Если они пусты, данные один раз импортируются из:
   Export.csv
   reviews.csv
   zip_codes_states.csv

6. После импорта рабочим хранилищем является PostgreSQL.
   Добавление и удаление отзывов и рынков сохраняется в базе данных.

Запуск:
python Farm_proj_POSTGRESQL.py
