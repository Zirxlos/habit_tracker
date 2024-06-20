from datetime import timedelta, date
from operator import attrgetter


def calculate_streak_daily(habit):
    """
    Calculate the longest and current streak of a daily Habit
    :param habit: Habit class object from which we want to get the longest and current streak
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

    if habit.check_dates and sorted_dates[0] != date.today():
        current_streak = 0

    habit.longest_streak = longest_streak
    habit.current_streak = current_streak

    return habit


def calculate_streak_weekly(habit):
    """
    computes the longest and current streak of a weekly Habit
    a habit needs to be completed at least every 7 days. If a habit is completed 8 times
    8 days in a row, it will compute a streak of 2
    :param habit: Habit class object from which we want to get the longest and current streak
    :return:
    """
    sorted_dates = sorted(habit.check_dates)
    longest_streak = 0
    current_streak = 0
    week_checked = False
    week_begin = sorted_dates[0] - timedelta(days=sorted_dates[0].weekday())  # Monday of the first week

    for check_in_date in sorted_dates:
        week_end = week_begin + timedelta(days=6)  # Sunday of the current week

        if check_in_date > week_end and week_checked:
            week_begin += timedelta(days=7)
            week_end = week_begin + timedelta(days=6)
            week_checked = False

        if check_in_date > week_end and not week_checked:
            week_begin += timedelta(days=7)
            week_end = week_begin + timedelta(days=6)
            current_streak = 1
            week_checked = True

        if week_begin <= check_in_date <= week_end and not week_checked:
            week_checked = True
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)

    if habit.check_dates and date.today() - sorted_dates[-1] >= 2 * timedelta(days=habit.periodicity):
        current_streak = 0

    habit.longest_streak = longest_streak
    habit.current_streak = current_streak

    return habit


def strongest_weakest_habit(db, habits):
    """
    function to extract the habit with the highest streak ever
    :param habits:
    :param db: database to search
    :return: a list with the habit with the max "longest_streak" at index 0 and the habit with the min "longest_streak"
    at index 1
    """
    #habits = hb.get_habits(db)
    for habit in habits:
        habit.calculate_streak(db)
    return [max(habits, key=attrgetter('longest_streak')), min(habits, key=attrgetter('longest_streak'))]