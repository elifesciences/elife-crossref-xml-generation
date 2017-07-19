import unittest
import time
from elifecrossref import utils

class TestUtils(unittest.TestCase):

    def test_calculate_journal_volume(self):
        "for test coverage"
        self.assertEqual(utils.calculate_journal_volume(None, None), None)
        pub_date = time.strptime("2017-01-01", "%Y-%m-%d")
        self.assertEqual(utils.calculate_journal_volume(pub_date, 2017), "1")

if __name__ == '__main__':
    unittest.main()
