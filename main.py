import questionary
from habit import Habit, get_habits
from db import get_db
from analyse import compute_weakest_habit, compute_strongest_habit
import sqlite3
from rich import print

# db = get_db('test.db')
db = get_db()


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

    habit = Habit(name=name, description=description, periodicity=period)

    try:
        habit.store(db)
        print(f'[blue]You added "{habit.name}" to your habits[/blue]')
    except sqlite3.IntegrityError:
        print(f'[red]Habit "{habit.name}" already in database, please retry[red]')

    main_menu()


def feedback():
    # habits = get_habits(db)
    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "See my Weakest Habit",
            "See my Strongest Habit",
            "Main Menu"
        ]
    ).ask()

    if choice == "See my Weakest Habit":
        #habit = compute_weakest_habit(db)
        habit = compute_weakest_habit(db, get_habits(db))
        print(f"Your weakest habit is {habit.name} with a longest streak of {habit.longest_streak}")
        main_menu()
    elif choice == "See my Strongest Habit":
        #habit = compute_strongest_habit(db)
        habit = compute_strongest_habit(db, get_habits(db))
        print(f"Your strongest habit is {habit.name} with a longest streak of {habit.longest_streak}")
        main_menu()
    else:
        main_menu()


def see_habits(type=None):
    if type is None:
        list_of_choices = ["Show daily habits", "Show weekly habits"] + [habit.name.capitalize() for habit in
                                                                         get_habits(db)] + ["Main Menu"]
    else:
        list_of_choices = [habit.name.capitalize() for habit in get_habits(db, type)] + ["Back"] + ["Main Menu"]
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
            "Back to Habit List"
        ]
    ).ask()

    if choice == "Complete the Habit":
        try:
            habit.add_event(db)
            habit.get_habit_data(db)
            print(f'[green]You successfully check in on {habit.check_dates[0]} for "{habit.name}" [/green]'
                  f'[green]which consists of "{habit.description}"[/green]')
        except sqlite3.IntegrityError:
            print("[red]You have already checked in for today[/red]")
        habit_menu(habit)
    elif choice == "Delete the Habit":
        print(f'{habit.name}', end=" ")
        habit.delete_habit(db)
        print('successfully deleted')
        see_habits()
    elif choice == f'See Current Streak of "{habit.name}"':
        habit.calculate_streak(db)
        print(f"The current streak of {habit.name} is {habit.current_streak}")
        habit_menu(habit)
    elif choice == f'See Longest Streak of "{habit.name}"':
        habit.calculate_streak(db)
        print(f"The longest streak of {habit.name} is {habit.longest_streak}")
        habit_menu(habit)
    else:
        see_habits()
    pass


main_menu()
