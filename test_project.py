from habit import Habit
from db import get_db, add_habit, increment_tracker, get_habit_data
import os
from analyse import calculate_longest_streak


class TestCounter:

    def setup_method(self):
        self.db = get_db("test.db")
        add_habit(self.db, "test_daily_habit", "test_daily_habit_desc", 1)
        add_habit(self.db, "test_weekly_habit", "test_weekly_habit_desc", 7)

        increment_tracker(self.db, "test_daily_habit", "2024-06-09")
        increment_tracker(self.db, "test_daily_habit", "2024-06-10")
        increment_tracker(self.db, "test_daily_habit", "2024-06-11")
        increment_tracker(self.db, "test_daily_habit", "2024-06-12")
        print(get_habit_data(self.db, "test_daily_habit"))

        increment_tracker(self.db, "test_weekly_habit", "2024-05-27")
        increment_tracker(self.db, "test_weekly_habit", "2024-06-02")
        increment_tracker(self.db, "test_weekly_habit", "2024-06-12")

    def test_habit(self):
        habit1 = Habit("test_habit_1", "test_description_1", 1)
        habit2 = Habit("test_habit_2", "test_description_2", 7)

        habit1.store(self.db)
        habit2.store(self.db)

    def test_db_habit(self):
        daily_data = get_habit_data(self.db, "test_daily_habit")
        assert len(daily_data) == 4

        daily_count = calculate_longest_streak(self.db, "test_daily_habit")
        assert daily_count == 4

        weekly_data = get_habit_data(self.db, "test_weekly_habit")
        assert len(weekly_data) == 3

        weekly_count = calculate_longest_streak(self.db, "test_weekly_habit")
        assert weekly_count == 2


    def teardown_method(self):
        self.db.close()
        os.remove("test.db")