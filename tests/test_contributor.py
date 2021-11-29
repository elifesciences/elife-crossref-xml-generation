import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Affiliation, Contributor
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


class TestSetAffiliations(unittest.TestCase):
    def test_set_affiliations(self):
        parent_tag = Element("person_name")
        contributor_object = Contributor(None, "Aardvark", "")
        aff_object = Affiliation()
        aff_object.text = "Text"
        aff_object.department = "Department"
        aff_object.institution = "Institution"
        aff_object.city = "City"
        aff_object.country = "Country"
        aff_object.ror = "https://ror.org/example"
        contributor_object.set_affiliation(aff_object)
        expected = (
            "<person_name>"
            "<affiliations>"
            "<institution>"
            "<institution_name>Department, Institution</institution_name>"
            '<institution_id type="ror">https://ror.org/example</institution_id>'
            "<institution_place>City, Country</institution_place>"
            "</institution>"
            "</affiliations>"
            "</person_name>"
        )
        contributor.set_affiliations(parent_tag, contributor_object)
        rough_string = ElementTree.tostring(parent_tag).decode("utf-8")
        self.assertEqual(rough_string, expected)


class TestAffiliationNamePlace(unittest.TestCase):
    def test_affiliation_name_place_all(self):
        aff_object = Affiliation()
        aff_object.text = "Text"
        aff_object.department = "Department"
        aff_object.institution = "Institution"
        aff_object.city = "City"
        aff_object.country = "Country"
        expected_text_name = "Department, Institution"
        expected_text_place = "City, Country"
        text_name, text_place = contributor.affiliation_name_place(aff_object)
        self.assertEqual(text_name, expected_text_name)
        self.assertEqual(text_place, expected_text_place)

    def test_affiliation_name_place_text_only(self):
        aff_object = Affiliation()
        aff_object.text = "Text"
        expected_text_name = "Text"
        expected_text_place = ""
        text_name, text_place = contributor.affiliation_name_place(aff_object)
        self.assertEqual(text_name, expected_text_name)
        self.assertEqual(text_place, expected_text_place)

    def test_affiliation_name_place_place_only(self):
        aff_object = Affiliation()
        aff_object.city = "City"
        aff_object.country = "Country"
        expected_text_name = "City, Country"
        expected_text_place = ""
        text_name, text_place = contributor.affiliation_name_place(aff_object)
        self.assertEqual(text_name, expected_text_name)
        self.assertEqual(text_place, expected_text_place)


if __name__ == "__main__":
    unittest.main()
