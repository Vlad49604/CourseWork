import os
import datetime as dt
from prettytable import PrettyTable, prettytable
from termcolor import colored
from dateutil import parser
import json


TODAY = dt.datetime.today().date()


def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')


class ExpenseManager:
    def __init__(self, user):
        self.user = user
        self.expenses_table = PrettyTable()
        self.expenses_table.hrules = prettytable.ALL
        self.expenses_table.field_names = ["Category", "Command"]
        self.expenses_table.padding_width = 2
        self.expenses_table.align["Command"] = 'c'
        self.expenses_table.align["Category"] = 'l'
        self.expenses_table.add_rows([
            ['Food (including groceries, dining out, and takeout)', 1],
            ['Housing (rent or mortgage payments, utilities, maintenance)', 2],
            ['Transportation (gasoline, public transit, vehicle maintenance)', 3],
            ['Health and wellness (healthcare expenses, gym memberships, medications)', 4],
            ['Entertainment (movies, concerts, streaming services)', 5],
            ['Shopping (clothing, electronics, personal care products)', 6],
            ['Travel (flights, hotels, vacation activities)', 7],
            ['Utilities (electricity, water, internet, phone)', 8],
            ['Education (tuition, books, supplies)', 9],
            ['Debt payments (credit card bills, loans)', 10],
            ['Insurance (health, auto, home)', 11],
            ['Personal care (haircuts, spa treatments, grooming products)', 12],
            ['Gifts and donations (birthday presents, charity donations)', 13],
            ['Household supplies (cleaning products, toiletries)', 14],
            ['Other Expenses', 15],
            ['Cancel operation', 'cancel']
        ])

        self.expenses = [
            'Food',
            'Housing',
            'Transportation',
            'Health and wellness',
            'Entertainment',
            'Shopping',
            'Travel',
            'Utilities',
            'Education',
            'Debt payments',
            'Insurance',
            'Personal care',
            'Gifts and donations',
            'Household supplies',
            'Other Expenses'
        ]

    @staticmethod
    def get_date():
        while True:
            date_input = input("Enter date you want to add expenses to (e.g., '2024-05-31'): ")
            if date_input.lower().strip() == "exit":
                break
            try:
                date_obj = parser.parse(date_input).date()
                if date_obj > TODAY:
                    clear_screen()
                    print(f"Date {date_obj} is in the future. Please enter past or present date.")
                elif (TODAY - date_obj).days > 365:
                    clear_screen()
                    print(f"Date {date_obj} was more than a year ago. Please enter a recent date.")
                else:
                    return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                clear_screen()
                print("Invalid date format!".upper())
                print("Please enter a valid date in format YYYY-MM-DD.")
                print("If you want to cancel operation, enter 'exit'\n")

    @staticmethod
    def format_date(date):
        date_obj = dt.datetime.strptime(date, "%Y-%m-%d")
        return date_obj.strftime("%d %B %Y")

    @staticmethod
    def enter_amount():
        while True:
            try:
                amount = float(input("Enter amount of money you've spent: $").strip().lower())
            except ValueError:
                print("You should enter a number! (e.g - 8.50)\n")
                continue
            if amount < 0:
                print("Money you've spent should be a positive number!\n")
                continue
            return amount

    @staticmethod
    def check_command(comm):
        try:
            comm = int(comm)
        except ValueError:
            print("Command is not valid. Please enter a number from 1 to 15 or 'cancel' to cancel operation")
            return False
        if 1 <= comm <= 15:
            return comm
        print("There is only 15 commands. Enter a number from 1 to 15 or 'cancel' to cancel operation")
        return False

    def initialize_file_with_format(self):
        with open(f'users/{self.user}.json', 'w') as json_file:
            data = {
                'date': {},
                'month': {}
            }
            json.dump(data, json_file, indent=4)

    def check_emptiness(self):
        try:
            with open(f'users/{self.user}.json', 'r') as json_file:
                try:
                    loaded_data = json.load(json_file)
                    if 'date' in loaded_data and 'month' in loaded_data \
                            and isinstance(loaded_data['date'], dict) \
                            and isinstance(loaded_data['month'], dict):
                        pass  # Data is in the desired format
                    else:
                        self.initialize_file_with_format()  # Reinitialize the file
                except json.JSONDecodeError:
                    self.initialize_file_with_format()  # File is empty or not valid JSON
        except FileNotFoundError:
            self.initialize_file_with_format()  # File doesn't exist, create with format

    def logo_table_expenses(self, date):
        clear_screen()
        print(self.expenses_table)
        print(f"SELECTED DATE - {date}")
        logo = colored(self.user, attrs={"bold"})
        print(f"Username: {logo}\n")

    def save_expense(self, expense, amount, date):
        # Read existing data from the JSON file
        try:
            with open(f"users/{self.user}.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Extract month and year from the date
        date_obj = dt.datetime.strptime(date, "%Y-%m-%d")
        month_year = date_obj.strftime("%B %Y")

        # Update data for the specific date
        if 'date' not in data:
            data['date'] = {}
        if date in data['date']:
            # If expense already exists for the date, update the amount
            if expense in data['date'][date]:
                data['date'][date][expense] += amount
            else:
                # If expense doesn't exist for the date, add it
                data['date'][date][expense] = amount
        else:
            # If there is no existing data for the date, create a new entry
            data['date'][date] = {expense: amount}

        # Update data for the specific month
        if 'month' not in data:
            data['month'] = {}

        if month_year in data['month']:
            if 'expenses' in data['month'][month_year] and expense in data['month'][month_year]['expenses']:
                # If the expense exists for the month, update its amount
                data['month'][month_year]['expenses'][expense] += amount
            else:
                # If the expense doesn't exist for the month, create a new entry
                data['month'][month_year]['expenses'][expense] = amount
        else:
            # If month doesn't exist, create a new entry
            data['month'][month_year] = {'limit': None, 'expenses': {expense: amount}}

            # Write the updated data back to the JSON file
        with open(f"users/{self.user}.json", "w") as file:
            json.dump(data, file, indent=4)

    def add_expenses(self, date=""):
        if date == "":
            date = self.get_date()
        if date is None:
            clear_screen()
            print("You have successfully canceled operation!\n")
            input("Press to continue...")
            return
        f_date = self.format_date(date)
        continue_adding = True
        while continue_adding:
            self.logo_table_expenses(f_date)
            correct_input = False
            while not correct_input:
                exp_choice = input("Enter which expense you want to add: ").lower().strip()
                if exp_choice == 'cancel':
                    return
                correct_input = self.check_command(exp_choice)
            clear_screen()
            print(f"You have selected {self.expenses[correct_input - 1]} expense.\n")
            amount = self.enter_amount()
            clear_screen()
            choice = input(f"Do you want to add {self.expenses[correct_input - 1]} "
                           f"expense with ${amount} of money spent at {f_date}? (y/n) ").lower().strip()
            while choice != 'y' and choice != 'n':
                print("You should enter only 'y' to save expense or 'n' to cancel it!")
                choice = input(f"Do you want to add {self.expenses[correct_input - 1]} "
                               f"expense with ${amount} of money spent at {f_date}?").lower().strip()
            if choice == 'n':
                print("Expense wasn't saved to your list!\n")
                continue
            self.save_expense(self.expenses[correct_input - 1], amount, date)
            print()
            choice = input("Do you want to add another expense? (y/n) ").strip().lower()
            while choice != 'y' and choice != 'n':
                print("Invalid input! Enter 'y' if you want to add another expense and 'n' if don't.")
                choice = input("Enter your choice: ").strip().lower()
            if choice == 'n':
                continue_adding = False
                continue
            else:
                print()

    def set_limit(self, select_month_func):
        # Load data from JSON file
        with open(f"users/{self.user}.json", "r") as file:
            data = json.load(file)

        clear_screen()

        # Get the current month
        selected_month = select_month_func("set a limit for")

        clear_screen()

        while True:
            clear_screen()

            if 'limit' in data['month'].get(selected_month, {}):
                print(f"The limit for {selected_month} is ${data['month'][selected_month]['limit']}\n")

            limit_input = input(f"Enter the new limit for {selected_month} (type 'cancel' to cancel): ")

            if limit_input.lower() == 'cancel':
                print("Operation cancelled.")
                return

            try:
                new_limit = float(limit_input)
            except ValueError:
                clear_screen()
                print("Invalid input! Please enter a number.")
                input("Press to continue...")
                continue  # Restart the loop to prompt the user again

            # Add or update the limit for the selected month
            data['month'].setdefault(selected_month, {})['limit'] = new_limit

            # Check if there are expenses for the selected month
            if 'expenses' not in data['month'][selected_month]:
                data['month'][selected_month]['expenses'] = {}

            # Write the updated data back to the JSON file
            with open(f"users/{self.user}.json", "w") as file:
                json.dump(data, file, indent=4)
            break  # Exit the loop if input is valid
