import unittest
from elifecrossref import utils


class TestUtils(unittest.TestCase):
    def test_allowed_tags(self):
        self.assertIsNotNone(utils.allowed_tags(), "allowed_tags not returned")

    def test_clean_string(self):
        self.assertEqual(utils.clean_string(None), None)
        self.assertEqual(utils.clean_string("-normal_"), "-normal_")
        self.assertEqual(utils.clean_string("/abnormal."), "abnormal")
