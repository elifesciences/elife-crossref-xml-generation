import unittest
import time
from elifecrossref import dates


class TestIsoDateString(unittest.TestCase):

    def test_iso_date_string(self):
        date_string = '2020-06-03'
        pub_date = time.strptime(date_string, '%Y-%m-%d')
        self.assertEqual(dates.iso_date_string(pub_date), date_string)

    def test_iso_date_string_none(self):
        self.assertIsNone(dates.iso_date_string(None))
