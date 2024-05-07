from prettytable import PrettyTable
import os
import datetime as dt
from expenses_report import ExpensesReport
from expense_manager import ExpenseManager

TODAY = dt.datetime.today().date()


def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')


class ExpenseTracker:
    def __init__(self, user):
        self.user = user
        self.expense_report = ExpensesReport(self.user)
        self.expense_manager = ExpenseManager(self.user)
        self.user_table = PrettyTable()
        self.user_table.field_names = ["Name of the command", "Command"]
        self.user_table.padding_width = 5
        self.user_table.align["Command"] = 'c'
        self.user_table.add_rows([
            ['Add today\'s expenses', 1],
            ['Add expenses for selected day', 2],
            ['Set month limit', 3],
            ['Look for month short data', 4],
            ['Display month data', 5],
            ['Get days report', 6],
            ['Send a mail report', 7],
            ['Log out from account', 'e']
        ])

    def run(self, clear=False):
        self.expense_manager.check_emptiness()
        if clear:
            clear_screen()
        print(self.user_table)
        print()
        choice = input("Enter command: ")
        match choice:
            case '1':
                self.expense_manager.add_expenses(str(TODAY))
            case '2':
                self.expense_manager.add_expenses()
            case '3':
                self.expense_manager.set_limit(self.expense_report.select_month)
            case '4':
                self.expense_report.short_month_data()
            case '5':
                self.expense_report.display_month_data()
            case '6':
                self.expense_report.days_report()
            case '7':
                self.expense_report.send_mail_report()
            case 'e':
                return True
            case _:
                clear_screen()
                print("Invalid input.\n".upper())
                input("Press to continue... ")
