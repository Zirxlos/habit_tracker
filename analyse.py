from db import get_habit_data, get_habit
from datetime import timedelta, datetime
from habit import Habit


def calculate_longest_streak(db, habit):
    """
    Calculate the longest streak of a habit

    :param db: initialised sqlite3 database connection
    :param habit: name of the habit
    :return: the longest streak of uninterrupted check-in of the habit
    """
    data = get_habit_data(db, habit)
    current_habit = Habit(*list(map(lambda x: x, *get_habit(db, habit))))
    sorted_dates = sorted(list(map(lambda x: x[0], data)))
    ##sorted_dates = sorted(list(map(lambda x: x[0], get_habit_data(db, habit))))
    longest_streak = 1
    current_streak = 1
    for i in range(1, len(sorted_dates)):
        if datetime.strptime(sorted_dates[i], '%Y-%m-%d') - datetime.strptime(sorted_dates[i - 1], '%Y-%m-%d') <= timedelta(days=current_habit.periodicity):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        ##if sorted_dates[i] - sorted_dates[i - 1] == timedelta(days=habit.periodicity):
        ##    current_streak += 1
        ##    longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    return longest_streak