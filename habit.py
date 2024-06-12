from db import add_habit, increment_tracker


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.longest_streak = 0
        self.current_streak = 0
        self.check_dates = []

    def check(self, date: str = None):
        pass
    def store(self, db):
        add_habit(db, self.name, self.description, self.periodicity)

    def add_event(self, db, date: str = None):
        increment_tracker(db, self.name, date)