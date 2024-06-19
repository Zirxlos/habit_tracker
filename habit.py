from datetime import date, datetime
from analyse import calculate_streak_daily, calculate_streak_weekly


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name.lower()
        self.description = description.lower()
        self.periodicity = periodicity
        self.longest_streak = 0
        self.current_streak = 0
        self.check_dates = []

    def store(self, db):
        cur = db.cursor()
        cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (self.name, self.description, self.periodicity))
        db.commit()

    def add_event(self, db, event_date: str = None):
        if not event_date:
            event_date = str(date.today())
        cur = db.cursor()
        cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, self.name))
        db.commit()

    def delete_habit(self, db):
        cur = db.cursor()
        cur.execute("DELETE FROM tracker WHERE habit_name=?", (self.name,))
        cur.execute("DELETE FROM habits WHERE name=?", (self.name,))
        db.commit()

    def get_habit_data(self, db):
        """
        function to return all the checked in dates of one specific habit.
        :param db: database to search
        :return: a list of all the checked in dates of one habit
        """
        cur = db.cursor()
        cur.execute("SELECT date FROM tracker WHERE habit_name=?", (self.name,))
        # transforming the result into a list of dates instead of a list of tuples with strings
        self.check_dates = list(map(lambda x: datetime.fromisoformat(x[0]).date(), cur.fetchall()))

    def calculate_streak(self, db):
        """
        function which computes streak of a Habit. A daily Habit must be made once per day and a weekly Habit must be
        done once per week between Monday and Friday.
        :param db: database to search
        :return: void, the Habit is returned by the called functions and updates the Habit instance
        """
        self.get_habit_data(db)
        if not self.check_dates:
            self.longest_streak = 0
            self.current_streak = 0
        elif self.periodicity == 1:
            calculate_streak_daily(self)
        else:
            calculate_streak_weekly(self)


def get_habits(db):
    """
    Function to obtain a list of Habit objects which is stored in the DB
    :param db: database to search
    :return: a list of Habit objects
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity FROM habits")
    # habits = [Habit(*item) for item in list(map(lambda x: x, cur.fetchall()))]
    # return habits
    return [Habit(*item) for item in list(map(lambda x: x, cur.fetchall()))]


def get_daily_habits(db):
    """
    Function to obtain a list of daily Habit objects which is stored in the DB
    :param db: database to search
    :return: a list of Habit objects with a periodicity of 1
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity FROM habits WHERE periodicity = 1")
    return [Habit(*item) for item in list(map(lambda x: x, cur.fetchall()))]


def get_weekly_habits(db):
    """
    Function to obtain a list of weekly Habit objects which is stored in the DB
    :param db: database to search
    :return: a list of Habit objects with a periodicity of 7
    """
    cur = db.cursor()
    cur.execute("SELECT name, description, periodicity FROM habits WHERE periodicity = 7")
    return [Habit(*item) for item in list(map(lambda x: x, cur.fetchall()))]