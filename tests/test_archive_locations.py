import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifecrossref import archive_locations


class TestSetArchiveLocationsTag(unittest.TestCase):
    "tests for set_archive_locations()"

    def test_set_archive_locations(self):
        "test adding archive_locations tag"
        parent = Element("root")
        archive_location_list = ["CLOCKSS"]
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b"<archive_locations>"
            b'<archive name="CLOCKSS" />'
            b"</archive_locations>"
            b"</root>"
        )
        # invoke
        archive_locations.set_archive_locations(parent, archive_location_list)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)
