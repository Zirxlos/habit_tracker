from __future__ import annotations
from datetime import timedelta, date
from operator import attrgetter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from habit import Habit


def calculate_streak_daily(habit: Habit) -> list[int]:
    """
    Calculates the longest and current streak of a daily habit.

    This function determines the longest streak of uninterrupted check-ins for
    a daily habit. It also calculates the current streak up to the most recent
    check-in date.

    :param habit: A Habit class object representing the daily habit for which the streaks are calculated.

    :return: A list containing the longest streak and the current streak of the habit.
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

    if habit.check_dates and sorted_dates[-1] != date.today():
        current_streak = 0

    return [longest_streak, current_streak]


def calculate_streak_weekly(habit: Habit) -> list[int]:
    """
    Computes the longest and current streak of a weekly Habit.

    A habit needs to be completed at least once every 7 days to maintain a streak.
    For example, if a habit is completed 8 times in 8 consecutive days, it will
    compute a streak of 2.

    :param habit: A Habit class object for which the longest and current streak are to be calculated.

    :return: A list containing the longest streak and the current streak.
    """
    sorted_dates = sorted(habit.check_dates)
    longest_streak = 0
    current_streak = 0
    week_checked = False
    week_begin = sorted_dates[0] - timedelta(days=sorted_dates[0].weekday())  # Monday of the first week

    for check_in_date in sorted_dates:
        week_end = week_begin + timedelta(days=6)  # Sunday of the current week

        if check_in_date > week_end and week_checked:
            # goes to the next week when current week checked
            week_begin += timedelta(days=7)
            week_end = week_begin + timedelta(days=6)
            week_checked = False

        if check_in_date > week_end and not week_checked:
            # goes to the next week when current week not checked
            week_begin += timedelta(days=7)
            week_end = week_begin + timedelta(days=6)
            current_streak = 1
            week_checked = True

        if week_begin <= check_in_date <= week_end and not week_checked:
            # check if date is in current week when week not checked
            week_checked = True
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)

        # no need to check if date is in current week and week checked because nothing would happen anyway

    # this is to be sure the current streak is 0 if a habit is checked for current streak and the day the user checks
    # is already too late to get a +1  to the streak
    if habit.check_dates and date.today() - sorted_dates[-1] >= 2 * timedelta(days=habit.periodicity):
        current_streak = 0

    return [longest_streak, current_streak]


def strongest_daily_habit(habits: list[Habit]) -> Habit:
    """
    Determines the strongest daily habit based on the longest streak.

    This function filters the given list of habits to only include those with a
    periodicity of 1 (daily habits). It then computes the streaks for these daily
    habits and returns the habit with the longest streak.

    :param habits: A list of Habit objects to be evaluated.

    :return: The Habit object with the longest streak among the daily habits.
    """
    daily_habits = [habit for habit in habits if habit.periodicity == 1]
    compute_streaks_for_a_list_of_habits(daily_habits)
    return max(daily_habits, key=attrgetter('longest_streak'))


def weakest_daily_habit(habits: list[Habit]) -> Habit:
    """
    Determines the weakest daily habit based on the shortest streak.

    This function filters the given list of habits to only include those with a
    periodicity of 1 (daily habits). It then computes the streaks for these daily
    habits and returns the habit with the shortest streak.

    :param habits: A list of Habit objects to be evaluated.

    :return: The Habit object with the shortest streak among the daily habits.
    """
    daily_habits = [habit for habit in habits if habit.periodicity == 1]
    compute_streaks_for_a_list_of_habits(daily_habits)
    return min(daily_habits, key=attrgetter('longest_streak'))


def strongest_weekly_habit(habits: list[Habit]) -> Habit:
    """
    Determines the strongest weekly habit based on the longest streak.

    This function filters the given list of habits to only include those with a
    periodicity of 7 (weekly habits). It then computes the streaks for these weekly
    habits and returns the habit with the longest streak.

    :param habits: A list of Habit objects to be evaluated.

    :return: The Habit object with the longest streak among the weekly habits.
    """
    weekly_habits = [habit for habit in habits if habit.periodicity == 7]
    compute_streaks_for_a_list_of_habits(weekly_habits)
    return max(weekly_habits, key=attrgetter('longest_streak'))


def weakest_weekly_habit(habits: list[Habit]) -> Habit:
    """
    Determines the weakest weekly habit based on the shortest streak.

    This function filters the given list of habits to only include those with a
    periodicity of 7 (weekly habits). It then computes the streaks for these weekly
    habits and returns the habit with the shortest streak.

    :param habits: A list of Habit objects to be evaluated.

    :return: The Habit object with the shortest streak among the weekly habits.
    """
    weekly_habits = [habit for habit in habits if habit.periodicity == 7]
    compute_streaks_for_a_list_of_habits(weekly_habits)
    return min(weekly_habits, key=attrgetter('longest_streak'))


def compute_streaks_for_a_list_of_habits(habits: list[Habit]):
    """
    Computes the streaks for a list of habits.

    This function iterates over the given list of habits and calculates the
    streak for each habit by calling the `calculate_streak` method on each Habit
    object.

    :param habits: A list of Habit objects for which streaks need to be calculated.

    :return: None
    """
    for habit in habits:
        habit.calculate_streak()
