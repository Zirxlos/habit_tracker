from datetime import date



class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
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
        for check_date in self.check_dates:
            if event_date == check_date:
                print("You have already checked in for today")
                return
        self.check_dates.append(event_date)
        cur = db.cursor()
        cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, self.name))
        db.commit()

    def delete_habit(self, db):
        cur = db.cursor()
        cur.execute("DELETE FROM tracker WHERE habit_name=?", (self.name,))
        cur.execute("DELETE FROM habits WHERE name=?", (self.name,))
        db.commit()
