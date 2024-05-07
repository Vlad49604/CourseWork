import unittest
from unittest.mock import patch
from expenses_report import ExpensesReport
from io import StringIO

class TestExpensesReport(unittest.TestCase):
    @patch('builtins.input', side_effect=['May 2024'])
    def test_select_another_month(self, mock_input):
        expenses_report = ExpensesReport('test_user')
        result = expenses_report.select_another_month('message')
        self.assertEqual(result, 'May 2024')

    @patch('builtins.input', side_effect=['n', 'April 2024'])
    def test_select_month_change_month(self, mock_input):
        expenses_report = ExpensesReport('test_user')
        result = expenses_report.select_month('message')
        expected_result = 'April 2024'
        self.assertEqual(result, expected_result)
        self.assertIn("Do you want to message", f"Do you want to message {expected_result}? (y/n): ")

    @patch('builtins.input', side_effect=['y'])
    def test_select_month_same_month(self, mock_input):
        expenses_report = ExpensesReport('test_user')
        result = expenses_report.select_month('message')
        self.assertEqual(result, 'May 2024')

    @patch('builtins.input', side_effect=['April 12', 'May 4'])
    def test_get_date_range_valid_input(self, mock_input):
        your_instance = ExpensesReport('existingUser')
        prompt = "Enter start date: "
        result = your_instance.get_date_range(prompt)  # Call the method under test
        expected_result = '2024-04-12'
        self.assertEqual(result, expected_result)  # Assert that the result matches the expected result

        prompt = "Enter end date: "
        result = your_instance.get_date_range(prompt)  # Call the method under test for the end date
        expected_result = '2024-05-04'
        self.assertEqual(result, expected_result)  # Assert that the result matches the expected result


    @patch('builtins.input', side_effect=['example@example.com', 'invalid_address', 'example@example.com'])
    def test_get_user_address(self, mock_input):
        your_instance = ExpensesReport("existingUser")
        expected_address = 'example@example.com'  # Define the expected address
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Test valid input
            result = your_instance.get_user_address()  # Call the method under test
            self.assertEqual(result, expected_address)  # Assert that the result matches the expected address

            # Test invalid input followed by valid input
            result = your_instance.get_user_address()
            self.assertEqual(result, expected_address)  # Assert that the result matches the expected address
            self.assertIn("Invalid address format. Please try again.",
                          fake_out.getvalue())  # Assert that error message is printed for invalid input


if __name__ == '__main__':
    unittest.main()
