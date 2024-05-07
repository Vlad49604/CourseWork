import unittest
from unittest.mock import patch


class TestExpenseManager(unittest.TestCase):

    @patch('builtins.input', side_effect=['2024-05-01'])
    def test_get_date_valid_date(self, mock_input):
        expense_manager = ExpenseManager(None)  # Pass None as user since user is not used in get_date function
        result = expense_manager.get_date()
        self.assertEqual(result, '2024-05-01')

    @patch('builtins.input', side_effect=['2024/05/31', '2024-05-01'])
    def test_get_date_invalid_format_then_valid_date(self, mock_input):
        expense_manager = ExpenseManager(None)  # Pass None as user since user is not used in get_date function
        result = expense_manager.get_date()
        self.assertEqual(result, '2024-05-01')

    @patch('builtins.input', side_effect=['exit'])
    def test_get_date_exit(self, mock_input):
        expense_manager = ExpenseManager(None)  # Pass None as user since user is not used in get_date function
        result = expense_manager.get_date()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

# import unittest
# from unittest.mock import patch, call
# from expense_manager import ExpenseManager
#
# class TestExpenseManager(unittest.TestCase):
#     @patch('builtins.input', side_effect=['1', '50', 'y', 'n'])
#     @patch('builtins.print')
#     @patch('expense_manager.ExpenseManager.get_date', return_value='2024-05-01')
#     @patch('expense_manager.ExpenseManager.check_command', return_value=1)
#     @patch('expense_manager.ExpenseManager.logo_table_expenses')
#     @patch('expense_manager.ExpenseManager.enter_amount', return_value=50)
#     @patch('expense_manager.ExpenseManager.save_expense')
#     def test_add_expenses(self, mock_save_expense, mock_enter_amount, mock_logo_table_expenses, mock_check_command,
#                           mock_get_date, mock_print, mock_input):
#         expense_manager = ExpenseManager('test_user')
#         expense_manager.add_expenses()
#
#         # Assertions
#         mock_get_date.assert_called_once()
#         mock_logo_table_expenses.assert_called_once_with('01 May 2024')
#         mock_check_command.assert_called_once_with('1')
#         mock_enter_amount.assert_called_once()
#         mock_save_expense.assert_called_once_with('Food', 50,
#                                                   '2024-05-01')
