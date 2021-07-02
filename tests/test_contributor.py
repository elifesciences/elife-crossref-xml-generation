import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Contributor
from elifecrossref import contributor


class TestSetPersonName(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_person_name(self):
        """all person name fields"""
        contributor_object = Contributor(None, "Aardvark", "Adam")
        contributor_object.suffix = "Jr."
        contributor_role = "author"
        sequence = "first"
        parent_tag = Element("person_name")
        expected = (
            '<person_name contributor_role="author" sequence="first">'
            "<given_name>Adam</given_name>"
            "<surname>Aardvark</surname><suffix>Jr.</suffix></person_name>"
        )
        person_name_element = contributor.set_person_name(
            parent_tag, contributor_object, contributor_role, sequence
        )
        rough_string = ElementTree.tostring(person_name_element).decode("utf-8")
        self.assertEqual(rough_string, expected)

    def test_set_person_name_no_given_name(self):
        """all person name fields"""
        contributor_object = Contributor(None, "Aardvark", "")
        contributor_role = "author"
        sequence = "first"
        parent_tag = Element("person_name")
        expected = (
            '<person_name contributor_role="author" sequence="first">'
            "<surname>Aardvark</surname></person_name>"
        )
        person_name_element = contributor.set_person_name(
            parent_tag, contributor_object, contributor_role, sequence
        )
        rough_string = ElementTree.tostring(person_name_element).decode("utf-8")
        self.assertEqual(rough_string, expected)


if __name__ == "__main__":
    unittest.main()
