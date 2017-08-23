import unittest
import time
from elifecrossref import utils
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

class TestUtils(unittest.TestCase):

    def test_calculate_journal_volume(self):
        "for test coverage"
        self.assertEqual(utils.calculate_journal_volume(None, None), None)
        pub_date = time.strptime("2017-01-01", "%Y-%m-%d")
        self.assertEqual(utils.calculate_journal_volume(pub_date, 2017), "1")

    def test_get_last_commit_to_master(self):
        self.assertIsNotNone(utils.get_last_commit_to_master())

    def test_append_minidom_xml_to_elementtree_xml(self):
        "test coverage of an edge case"
        parent = Element('root')
        tag = SubElement(parent, 'i')
        tag.text = "Text"
        tag.tail = " and tail."
        attributes = ["class"]
        # Add a first example
        xml = '<span><i>and</i> some <i>XML</i>.</span>'
        reparsed = minidom.parseString(xml.encode('utf-8'))
        parent = utils.append_minidom_xml_to_elementtree_xml(parent, reparsed)
        # Add another example to test more lines of code
        xml = '<span class="span"> <i>more</i> text</span>'
        reparsed = minidom.parseString(xml.encode('utf-8'))
        parent = utils.append_minidom_xml_to_elementtree_xml(parent, reparsed, False, attributes)
        # Generate output and compare it
        rough_string = ElementTree.tostring(parent)
        self.assertEqual(rough_string, '<root><i>Text</i> and tail.<span><i>and</i> some <i>XML</i>.</span><span class="span"> <i>more</i> text</span></root>')


if __name__ == '__main__':
    unittest.main()
