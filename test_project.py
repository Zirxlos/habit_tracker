from habit import Habit
from db import get_db
import os
from analyse import strongest_daily_habit, strongest_weekly_habit, weakest_daily_habit, weakest_weekly_habit
from datetime import date, timedelta


class TestHabit:
    """
    Test suite for the Habit class and its methods.
    """

    def setup_method(self):
        """
        Setup method to initialize the test database and test habits.
        This method creates a test database and populates it with multiple habits and events.
        """
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

    def test_get_habit_data(self):
        """
        Test the get_habit_data method to ensure it retrieves the correct check-in dates.
        """
        self.test_daily_habit.get_habit_data(self.db)
        assert len(self.test_daily_habit.check_dates) == 19

        self.test_strongest_weekly_habit.get_habit_data(self.db)
        assert len(self.test_strongest_weekly_habit.check_dates) == 21

    def test_delete_habit(self):
        """
        Test the delete_habit method to ensure habits are removed from the database correctly.
        """
        self.test_daily_habit.delete_habit(self.db)
        self.test_strongest_weekly_habit.delete_habit(self.db)
        self.test_strongest_daily_habit.delete_habit(self.db)
        self.test_weakest_weekly_habit.delete_habit(self.db)
        self.test_weakest_daily_habit.delete_habit(self.db)
        self.test_weekly_habit.delete_habit(self.db)
        assert len(Habit.get_habits(self.db)) == 0

    def test_calculate_streak(self):
        """
        Test the calculate_streak method to verify the longest and current streak calculations for daily
        and weekly habits.
        """
        self.test_daily_habit.calculate_streak()
        assert self.test_daily_habit.longest_streak == 19
        assert self.test_daily_habit.current_streak == 0

        self.test_weekly_habit.calculate_streak()
        assert self.test_weekly_habit.longest_streak == 2
        assert self.test_weekly_habit.current_streak == 0

        self.test_strongest_weekly_habit.calculate_streak()
        assert self.test_strongest_weekly_habit.longest_streak == 4
        assert self.test_strongest_weekly_habit.current_streak == 4

        self.test_strongest_daily_habit.calculate_streak()
        assert self.test_strongest_daily_habit.longest_streak == 21
        assert self.test_strongest_daily_habit.current_streak == 21

        self.test_weakest_weekly_habit.calculate_streak()
        assert self.test_weakest_weekly_habit.longest_streak == 1
        assert self.test_weakest_weekly_habit.current_streak == 0

        self.test_weakest_daily_habit.calculate_streak()
        assert self.test_weakest_daily_habit.longest_streak == 1
        assert self.test_weakest_daily_habit.current_streak == 1

    def test_strongest_and_weakest_habits(self):
        """
        Test the functions to find the strongest and weakest habits for both daily and weekly habits.
        """
        assert strongest_daily_habit(self.habits).longest_streak == 21
        assert weakest_daily_habit(self.habits).longest_streak == 1

        assert strongest_weekly_habit(self.habits).longest_streak == 4
        assert weakest_weekly_habit(self.habits).longest_streak == 1

    def test_get_habits(self):
        """
        Test the get_habits class method to ensure it retrieves all habits from the database.
        """
        assert len(Habit.get_habits(self.db)) == 6

    def teardown_method(self):
        """
        Teardown method to close the database connection and remove the test database file.
        """
        self.db.close()
        os.remove("test.db")
