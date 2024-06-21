import questionary
from habit import Habit
from db import get_db, get_habits
from analyse import strongest_weakest_habit
import sqlite3
from rich import print

# db = get_db('test.db')
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
            "See my Weakest Habit",
            "See my Strongest Habit",
            "Main Menu"
        ]
    ).ask()

    if choice == "See my Weakest Habit":
        weakest_habit = strongest_weakest_habit(habits)[1]
        print(f"Your weakest habit is {weakest_habit.name} with a longest streak of {weakest_habit.longest_streak}")
        main_menu()
    elif choice == "See my Strongest Habit":
        strongest_habit = strongest_weakest_habit(habits)[0]
        print(
            f'Your strongest habit is {strongest_habit.name} with a longest streak of {strongest_habit.longest_streak}')
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

    for habit in get_habits(db):
        if choice == habit.name.capitalize():
            habit.get_habit_data(db)
            habit_menu(habit)
            return

    main_menu()


def habit_menu(habit):
    choice = questionary.select(
        "What do you want to do?",
        choices=[
            f'Complete "{habit.name}"',
            f'Delete "{habit.name}"',
            f'See Current Streak of "{habit.name}"',
            f'See Longest Streak of "{habit.name}"',
            f'See description of "{habit.name}"',
            "Back to Habit List"
        ]
    ).ask()

    if choice == f'Complete "{habit.name}"':
        try:
            habit.add_event(db)
            print(f'[green]You successfully check in on {habit.check_dates[0]} for "{habit.name.capitalize()}" [/green]'
                  f'[green]which consists of "{habit.description}"[/green]')
        except sqlite3.IntegrityError:
            print(f'[red]You have already checked "{habit.name.capitalize()}" for today[/red]')
        habit_menu(habit)
    elif choice == f'Delete "{habit.name}"':
        print(f'[green]"{habit.name.capitalize()}"[/green]', end=" ")
        habit.delete_habit(db)  # updating database
        habits.remove(habit)  # updating global list
        print('[green]successfully deleted[/green]')
        see_habits()
    elif choice == f'See Current Streak of "{habit.name}"':
        habit.calculate_streak()
        print(f'[green]The current streak of "{habit.name.capitalize()}" is {habit.current_streak}[/green]')
        habit_menu(habit)
    elif choice == f'See Longest Streak of "{habit.name}"':
        habit.calculate_streak()
        print(f'[green]The longest streak of "{habit.name.capitalize()}" is {habit.longest_streak}[/green]')
        habit_menu(habit)
    elif choice == f'See description of "{habit.name}"':
        print(f'"{habit.name.capitalize()}" consists of "{habit.description}"')
        habit_menu(habit)
    else:
        see_habits()
    pass


main_menu()
