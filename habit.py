from datetime import date, datetime
from analyse import calculate_streak_daily, calculate_streak_weekly


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name.lower()  # stores the name in lower case to be sure to avoid duplicate in the database
        self.description = description.lower()
        self.periodicity = periodicity  # periodicity would be 1 for daily or 7 for weekly
        self.longest_streak = 0
        self.current_streak = 0
        self.check_dates = []

    # this is only to be able to delete a habit from the list of habits
    def __eq__(self, other):
        return self.name == other.name

    def store(self, db):
        """
        method to store the habit into the habits table of the database
        :param db: database to insert into
        :return: void
        """
        cur = db.cursor()
        cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (self.name, self.description, self.periodicity))
        db.commit()

    def add_event(self, db, event_date: str = None):
        """
        method to add a check in date into the database and inside the check_dates list attribute of the habit
        :param db: database to insert into
        :param event_date: if no date inserted, will default to todays date
        :return: void
        """
        if not event_date:
            event_date = str(date.today())
        cur = db.cursor()
        cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, self.name))
        self.check_dates.insert(0, datetime.fromisoformat(event_date).date())
        db.commit()

    def delete_habit(self, db):
        """
        method to delete the habit from the database
        :param db: database to delete from
        :return: void
        """
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
        self.check_dates = [datetime.fromisoformat(row[0]).date() for row in cur.fetchall()]

    def calculate_streak(self):
        """
        function which computes streak of a Habit. A daily Habit must be made once per day and a weekly Habit must be
        done once per week between Monday and Friday.
        :return: void, the Habit is returned by the called functions and updates the Habit instance
        """
        if not self.check_dates:
            self.longest_streak = 0
            self.current_streak = 0
        elif self.periodicity == 1:
            calculate_streak_daily(self)
        else:
            calculate_streak_weekly(self)
