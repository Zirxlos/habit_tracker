from datetime import date, datetime
from analyse import calculate_streak_weekly, calculate_streak_daily


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
        method to store the habit into the habits table of the DB
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
        :param event_date: if no date inserted, will default to today's date
        :return: void
        """
        if not event_date:
            event_date = str(date.today())
        cur = db.cursor()
        cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, self.name))
        self.check_dates.append(datetime.fromisoformat(event_date).date())
        db.commit()

    def delete_habit(self, db):
        """
        method to delete the habit from the DB
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
        Method which computes streak of a Habit. A daily Habit must be made once per day and a weekly Habit must be
        done once per week between Monday and Sunday.
        :return:
        """
        if not self.check_dates:
            longest_streak = 0
            current_streak = 0
            return [longest_streak, current_streak]
        elif self.periodicity == 1:
            self.longest_streak, self.current_streak = calculate_streak_daily(self)
        else:
            self.longest_streak, self.current_streak = calculate_streak_weekly(self)

    @classmethod
    def get_habits(cls, db):
        """
        Class method to obtain a list of objects (daily, weekly or all of them) which is stored in the DB.
        :param periodicity:
        :return:
        """
        cur = db.cursor()
        cur.execute("SELECT name, description, periodicity FROM habits")
        return [cls(*item) for item in [row for row in cur.fetchall()]]