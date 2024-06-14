from datetime import timedelta, date
from operator import attrgetter
import habit as hb


def calculate_streak_daily(habit):
    """
    Calculate the longest streak of a habit
    :param habit: Habit class object
    :return: the longest streak of uninterrupted check-in of the habit
    """
    sorted_dates = sorted(habit.check_dates)
    longest_streak = 1
    current_streak = 1
    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] - sorted_dates[i - 1] <= timedelta(days=habit.periodicity):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
    # putting back the streaks to 0 because for computing if no checked in date, they are set to 1
    if habit.check_dates and sorted_dates[0] != date.today():
        current_streak = 0

    habit.longest_streak = longest_streak
    habit.current_streak = current_streak

    return habit


def calculate_streak_weekly(habit):
    sorted_dates = sorted(habit.check_dates)
    longest_streak = 1
    current_streak = 1
    week_checked = False
    week_begin = sorted_dates[0]
    for i in range(1, len(sorted_dates)):
        if week_begin - sorted_dates[i - 1] >= timedelta(days=habit.periodicity):
            week_checked = False
        if sorted_dates[i] - sorted_dates[i - 1] <= timedelta(days=habit.periodicity) and not week_checked:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
            week_checked = True
            week_begin = sorted_dates[i - 1]
        elif week_checked:
            pass
        else:
            current_streak = 1

    if habit.check_dates and date.today() - sorted_dates[0] >= timedelta(days=habit.periodicity):
        current_streak = 0

    habit.longest_streak = longest_streak
    habit.current_streak = current_streak

    return habit


def compute_strongest_habit(db):
    """
    function to extract the habit with the highest streak ever
    :param db: database to search
    :return: the habit with the max "longest_streak"
    """
    habits = hb.get_habits(db)
    for habit in habits:
        habit.calculate_streak(db)
    return max(habits, key=attrgetter('longest_streak'))


def compute_weakest_habit(db):
    """
    function to extract the habit with the lowest streak ever
    :param db: database to search
    :return: the habit with the min "longest_streak"
    """
    habits = hb.get_habits(db)
    for habit in habits:
        habit.calculate_streak(db)
    return min(habits, key=attrgetter('longest_streak'))
