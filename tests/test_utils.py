import unittest
from elifecrossref import utils

class TestUtils(unittest.TestCase):

    def test_allowed_tags(self):
        self.assertIsNotNone(utils.allowed_tags(), 'allowed_tags not returned')

if __name__ == '__main__':
    unittest.main()
