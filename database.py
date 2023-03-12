import sqlite3 as sq
from scheduled import parse_scheduled


def create_matches_table(table_name="matches"):
    with sq.connect("database.db") as con:
        cur = con.cursor()  # Cursor
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                   match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   score TEXT NOT NULL,
                   time TEXT NOT NULL,
                   category TEXT NOT NULL
                )""")
        con.commit()
        print("Database is created")


def delete_table(table_name):
    with sq.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS '{table_name}'")  # DELETE table


def add_results_to_matches_table():
    with sq.connect("database.db") as con:
        cur = con.cursor()
        for match in parse_results():
            cur.execute("SELECT 1 FROM matches WHERE title = ? AND category = ?", (match[0], match[3]))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO matches (title, score, time, category) VALUES (?, ?, ?, ?)", match)
                print("Матч добавлен.")
            else:
                print("Такой матч уже есть в базе данных.")
    con.commit()


def create_player_table(nickname):
    with sq.connect("database.db") as con:
        cur = con.cursor()  # Cursor
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {nickname} (
                   match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   score TEXT NOT NULL,
                   forecast TEXT,
                   time TEXT NOT NULL,
                   category TEXT NOT NULL
                )""")
        con.commit()


def insert_player_table(table_name):
    with sq.connect("database.db") as con:
        cur = con.cursor()
        for match in parse_scheduled():
            cur.execute(f"SELECT 1 FROM {table_name} WHERE title = ? AND category = ?", (match[0], match[3]))
            if cur.fetchone() is None:
                cur.execute(
                    f"""INSERT INTO {table_name} (title, score, time, category) VALUES ('{match[0]}', '{match[1]}',
                    '{match[2]}', '{match[3]}')
                    """)
                print("Матч добавлен.")
            else:
                continue
    con.commit()


def update_player_table(table_name):
    with sq.connect("database.db") as con:
        cur = con.cursor()
        for match in parse_scheduled():
            cur.execute(f"UPDATE {table_name} SET score = ? WHERE title = ? AND category = ?",
                        (match[1], match[0], match[3]))
        print(
            f"Счёт матча обновлён.")  # Обновляет только 1 матч, а надо, чтобы сразу все или только те где появился счет


# def last_tour_matches(table_name, category):
#     with sq.connect("database.db") as con:
#         cur = con.cursor()
#         cur.execute(f"SELECT * FROM '{table_name}' WHERE category = '{category}'")
#         result = [title[2] for title in cur.fetchall()]
#     return result


def all_players_tables():
    with sq.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND sql LIKE '%forecast%'")
        tables = cur.fetchall()
    return tables


def last_tour_buttons(player_table):
    with sq.connect("database.db") as con:
        cur = con.cursor()
        last_tour = f"SELECT * FROM {player_table} WHERE forecast is NULL ORDER BY match_id LIMIT 8"
        cur.execute(last_tour)
        result = cur.fetchall()
        # добавить, чтоб выдавал список не только где пустое поле forecast, но и где в поле score = '—'

        return result
