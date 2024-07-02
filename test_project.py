from habit import Habit
from db import get_db
import os
from analyse import (get_habits, calculate_streak, strongest_daily_habit, strongest_weekly_habit, weakest_daily_habit,
                     weakest_weekly_habit)
from datetime import date, timedelta


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")
        self.habits = []
        self.test_daily_habit = Habit("test_daily_habit", "test_daily_habit_desc", 1)
        self.test_weekly_habit = Habit("test_weekly_habit", "test_weekly_habit_desc", 7)
        self.test_strongest_weekly_habit = Habit("test_strongest_weekly_habit", "test_strongest_weekly_habit_desc", 7)
        self.test_strongest_daily_habit = Habit("test_strongest_daily_habit", "test_strongest_habit_desc", 1)
        self.test_weakest_weekly_habit = Habit("test_weakest_weekly_habit", "test_weakest_weekly_habit_desc", 7)
        self.test_weakest_daily_habit = Habit("test_weakest_daily_habit", "test_weakest_daily_habit_desc", 1)

        self.test_daily_habit.store(self.db)
        self.habits.append(self.test_daily_habit)
        self.test_strongest_weekly_habit.store(self.db)
        self.habits.append(self.test_strongest_weekly_habit)
        self.test_strongest_daily_habit.store(self.db)
        self.habits.append(self.test_strongest_daily_habit)
        self.test_weakest_weekly_habit.store(self.db)
        self.habits.append(self.test_weakest_weekly_habit)
        self.test_weakest_daily_habit.store(self.db)
        self.habits.append(self.test_weakest_daily_habit)
        self.test_weekly_habit.store(self.db)
        self.habits.append(self.test_weekly_habit)

        for i in range(2, 21):
            self.test_daily_habit.add_event(self.db, str(date.today() - timedelta(days=i)))

        for i in range(14, 22, 7):
            self.test_weekly_habit.add_event(self.db, str(date.today() - timedelta(days=i)))

        for i in range(21):
            self.test_strongest_daily_habit.add_event(self.db, str(date.today() - timedelta(days=i)))
            self.test_strongest_weekly_habit.add_event(self.db, str(date.today() - timedelta(days=i)))

        self.test_weakest_weekly_habit.add_event(self.db, str(date.today() - timedelta(days=15)))

        for i in range(0, 21, 2):
            self.test_weakest_daily_habit.add_event(self.db, str(date.today() - timedelta(days=i)))


    def test_habit(self):
        habit1 = Habit("test_habit_1", "test_description_1", 1)
        habit2 = Habit("test_habit_2", "test_description_2", 7)

        habit1.store(self.db)
        habit2.store(self.db)

    def test_db_habit(self):
        self.test_daily_habit.get_habit_data(self.db)
        assert len(self.test_daily_habit.check_dates) == 19

        self.test_strongest_weekly_habit.get_habit_data(self.db)
        assert len(self.test_strongest_weekly_habit.check_dates) == 21

    def test_calculate_streak(self):
        (self.test_daily_habit.longest_streak,
         self.test_daily_habit.current_streak) = calculate_streak(self.test_daily_habit)
        assert self.test_daily_habit.longest_streak == 19
        assert self.test_daily_habit.current_streak == 0

        (self.test_weekly_habit.longest_streak,
         self.test_weekly_habit.current_streak) = calculate_streak(self.test_weekly_habit)
        assert self.test_weekly_habit.longest_streak == 2
        assert self.test_weekly_habit.current_streak == 0

        (self.test_strongest_weekly_habit.longest_streak,
         self.test_strongest_weekly_habit.current_streak) = calculate_streak(self.test_strongest_weekly_habit)
        assert self.test_strongest_weekly_habit.longest_streak == 4
        assert self.test_strongest_weekly_habit.current_streak == 4

        (self.test_strongest_daily_habit.longest_streak,
         self.test_strongest_daily_habit.current_streak) = calculate_streak(self.test_strongest_daily_habit)
        assert self.test_strongest_daily_habit.longest_streak == 21
        assert self.test_strongest_daily_habit.current_streak == 21

        (self.test_weakest_weekly_habit.longest_streak,
         self.test_weakest_weekly_habit.current_streak) = calculate_streak(self.test_weakest_weekly_habit)
        assert self.test_weakest_weekly_habit.longest_streak == 1
        assert self.test_weakest_weekly_habit.current_streak == 0

        (self.test_weakest_daily_habit.longest_streak,
         self.test_weakest_daily_habit.current_streak) = calculate_streak(self.test_weakest_daily_habit)
        assert self.test_weakest_daily_habit.longest_streak == 1
        assert self.test_weakest_daily_habit.current_streak == 1


    def test_strongest_and_weakest_habits(self):
        assert strongest_daily_habit(self.habits).longest_streak == 21
        assert weakest_daily_habit(self.habits).longest_streak == 1

        assert strongest_weekly_habit(self.habits).longest_streak == 4
        assert weakest_weekly_habit(self.habits).longest_streak == 1


    def test_get_habits(self):
        assert len(get_habits(self.db)) == 6
        assert len(get_habits(self.db, "weekly")) == 3
        assert len(get_habits(self.db, "daily")) == 3

    def teardown_method(self):
        self.db.close()
        os.remove("test.db")
