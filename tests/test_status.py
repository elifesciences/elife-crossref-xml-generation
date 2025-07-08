import unittest
import time
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifecrossref import status


class TestSetStatusTag(unittest.TestCase):
    "tests for set_status_tag()"

    def test_set_status_tag(self):
        "test adding status tag with a description tag"
        parent = Element("root")
        status_type = "withdrawn"
        status_date = time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S")
        description = "This article is retracted."
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<status date="2018-01-12" type="withdrawn">'
            b"<description>This article is retracted.</description>"
            b"</status>"
            b"</root>"
        )
        # invoke
        status.set_status_tag(parent, status_type, status_date, description)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)
