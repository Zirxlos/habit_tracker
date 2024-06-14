import sqlite3
from datetime import datetime
from habit import Habit

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

def get_habit_data(db, habit):
    """
    function to return all the checked in dates of one specific habit.
    :param db: database to search
    :param habit: habit to get the dates
    :return: a list of all the checked in dates of one habit
    """
    cur = db.cursor()
    cur.execute("SELECT date FROM tracker WHERE habit_name=?", (habit.name,))
    ## transforming the result into a list of dates instead of a list of tuples with strings
    habit.check_dates = list(map(lambda x: datetime.fromisoformat(x[0]).date(), cur.fetchall()))
    return habit

def get_habits(db):
    """
    Function to obtain a list of Habit objects which is stored in the DB
    :param db: database to search
    :return: a list of Habit objects
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity FROM habits")
    habits = [Habit(*item) for item in list(map(lambda x: x, cur.fetchall()))]
    return habits