import sqlite3
from datetime import date

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
            FOREIGN KEY (habit_name) REFERENCES habits(name)
        )""")

    db.commit()

def add_habit(db, name, description, periodicity):
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (name, description, periodicity))
    db.commit()

def increment_tracker(db, name, event_date=None):
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()

def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT date FROM tracker WHERE habit_name=?", (name,))
    return cur.fetchall()

def get_habit(db, name):
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity FROM habits WHERE name=?", (name,))
    return cur.fetchall()