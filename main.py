import questionary
from habit import Habit
from db import get_db
from analyse import calculate_streak, get_habits, strongest_daily_habit, strongest_weekly_habit, weakest_weekly_habit, weakest_daily_habit
import sqlite3
from rich import print

# loading the whole database
db = get_db()
habits = get_habits(db)  # creating a global list
for item in habits:
    item.get_habit_data(db)  # loading all the checked in dates


def main_menu():
    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "Create a Habit",
            "Get Feedback on your Habits",
            "See Habits",
            "Exit"
        ]
    ).ask()

    if choice == "Create a Habit":
        create_habit()
    elif choice == "Get Feedback on your Habits":
        feedback()
    elif choice == "See Habits":
        see_habits()
    elif choice == "Exit":
        db.close()
        exit()


def create_habit():
    name = questionary.text("What is the name of your habit?").ask()
    description = questionary.text('Please insert a description:').ask()
    periodicity = questionary.select("How often do you want to do this habit?", choices=["Daily", "Weekly"]).ask()

    if periodicity == "Daily":
        period = 1
    else:
        period = 7

    new_habit = Habit(name=name, description=description, periodicity=period)

    try:
        new_habit.store(db)  # updating database
        habits.append(new_habit)  # updating global list
        print(f'[blue]You added "{new_habit.name}" to your habits[/blue]')
    except sqlite3.IntegrityError:
        print(f'[red]Habit "{new_habit.name}" already in database, please retry[red]')

    main_menu()


def feedback():
    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "See my Strongest Daily Habit",
            "See my Weakest Daily Habit",
            "See my Strongest Weekly Habit",
            "See my Weakest Weekly Habit",
            "Main Menu"
        ]
    ).ask()

    if choice == "See my Strongest Daily Habit":
        strongest_day_habit = strongest_daily_habit(habits)
        print(f'Your [green]strongest daily habit[/green] is [green]"{strongest_day_habit.name.capitalize()}"[/green] '
              f'with a longest streak of [green]{strongest_day_habit.longest_streak}[/green]')
        main_menu()
    elif choice == "See my Weakest Daily Habit":
        weakest_day_habit = weakest_daily_habit(habits)
        print(f'Your [blue]weakest daily habit[/blue] is [blue]"{weakest_day_habit.name.capitalize()}"[/blue] with '
              f'a longest streak of [blue]{weakest_day_habit.longest_streak}[/blue]')
        main_menu()
    elif choice == "See my Strongest Weekly Habit":
        strongest_week_habit = strongest_weekly_habit(habits)
        print(
            f'Your [green]strongest weekly habit[/green] is [green]"{strongest_week_habit.name.capitalize()}"[/green] '
            f'with a longest streak of [green]{strongest_week_habit.longest_streak}[/green]')
        main_menu()
    elif choice == "See my Weakest Weekly Habit":
        weakest_week_habit = weakest_weekly_habit(habits)
        print(
            f'Your [blue]weakest weekly habit[/blue] is [blue]"{weakest_week_habit.name.capitalize()}"[/blue] with a '
            f'longest streak of [blue]{weakest_week_habit.longest_streak}[/blue]')
        main_menu()
    else:
        main_menu()


def see_habits(frequency=None):
    if frequency is None:
        list_of_choices = ["Show daily habits", "Show weekly habits"] + [habit.name.capitalize() for habit in
                                                                         habits] + ["Main Menu"]
    elif frequency == "daily":
        list_of_choices = [habit.name.capitalize() for habit in habits if habit.periodicity == 1] + ["Back"] + ["Main "
                                                                                                                "Menu"]
    else:
        list_of_choices = [habit.name.capitalize() for habit in habits if habit.periodicity == 7] + ["Back"] + [
            "Main Menu"]
    choice = questionary.select(
        "Please chose a habit:",
        choices=list_of_choices,
        use_shortcuts=True
    ).ask()

    if choice == "Main Menu":
        main_menu()
    if choice == "Show daily habits":
        see_habits("daily")
    if choice == "Show weekly habits":
        see_habits("weekly")
    if choice == "Back":
        see_habits()

    for habit in habits:
        if choice == habit.name.capitalize():
            habit.get_habit_data(db)
            habit_menu(habit)
            return

    main_menu()


def habit_menu(habit):
    habit_name = habit.name.capitalize()
    choice = questionary.select(
        "What do you want to do?",
        choices=[
            f'Complete "{habit_name}"',
            f'Delete "{habit_name}"',
            f'See Current Streak of "{habit_name}"',
            f'See Longest Streak of "{habit_name}"',
            f'See description of "{habit_name}"',
            "Back to Habit List"
        ]
    ).ask()

    if choice == f'Complete "{habit_name}"':
        try:
            habit.add_event(db)
            print(f'[green]You successfully check in on {habit.check_dates[0]} for "{habit_name}" [/green]'
                  f'[green]which consists of "{habit.description}"[/green]')
        except sqlite3.IntegrityError:
            print(f'[red]You have already checked "{habit_name}" for today[/red]')
        habit_menu(habit)
    elif choice == f'Delete "{habit_name}"':
        print(f'[green]"{habit_name}"[/green]', end=" ")
        habit.delete_habit(db)  # updating database
        habits.remove(habit)  # updating global list
        print('[green]successfully deleted[/green]')
        see_habits()
    elif choice == f'See Current Streak of "{habit_name}"':
        habit.longest_streak, habit.current_streak = calculate_streak(habit)
        print(f'[green]The current streak of "{habit_name}" is {habit.current_streak}[/green]')
        habit_menu(habit)
    elif choice == f'See Longest Streak of "{habit_name}"':
        habit.longest_streak, habit.current_streak = calculate_streak(habit)
        print(f'[green]The longest streak of "{habit_name}" is {habit.longest_streak}[/green]')
        habit_menu(habit)
    elif choice == f'See description of "{habit_name}"':
        print(f'"{habit_name}" consists of "{habit.description}"')
        habit_menu(habit)
    else:
        see_habits()
    pass


main_menu()
