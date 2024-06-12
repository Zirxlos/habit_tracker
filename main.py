import questionary
from habit import Habit

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
    print(
        f'Your habit is {habit.name.lower()}, which consists of {habit.description.lower()} '
        f'that you will do every {habit.periodicity} day')

    main_menu()


def feedback():
    pass

def see_habits():
    habits = [
        "exercise",
        "cooking",
        "going to the cinema",
        "seeing friends"
    ]
    choice = questionary.select(
        "Please chose a habit:",
        choices=habits
    ).ask()

    for habit in habits:
        if choice == habit:
            habit_menu(habit)
            return

    main_menu()

def habit_menu(habit):
    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "Complete the Habit",
            "Delete the Habit",
            "See Current Streak of the Habit",
            "See Longest Streak of the Habit",
            "Exit"
        ]
    ).ask()

    pass


main_menu()