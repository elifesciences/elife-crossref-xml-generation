import unittest
from elifecrossref import dataset


class TestDataset(unittest.TestCase):
    def test_choose_dataset_identifier_none(self):
        """test when an object has no attributes"""
        self.assertIsNone(dataset.choose_dataset_identifier(None))


if __name__ == "__main__":
    unittest.main()
