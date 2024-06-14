import sqlite3


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_table(db)
    return db


def create_table(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY,
        description TEXT,
        periodicity INT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
            date TEXT,
            habit_name TEXT,
            PRIMARY KEY (date, habit_name),
            FOREIGN KEY (habit_name) REFERENCES habits(name)
        )""")

    db.commit()

