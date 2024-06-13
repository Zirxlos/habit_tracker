from habit import Habit
from db import get_db, get_habit_data
import os
from analyse import calculate_streak, compute_strongest_habit, compute_weakest_habit


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")
        self.test_daily_habit = Habit("test_daily_habit", "test_daily_habit_desc", 1)
        self.test_weekly_habit = Habit("test_weekly_habit", "test_weekly_habit_desc", 7)
        self.test_strongest_habit = Habit("test_strongest_habit", "test_strongest_habit_desc", 1)
        self.test_weakest_habit = Habit("test_weakest_habit", "test_weakest_habit_desc", 7)

        self.test_daily_habit.store(self.db)
        self.test_weekly_habit.store(self.db)
        self.test_strongest_habit.store(self.db)
        self.test_weakest_habit.store(self.db)

        self.test_daily_habit.add_event(self.db, "2024-06-09")
        self.test_daily_habit.add_event(self.db, "2024-06-10")
        self.test_daily_habit.add_event(self.db, "2024-06-11")
        self.test_daily_habit.add_event(self.db, "2024-06-12")

        self.test_strongest_habit.add_event(self.db, "2024-06-05")
        self.test_strongest_habit.add_event(self.db, "2024-06-06")
        self.test_strongest_habit.add_event(self.db, "2024-06-07")
        self.test_strongest_habit.add_event(self.db, "2024-06-08")
        self.test_strongest_habit.add_event(self.db, "2024-06-09")
        self.test_strongest_habit.add_event(self.db, "2024-06-10")
        self.test_strongest_habit.add_event(self.db, "2024-06-11")
        self.test_strongest_habit.add_event(self.db, "2024-06-12")

        self.test_weekly_habit.add_event(self.db, "2024-05-27")
        self.test_weekly_habit.add_event(self.db, "2024-06-02")
        self.test_weekly_habit.add_event(self.db, "2024-06-12")

    def test_habit(self):
        habit1 = Habit("test_habit_1", "test_description_1", 1)
        habit2 = Habit("test_habit_2", "test_description_2", 7)

        habit1.store(self.db)
        habit2.store(self.db)

    def test_db_habit(self):
        daily_data = get_habit_data(self.db, self.test_daily_habit)
        assert len(daily_data.check_dates) == 4

        calculate_streak(self.db, self.test_daily_habit)
        assert self.test_daily_habit.longest_streak == 4

        weekly_data = get_habit_data(self.db, self.test_weekly_habit)
        assert len(weekly_data.check_dates) == 3

        calculate_streak(self.db, self.test_weekly_habit)
        assert self.test_weekly_habit.longest_streak == 2

        assert compute_strongest_habit(self.db).longest_streak == 8
        assert compute_weakest_habit(self.db).longest_streak == 0



    def teardown_method(self):
        self.db.close()
        os.remove("test.db")