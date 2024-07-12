import sqlite3


def get_db(name: str = "main.db"):
    """
    Establishes a connection to the SQLite database and creates necessary tables.

    This function connects to the specified SQLite database file. If the file does not
    exist, it will be created. It also ensures that the required tables are present by
    calling the `create_table` function.

    :param name: The name of the database file. Defaults to "main.db".
    :return: A connection object to the SQLite database.
    """
    db = sqlite3.connect(name)
    create_table(db)
    return db


def create_table(db):
    """
    Creates the required tables in the SQLite database if they do not already exist.

    This function creates two tables: `habits` and `tracker`. The `habits` table stores
    the habit details, while the `tracker` table stores the check-in dates for each habit.

    :param db: The SQLite database connection object.
    :return: None
    """
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
