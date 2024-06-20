import sqlite3
import habit as h


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


def get_habits(db, periodicity=None):
    """
    Function to obtain a list of Habit objects which is stored in the DB
    :param periodicity: "daily" or "weekly"
    :param db: database to search
    :return: a list of Habit objects
    """
    cur = db.cursor()
    if periodicity == "daily":
        cur.execute("SELECT name, description, periodicity FROM habits WHERE periodicity = 1")
    elif periodicity == "weekly":
        cur.execute("SELECT name, description, periodicity FROM habits WHERE periodicity = 7")
    else:
        cur.execute("SELECT name, description, periodicity FROM habits")
    return [h.Habit(*item) for item in [row for row in cur.fetchall()]]
