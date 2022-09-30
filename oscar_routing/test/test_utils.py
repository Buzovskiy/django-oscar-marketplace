import unittest
from ..utils import check_email_valid


class TestUtilsCase(unittest.TestCase):

    def test_check_email_valid(self):
        self.assertTrue(check_email_valid('example@gmail.com'))
        self.assertFalse(check_email_valid('example'))
        self.assertFalse(check_email_valid(''))
