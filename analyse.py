from db import get_habit_data, get_habits
from datetime import timedelta
from habit import Habit
from operator import attrgetter


def calculate_streak(db, habit):
    """
    Calculate the longest streak of a habit

    :param db: initialised sqlite3 database connection
    :param habit: name of the habit
    :return: the longest streak of uninterrupted check-in of the habit
    """
    sorted_dates = sorted(get_habit_data(db, habit).check_dates)
    longest_streak = 1
    current_streak = 1
    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] - sorted_dates[i - 1] <= timedelta(days=habit.periodicity):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
    habit.longest_streak = longest_streak
    habit.current_streak = current_streak

    return habit

def compute_strongest_habit(db):
    habits = get_habits(db)
    for habit in habits:
        calculate_streak(db, habit)
    return max(habits, key=attrgetter('longest_streak'))

def compute_weakest_habit(db):
    habits = get_habits(db)
    for habit in habits:
        calculate_streak(db, habit)
    return min(habits, key=attrgetter('longest_streak'))

