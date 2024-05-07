import os
import json
import datetime as dt
from prettytable import PrettyTable
from dateutil import parser
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

TODAY = dt.datetime.today().date()
MY_EMAIL = "vlad.lozynsky.test@gmail.com"
APP_PASSWORD = "xjoxedmjphlgxsgc"


def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')


class ExpensesReport:

    def __init__(self, user):
        self.user = user
        self.report_table = PrettyTable()
        self.report_table.field_names = ["Name of the command", "Command"]
        self.report_table.padding_width = 5
        self.report_table.align["Command"] = 'c'
        self.report_table.add_rows([
            ["Send this month report", 1],
            ["Send selected month report", 2],
            ["Sent days report", 3],
            ["Cancel report sending", 'e']
        ])

    @staticmethod
    def select_another_month(message):
        clear_screen()
        while True:
            user_input = input(f"Enter the month you want to {message} (e.g., 'May 2024'): ").strip()
            try:
                formatted_month = dt.datetime.strptime(user_input, "%B %Y").strftime("%B %Y")
                return formatted_month
            except ValueError:
                clear_screen()
                print(
                    "Invalid input! "
                    "Please enter the month and year in the format 'Month Year' (e.g., 'May 2024')\n")

    def select_month(self, message):
        current_month = dt.datetime.now().strftime("%B %Y")
        change_month = input(
            f"Do you want to {message} {current_month}? (y/n): ").lower().strip()
        if change_month == 'y':
            return current_month
        elif change_month == 'n':
            return self.select_another_month(message)
        else:
            clear_screen()
            print(f"Invalid data! Please enter 'y' or 'n'\n")
            return self.select_month(message)

    @staticmethod
    def get_date_range(prompt):
        while True:
            date_input = input(prompt)
            if date_input.lower().strip() == "cancel":
                return None
            try:
                date_obj = parser.parse(date_input).date()
                if date_obj > TODAY:
                    clear_screen()
                    print(f"Date {date_obj} is in the future. Please enter past or present date.")
                    continue
                elif (TODAY - date_obj).days > 365:
                    clear_screen()
                    print(f"Date {date_obj} was more than a year ago. Please enter a recent date.")
                    continue
                else:
                    return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                clear_screen()
                print("Invalid date format!".upper())
                print("Please enter a valid date in format YYYY-MM-DD.")
                print("If you want to cancel operation, enter 'cancel'\n")

    @staticmethod
    def get_user_address():
        while True:
            address = input("Enter your address: ")
            if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', address):
                return address
            else:
                print("Invalid address format. Please try again.")

    @staticmethod
    def get_month_report_info(month_data):
        report_info = []

        total_amount = 0
        num_expenses = len(month_data.get('expenses', {}))

        if num_expenses >= 3:
            table = PrettyTable(["Category", "Price"])

            # Adjust padding width for consistent spacing
            table.padding_width = 2

            # Set alignment for columns
            table.align["Price"] = "r"  # Right align Price column
            table.align["Category"] = 'l'  # Left align Category column

            for expense, amount in month_data['expenses'].items():
                table.add_row([expense, f"${amount:.2f}"])
                total_amount += amount

            table.add_row(["-" * 30, "-" * 10])  # Adjust as needed
            table.add_row(["Total", f"${total_amount:.2f}"])

            report_info.append(table)
        else:
            expenses_info = "\n".join([f"{expense}: ${amount:.2f}"
                                       for expense, amount in month_data.get('expenses', {}).items()])
            report_info.append("Expenses:\n" + expenses_info)

            total_amount = sum(month_data.get('expenses', {}).values())
            if num_expenses > 1:
                report_info.append(f"Total: ${total_amount:.2f}")

        if 'limit' in month_data and isinstance(month_data['limit'], float):
            limit = month_data['limit']
            report_info.append(f"Limit: ${limit:.2f}")
            amount_available = limit - total_amount
            report_info.append(f"Amount available: ${amount_available:.2f}")
        else:
            report_info.append("No limit set for this month.")

        return "\n\n".join([str(table) for table in report_info])

    @staticmethod
    def get_month_report_info_smtp(month_data):
        report_info = []

        total_amount = 0
        num_expenses = len(month_data.get('expenses', {}))

        for expense, amount in month_data.get('expenses', {}).items():
            report_info.append(f"{expense}: ${amount:.2f}")
            total_amount += amount

        if num_expenses > 0:
            report_info.append("-" * 30)  # Add separator line

        report_info.append(f"Total: ${total_amount:.2f}")

        if 'limit' in month_data and isinstance(month_data['limit'], float):
            limit = month_data['limit']
            report_info.append(f"Limit: ${limit:.2f}")
            amount_available = limit - total_amount
            report_info.append(f"Amount available: ${amount_available:.2f}")
        else:
            report_info.append("No limit set for this month.")

        return "\n".join(report_info)

    def short_month_data(self):
        # Load data from JSON file
        with open(f"users/{self.user}.json", "r") as file:
            data = json.load(file)

        clear_screen()

        selected_month = self.select_month("get information about")

        clear_screen()

        # Extract data for the current month
        selected_month_data = data['month'].get(selected_month)

        if selected_month_data is None:
            print(f"No data found for {selected_month}.\n")
            input("Press to continue...")
            return

        # Get the limit for the current month, if set
        limit = selected_month_data.get('limit')

        # Calculate total amount spent
        expenses_only = selected_month_data.get('expenses', {})
        total_spent = sum(expenses_only.values())

        # Print results
        print(f"Total amount spent in {selected_month}: ${total_spent:.2f}")
        if limit and isinstance(limit, float):
            print(f"Limit set for {selected_month}: ${limit:.2f}")
            amount_available = limit - total_spent
            print(f"Amount available: ${amount_available:.2f}")
        else:
            print("No limit set for this month.")

        input("Press to continue...")

    def get_month_data(self, s_month):
        # Load data from JSON file
        with open(f"users/{self.user}.json", "r") as file:
            data = json.load(file)

        # Extract data for the selected month
        return data['month'].get(s_month)

    def display_month_data(self):
        selected_month = self.select_month("display data for")

        month_data = self.get_month_data(selected_month)

        # Check if data exists for the selected month
        if month_data:
            clear_screen()
            print(f"Month: {selected_month}")

            report_info = self.get_month_report_info(month_data)
            print(report_info)
        else:
            clear_screen()
            print(f"No data found for {selected_month}.\n")

        input("Press to continue...")

    def send_month_report(self, selected_month):
        user_address = self.get_user_address()
        report_info = self.get_month_report_info_smtp(
            self.get_month_data(selected_month))  # assuming month_data is available here
        subject = "Month spending report"

        msg = MIMEMultipart()
        msg['From'] = MY_EMAIL
        msg['To'] = user_address
        msg['Subject'] = subject

        body = f"Month: {selected_month}\n\n{report_info}"

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PASSWORD)
            connection.send_message(msg)

    @staticmethod
    def calculate_category_totals(data, start_date, end_date):
        category_totals = {}
        current_date = end_date
        while current_date >= start_date:
            current_date_str = current_date.strftime("%Y-%m-%d")
            if current_date_str in data['date']:
                expenses_for_date = data['date'][current_date_str]
                for category, amount in expenses_for_date.items():
                    category_totals[category] = category_totals.get(category, 0) + amount
            current_date -= dt.timedelta(days=1)
        return category_totals

    def send_days_report(self):
        with open(f"users/{self.user}.json", "r") as file:
            data = json.load(file)

        user_email = self.get_user_address()
        start_date = self.get_date_range("Enter start date for the expense report (e.g., '2024-04-01'): ")
        end_date = self.get_date_range("Enter end date for the expense report (e.g., '2024-04-01'): ")

        if start_date is None or end_date is None:
            print("You have canceled action!\n")
            input("Press to continue...")
            return

        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

        category_totals = self.calculate_category_totals(data, start_date, end_date)
        total_all_expenses = sum(category_totals.values())

        # Construct email body
        body = ""
        start_date_str = start_date.strftime("%d %B %Y")
        end_date_str = end_date.strftime("%d %B %Y")

        body += f"Expenses report for time period from {start_date_str} to {end_date_str}\n\n"
        current_date = end_date
        while current_date >= start_date:
            current_date_str = current_date.strftime("%Y-%m-%d")
            if current_date_str in data['date']:
                expenses_for_date = data['date'][current_date_str]
                if current_date_str not in body:
                    body += f"----------------------------------------------------------------------------------\n"
                    body += f"{current_date_str} expenses:\n"
                for category, amount in expenses_for_date.items():
                    body += f"  {category}: ${amount:.2f}\n"
            current_date -= dt.timedelta(days=1)

        body += "----------------------------------------------------------------------------------\n"
        body += "\nTotal expenses for each category:\n"
        for category, total in category_totals.items():
            body += f"  {category}: ${total:.2f}\n"

        body += "----------------------------------------------------------------------------------\n"
        body += f"\nTotal for all expenses: ${total_all_expenses:.2f}\n"

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = "your_email@gmail.com"  # Your email address
        msg['To'] = user_email
        msg['Subject'] = "Expense Report"
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PASSWORD)
            connection.send_message(msg)

    def days_report(self):
        with open(f"users/{self.user}.json", "r") as file:
            data = json.load(file)

        clear_screen()

        start_date = self.get_date_range("Enter start date for the expense report (e.g., '2024-04-01'): ")

        if start_date is None:
            print("You have canceled action!\n")
            input("Press to continue...")
            return

        end_date = self.get_date_range("Enter end date for the expense report (e.g., '2024-04-01'): ")

        if end_date is None:
            print("You have canceled action!\n")
            input("Press to continue...")
            return

        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

        category_totals = self.calculate_category_totals(data, start_date, end_date)

        current_date = end_date

        start_date_str = start_date.strftime("%d %B %Y")
        end_date_str = end_date.strftime("%d %B %Y")

        clear_screen()
        print(f"Expenses report for time period from {start_date_str} to {end_date_str}")

        while current_date >= start_date:
            current_date_str = current_date.strftime("%Y-%m-%d")
            if current_date_str in data['date']:
                expenses_for_date = data['date'][current_date_str]
                print()
                print("----------------------------------------------------------------------------------")
                print(f"{current_date.strftime('%d %B %Y')} expenses:")
                for category, amount in expenses_for_date.items():
                    print(f"  {category}: ${amount:.2f}")
            current_date -= dt.timedelta(days=1)

        print("----------------------------------------------------------------------------------")
        print("\nTotal expenses for each category:")
        for category, total in category_totals.items():
            print(f"  {category}: ${total:.2f}")

        total_all_expenses = sum(category_totals.values())
        print(f"\nTotal for all expenses: ${total_all_expenses:.2f}")

        print()
        input("Press to continue...")

    def send_mail_report(self):
        clear_screen()
        while True:
            print(self.report_table)
            print()
            choice = input("Enter command: ")
            match choice:
                case '1':
                    self.send_month_report(dt.datetime.now().strftime("%B %Y"))
                    return
                case '2':
                    selected_month = self.select_another_month("get information about")
                    self.send_month_report(selected_month)
                    return
                case '3':
                    self.send_days_report()
                    return
                case 'e':
                    return
                case _:
                    clear_screen()
                    print("Invalid input.\n")
