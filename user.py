import os
import json
from prettytable import PrettyTable
from getpass import getpass

FILE_PATH = "users_data.json"


def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')


class User:
    def __init__(self):
        """
        Initializes a new User object.

        Returns:
            None

        Method initializes the attributes of the User object.
        """
        self.username = ""
        self.password = None
        self.table = PrettyTable()
        self.table.field_names = ["Name of the command", "Command"]
        self.table.padding_width = 5
        self.table.align["Command"] = 'c'
        self.table.add_rows([
            ['Log in as a user', 1],
            ['Create a new user', 2],
            ['Delete an account', 3],
            ['Exit the program', 'e']
        ])

    def user_checker(self):
        """
        Displays the main menu and prompts the user for input.

        Returns:
            str or int: The command chosen by the user.

        Method displays the main menu, prompts the user for input,
        and returns the selected command.
        """
        while True:
            print(self.table)
            print()
            command = input("Enter command: ").strip().lower()

            if command in ['1', '2', '3']:
                command = int(command)
                return command
            elif command == 'e':
                # print()
                return 'exit'
            else:
                clear_screen()
                print("Invalid command")

    @staticmethod
    def is_valid_username(username):
        # Define rules for valid usernames here
        # For example, username must be at least 3 characters long and contain only alphanumeric characters
        return len(username) >= 3 and username.isalnum()

    @staticmethod
    def is_valid_password(password):
        # Define rules for valid passwords here
        # For example, password must be at least 6 characters long
        return len(password) >= 8 and " " not in password

    @staticmethod
    def load_existing_data():
        try:
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def store_data(self, username, password):
        """
        Store user data in the JSON file.

        Parameters:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Method stores the username and password of a new user in the JSON file.
        """
        # Load existing data
        existing_data = self.load_existing_data()

        # Update existing data with new user data
        existing_data[username] = {"password": password}

        # Write updated data to the file
        with open(FILE_PATH, "w") as file:
            json.dump(existing_data, file, indent=4)

    @staticmethod
    def username_exist(username):
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                return username in list(data.keys())
        except FileNotFoundError:
            return False

    def create_new_user(self):
        """
        Creates a new user account in the system.

        Returns:
            bool: True if the user account is successfully created, False otherwise.

        Method prompts the user to enter a new username and password,
        validates the input, and creates a new user account in the system.
        Returns True if the account is created successfully, otherwise False.
        """
        clear_screen()
        print("CREATE NEW USER\n")
        print("Type 'cancel' at any point to cancel operation of creating a new user\n")
        while True:
            username = input("Enter username: ").strip()
            if username.lower() == 'cancel':
                print("Operation canceled.")
                return False  # Return False to indicate cancellation
            if self.is_valid_username(username):
                if self.username_exist(username):
                    choice = input("This User already exists! "
                                   "Would you like to choose another username? (y/n)\n").strip().lower()
                    if choice == 'y':
                        clear_screen()
                    elif choice == 'n':
                        return False
                    else:
                        clear_screen()
                        print("Invalid command! Please register new user.")
                else:
                    self.username = username
                    break
            else:
                clear_screen()
                print("Invalid username.\n"
                      "Username must be at least 3 characters long and contain only alphanumeric characters.\n")

        while True:
            password = getpass("Enter password (at least 8 characters): ").strip()
            if password.lower() == 'cancel':
                print("Operation cancelled.")
                return False  # Return False to indicate cancellation
            password_confirmation = getpass("Confirm password: ").strip()
            if password_confirmation.lower() == 'cancel':
                print("Operation cancelled.")
                return False  # Return False to indicate cancellation
            if password == password_confirmation:
                if self.is_valid_password(password):
                    self.password = password
                    break
                else:
                    clear_screen()
                    print("Password must be at least 8 characters long.\n")
            else:
                clear_screen()
                print("Passwords do not match. Please try again.\n")

        self.store_data(self.username, self.password)
        print(f"User {self.username} successfully created!")
        return True

    def find_user(self):
        """
        Finds and validates the user in the system.

        Returns:
            bool: True if the user is found and validated, False otherwise.

        Method prompts the user to enter their username and password,
        validates the credentials against the system, and returns True if
        the user is found and validated, otherwise False.
        """
        clear_screen()
        print("LOG INTO USER ACCOUNT\n")
        username = input("Enter username: ").strip()
        password = getpass("Enter user password: ").strip()
        data = self.load_existing_data()
        if username in data.keys() and data[username]["password"] == password:
            clear_screen()
            print("YOU HAVE SUCCESSFULLY LOGGED INTO USER ACCOUNT\n")
            print(f"Username: {username}\n")
            self.username = username
            return True
        else:
            clear_screen()
            print("Unable to log into an account!".upper())
            print("Reason: wrong username or password.\n")
            input("Press to continue...")
            clear_screen()
            return False

    def delete_account(self):
        """
        Deletes the user account from the system.

        Returns:
            bool: True if the user account is successfully deleted, False otherwise.

        Method prompts the user to confirm the deletion of their account,
        deletes the account from the system, and returns True if the deletion
        is successful, otherwise False.
        """
        clear_screen()
        print("Delete an account\n".upper())
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        existing_data = self.load_existing_data()

        if username in existing_data and existing_data[username]["password"] == password:
            del existing_data[username]
            with open(FILE_PATH, "w") as file:
                json.dump(existing_data, file, indent=4)
            print(f"Account {username} deleted successfully!\n")
            input("Press to continue...")
        else:
            clear_screen()
            print("Account deletion failed".upper())
            print("Reason: invalid username or password.\n")
            choice = input("Do you want to try again? (y/n) ").strip().lower()
            if choice == 'y':
                self.delete_account()
