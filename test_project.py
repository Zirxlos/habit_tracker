from habit import Habit, get_weekly_habits, get_daily_habits, get_habits
from db import get_db
import os
from analyse import compute_strongest_habit, compute_weakest_habit


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")
        self.test_daily_habit = Habit("test_daily_habit", "test_daily_habit_desc", 1)
        self.test_weekly_habit = Habit("test_weekly_habit", "test_weekly_habit_desc", 7)
        self.test_strongest_habit = Habit("test_strongest_habit", "test_strongest_habit_desc",
                                          1)
        self.test_weakest_habit = Habit("test_weakest_habit", "test_weakest_habit_desc", 7)
        self.test_weekly_habit_computing = Habit("test_weekly_habit_computing",
                                                 "test_weekly_habit_computing_desc", 7)

        self.test_daily_habit.store(self.db)
        self.test_weekly_habit.store(self.db)
        self.test_strongest_habit.store(self.db)
        self.test_weakest_habit.store(self.db)
        self.test_weekly_habit_computing.store(self.db)

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
        self.test_weekly_habit.add_event(self.db, "2024-06-03")
        self.test_weekly_habit.add_event(self.db, "2024-06-12")

        self.test_weekly_habit_computing.add_event(self.db, "2024-05-01")
        self.test_weekly_habit_computing.add_event(self.db, "2024-05-12")
        self.test_weekly_habit_computing.add_event(self.db, "2024-05-13")
        self.test_weekly_habit_computing.add_event(self.db, "2024-05-14")
        self.test_weekly_habit_computing.add_event(self.db, "2024-05-15")
        self.test_weekly_habit_computing.add_event(self.db, "2024-05-16")
        self.test_weekly_habit_computing.add_event(self.db, "2024-05-23")
        self.test_weekly_habit_computing.add_event(self.db, "2024-06-02")
        self.test_weekly_habit_computing.add_event(self.db, "2024-06-19")

    def test_habit(self):
        habit1 = Habit("test_habit_1", "test_description_1", 1)
        habit2 = Habit("test_habit_2", "test_description_2", 7)

        habit1.store(self.db)
        habit2.store(self.db)

    def test_db_habit(self):
        self.test_daily_habit.get_habit_data(self.db)
        assert len(self.test_daily_habit.check_dates) == 4

        self.test_weekly_habit.get_habit_data(self.db)
        assert len(self.test_weekly_habit.check_dates) == 3

    def test_calculate_streak(self):
        self.test_daily_habit.calculate_streak(self.db)
        assert self.test_daily_habit.longest_streak == 4
        assert self.test_daily_habit.current_streak == 0

        self.test_weekly_habit.calculate_streak(self.db)
        assert self.test_weekly_habit.longest_streak == 3
        assert self.test_weekly_habit.current_streak == 3

        assert compute_strongest_habit(self.db, get_habits(self.db)).longest_streak == 8
        assert compute_weakest_habit(self.db, get_habits(self.db)).longest_streak == 0

        self.test_weekly_habit_computing.calculate_streak(self.db)
        assert self.test_weekly_habit_computing.longest_streak == 5
        assert self.test_weekly_habit_computing.current_streak == 1

    def test_get_habits(self):
        assert len(get_habits(self.db)) == 5
        assert len(get_weekly_habits(self.db)) == 3
        assert len(get_daily_habits(self.db)) == 2

    def teardown_method(self):
        self.db.close()
        os.remove("test.db")
