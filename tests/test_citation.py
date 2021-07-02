import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Citation
from elifecrossref import citation


class TestSetUnstructuredCitation(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_unstructured_citation_no_face_markup(self):
        """unstructured citation example with no face markup"""
        article_title = (
            "PhD thesis: Submicroscopic <italic>Plasmodium falciparum</italic> gametocytaemia "
            + "and the contribution to malaria transmission"
        )
        expected = (
            "<citation><unstructured_citation>PhD thesis: Submicroscopic "
            + "Plasmodium falciparum gametocytaemia and the contribution to "
            + "malaria transmission.</unstructured_citation></citation>"
        )
        citation_object = Citation()
        citation_object.article_title = article_title
        citation_object.publication_type = "patent"
        parent = Element("citation")
        face_markup = False
        citation_element = citation.set_unstructured_citation(
            parent, citation_object, face_markup
        )
        rough_string = ElementTree.tostring(citation_element).decode("utf-8")
        self.assertEqual(rough_string, expected)

    def test_set_unstructured_citation_face_markup(self):
        """unstructured citation example which does include face markup"""
        article_title = (
            "PhD thesis: Submicroscopic <italic>Plasmodium falciparum</italic> gametocytaemia "
            + "and the contribution to malaria transmission"
        )
        expected = (
            "<citation><unstructured_citation>PhD thesis: Submicroscopic "
            + "<i>Plasmodium falciparum</i> gametocytaemia and the contribution to "
            + "malaria transmission.</unstructured_citation></citation>"
        )
        citation_object = Citation()
        citation_object.article_title = article_title
        citation_object.publication_type = "patent"
        parent = Element("citation")
        face_markup = True
        citation_element = citation.set_unstructured_citation(
            parent, citation_object, face_markup
        )
        rough_string = ElementTree.tostring(citation_element).decode("utf-8")
        self.assertEqual(rough_string, expected)


class TestCitationPublisher(unittest.TestCase):
    def setUp(self):
        self.publisher_loc = "Nijmegen, The Netherlands"
        self.publisher_name = "Radboud University Nijmegen Medical Centre"

    def test_citation_publisher_none(self):
        """no publisher name concatenation"""
        citation_object = Citation()
        self.assertIsNone(citation.citation_publisher(citation_object))

    def test_citation_publisher_loc_only(self):
        """no publisher name concatenation"""
        citation_object = Citation()
        citation_object.publisher_loc = self.publisher_loc
        self.assertEqual(
            citation.citation_publisher(citation_object), "Nijmegen, The Netherlands"
        )

    def test_citation_publisher_name_only(self):
        """no publisher name concatenation"""
        citation_object = Citation()
        citation_object.publisher_name = self.publisher_name
        self.assertEqual(
            citation.citation_publisher(citation_object),
            "Radboud University Nijmegen Medical Centre",
        )

    def test_citation_publisher_all(self):
        """no publisher name concatenation"""
        citation_object = Citation()
        citation_object.publisher_loc = self.publisher_loc
        citation_object.publisher_name = self.publisher_name
        self.assertEqual(
            citation.citation_publisher(citation_object),
            "Nijmegen, The Netherlands: Radboud University Nijmegen Medical Centre",
        )


if __name__ == "__main__":
    unittest.main()
