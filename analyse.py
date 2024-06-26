from datetime import timedelta, date
from operator import attrgetter
from habit import Habit


def calculate_streak(habit: Habit) -> list[int]:
    """
    function which computes streak of a Habit. A daily Habit must be made once per day and a weekly Habit must be
    done once per week between Monday and Friday.
    :type habit: object
    :return: void, the Habit is returned by the called functions and updates the Habit instance
    """
    if not habit.check_dates:
        longest_streak = 0
        current_streak = 0
        return [longest_streak, current_streak]
    elif habit.periodicity == 1:
        return calculate_streak_daily(habit)
    else:
        return calculate_streak_weekly(habit)


def calculate_streak_daily(habit: Habit) -> list[int]:
    """
    Calculate the longest and current streak of a daily habit
    :param habit: daily habit to input
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

    if habit.check_dates and sorted_dates[-1] != date.today():
        current_streak = 0

    return [longest_streak, current_streak]


def calculate_streak_weekly(habit: Habit) -> list[int]:
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

        if check_in_date > week_end and week_checked:  # goes to the next week when current week checked
            week_begin += timedelta(days=7)
            week_end = week_begin + timedelta(days=6)
            week_checked = False

        if check_in_date > week_end and not week_checked:  # goes to the next week when current week not checked
            week_begin += timedelta(days=7)
            week_end = week_begin + timedelta(days=6)
            current_streak = 1
            week_checked = True

        if week_begin <= check_in_date <= week_end and not week_checked:  # check if date is in current week when
            # week not checked
            week_checked = True
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)

        # no need to check if date is in current week and week checked because nothing would happen anyway

    # this is to be sure the current streak is 0 if a habit is checked for current streak and the day the user checks
    # is already too late to get a +1  to the streak
    if habit.check_dates and date.today() - sorted_dates[-1] >= 2 * timedelta(days=habit.periodicity):
        current_streak = 0

    return [longest_streak, current_streak]


def strongest_weakest_habit(habits: list[Habit]) -> list[Habit]:
    """
    function to extract the habit with the highest streak ever
    :param habits:
    :return: a list with the habit with the max "longest_streak" at index 0 and the habit with the min "longest_streak"
    at index 1
    """
    # habits = hb.get_habits(db)
    for habit in habits:
        habit.longest_streak, habit.current_streak = calculate_streak(habit)
    return [max(habits, key=attrgetter('longest_streak')), min(habits, key=attrgetter('longest_streak'))]


def get_habits(db, periodicity: str = None) -> list[Habit]:
    """
    Function to obtain a list of Habit objects (daily, weekly or all of them) which is stored in the DB.
    :param periodicity: "daily" or "weekly". If no argument, or any other, default is to all habits.
    :param db: database to search
    :return: a list of Habit objects
    """
    cur = db.cursor()
    if periodicity == "daily":
        cur.execute("SELECT name, description, periodicity FROM habits WHERE periodicity = 1")
    elif periodicity == "weekly":
        cur.execute("SELECT name, description, periodicity FROM habits WHERE periodicity = 7")
    else:
        cur.execute("SELECT name, description, periodicity FROM habits")
    return [Habit(*item) for item in [row for row in cur.fetchall()]]
