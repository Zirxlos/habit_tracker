from db import get_habit_data, get_habits
from datetime import timedelta
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
    """
    function to extract the habit with the highest streak ever
    :param db: database to search
    :return: the habit with the max "longest_streak"
    """
    habits = get_habits(db)
    for habit in habits:
        calculate_streak(db, habit)
    return max(habits, key=attrgetter('longest_streak'))

def compute_weakest_habit(db):
    """
    function to extract the habit with the lowest streak ever
    :param db: database to search
    :return: the habit with the min "longest_streak"
    """
    habits = get_habits(db)
    for habit in habits:
        calculate_streak(db, habit)
        ## putting back the streaks to 0 because for computing sake, they are set to 1 in "calculate_streak"
        if habit.check_dates == []:
            habit.longest_streak = 0
            habit.current_streak = 0
    return min(habits, key=attrgetter('longest_streak'))

