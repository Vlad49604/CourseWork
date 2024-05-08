import os
from user import User
from expense_tracker import ExpenseTracker


def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')


# Activates a user session for the given username.
def active_user(username):
    expense_tracker = ExpenseTracker(username)
    while True:
        if expense_tracker.run(True):
            break


clear_screen()

while True:
    user = User()
    command = user.user_checker()

    if command == 1:
        if user.find_user():
            active_user(user.username)
            clear_screen()
            print(f"You have log out from user account {user.username}!\n")
            input("Press to continue...")
            clear_screen()
    elif command == 'exit':
        break
    elif command == 3:
        result = user.delete_account()
        clear_screen()
        if result:
            print("User account has been deleted\n")
            input("Press to continue...")
            clear_screen()
    else:
        result = user.create_new_user()
        clear_screen()
        if result:
            print("New user has been created\n")
            input("Press to continue...")
            clear_screen()
