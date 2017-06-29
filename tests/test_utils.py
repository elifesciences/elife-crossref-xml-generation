import unittest
from elifecrossref import utils

class TestUtils(unittest.TestCase):

    def test_elife_journal_volume(self):
        "for test coverage"
        self.assertEqual(utils.elife_journal_volume(None), None)

if __name__ == '__main__':
    unittest.main()
