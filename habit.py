from datetime import date, datetime
from analyse import calculate_streak_weekly, calculate_streak_daily


class Habit:
    """
    A class to represent a habit.

    Attributes:
        name (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (int): The periodicity of the habit (1 for daily, 7 for weekly).
        longest_streak (int): The longest streak of the habit.
        current_streak (int): The current streak of the habit.
        check_dates (list[date]): A list of dates when the habit was checked in.
    """

    def __init__(self, name, description, periodicity):
        """
        Initializes the Habit class with the given name, description, and periodicity.

        :param name: The name of the habit.
        :type name: str
        :param description: A description of the habit.
        :type description: str
        :param periodicity: The periodicity of the habit (1 for daily, 7 for weekly).
        :type periodicity: int
        """
        self.name = name.lower()  # stores the name in lower case to be sure to avoid duplicate in the database
        self.description = description.lower()
        self.periodicity = periodicity  # periodicity would be 1 for daily or 7 for weekly
        self.longest_streak = 0
        self.current_streak = 0
        self.check_dates = []

    # this is only to be able to delete a habit from the list of habits
    def __eq__(self, other):
        """
        Checks if two Habit objects are equal based on their name.

        :param other: Another Habit object to compare with.

        :return: True if the names are equal, False otherwise.
        """
        return self.name == other.name

    def store(self, db):
        """
        Stores the habit into the habits table of the database.

        :param db: The database to insert into.

        :return: None
        """
        cur = db.cursor()
        cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (self.name, self.description, self.periodicity))
        db.commit()

    def add_event(self, db, event_date: str = None):
        """
        Adds a check-in date into the database and the check_dates list attribute of the habit.

        :param db: The database to insert into.
        :param event_date: The date of the event. Defaults to today's date if not provided.
        :return: None
        """
        if not event_date:
            event_date = str(date.today())
        cur = db.cursor()
        cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, self.name))
        self.check_dates.append(datetime.fromisoformat(event_date).date())
        db.commit()

    def delete_habit(self, db):
        """
        Deletes the habit from the database.

        :param db: The database to delete from.
        :return: None
        """
        cur = db.cursor()
        cur.execute("DELETE FROM tracker WHERE habit_name=?", (self.name,))
        cur.execute("DELETE FROM habits WHERE name=?", (self.name,))
        db.commit()

    def get_habit_data(self, db):
        """
        Returns all the check-in dates of the habit in its check_date attribute.

        :param db: The database to search.
        :return: None
        """
        cur = db.cursor()
        cur.execute("SELECT date FROM tracker WHERE habit_name=?", (self.name,))
        # transforming the result into a list of dates instead of a list of tuples with strings
        self.check_dates = [datetime.fromisoformat(row[0]).date() for row in cur.fetchall()]

    def calculate_streak(self):
        """
        Computes the streaks of the habit.

        A daily habit must be completed once per day and a weekly habit must be completed
        once per week between Monday and Sunday. See details in calculate_streak_daily and
        calculate_streak_weekly in analyse.py

        :return: None
        """
        if not self.check_dates:
            self.longest_streak = 0
            self.current_streak = 0
        elif self.periodicity == 1:
            self.longest_streak, self.current_streak = calculate_streak_daily(self)
        else:
            self.longest_streak, self.current_streak = calculate_streak_weekly(self)

    @classmethod
    def get_habits(cls, db):
        """
        Obtains a list of Habit objects stored in the database.

        :param db: The database to query.
        :return: A list of Habit objects.
        """
        cur = db.cursor()
        cur.execute("SELECT name, description, periodicity FROM habits")
        return [cls(*item) for item in [row for row in cur.fetchall()]]
