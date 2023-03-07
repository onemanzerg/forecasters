import sqlite3 as sq
from serie_a_results import parse_results


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
                   forecast TEXT NOT NULL,
                   time TEXT NOT NULL,
                   category TEXT NOT NULL
                )""")
        con.commit()
