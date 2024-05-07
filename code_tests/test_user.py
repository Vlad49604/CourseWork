import unittest
from unittest.mock import patch, mock_open
from user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    @patch('builtins.input', side_effect=['1'])
    def test_user_checker_valid_input(self, mock_input):
        result = self.user.user_checker()
        self.assertEqual(result, 1)

    @patch('builtins.input', side_effect=['invalid', 'e'])
    def test_user_checker_invalid_input(self, mock_input):
        result = self.user.user_checker()
        self.assertEqual(result, 'exit')

    def test_is_valid_username(self):
        self.assertTrue(self.user.is_valid_username("test123"))
        self.assertTrue(self.user.is_valid_username("123"))
        self.assertFalse(self.user.is_valid_username("12 "))
        self.assertFalse(self.user.is_valid_username("test!@#"))

    def test_is_valid_password(self):
        self.assertTrue(self.user.is_valid_password("password123"))
        self.assertTrue(self.user.is_valid_password("securepassword"))
        self.assertFalse(self.user.is_valid_password("pass word"))
        self.assertFalse(self.user.is_valid_password("weak"))

    def test_username_exist(self):
        result = self.user.username_exist('existingUser')
        self.assertTrue(result)
        result = self.user.username_exist('nonExistingUser')
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
