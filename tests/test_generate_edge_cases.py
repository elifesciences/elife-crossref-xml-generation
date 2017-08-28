import unittest
import time
import os
import re
from elifecrossref import generate
from elifecrossref.conf import config, parse_raw_config
from elifearticle.article import Article, Component, Citation
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

class TestGenerateComponentList(unittest.TestCase):

    def setUp(self):
        pass

    def test_component_subtitle_no_face_markup(self):
        "build an article object and component, generate Crossref XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        component = Component()
        component.title = "A component"
        component.subtitle = "A <sc>STRANGE</sc> <italic>subtitle</italic>, and this tag is <not_allowed>!</not_allowed>"
        expected_subtitle = "A STRANGE subtitle, and this tag is &lt;not_allowed&gt;!&lt;/not_allowed&gt;"
        article.component_list = [component]
        # generate the crossrefXML
        cXML = generate.build_crossref_xml([article])
        crossref_xml_string = cXML.output_XML()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for the expected string to test for tags and escape characters
        self.assertTrue(expected_subtitle in crossref_xml_string)


    def test_component_subtitle_with_face_markup(self):
        "build an article object and component, generate Crossref XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        component = Component()
        component.title = "A component"
        component.subtitle = "A <sc>STRANGE</sc> <italic>subtitle</italic>, and this tag is <not_allowed>!</not_allowed>"
        expected_subtitle = "A <sc>STRANGE</sc> <i>subtitle</i>, and this tag is &lt;not_allowed&gt;!&lt;/not_allowed&gt;"
        article.component_list = [component]
        # load a config and override the value
        raw_config = config['elife']
        face_markup = raw_config.get('face_markup')
        raw_config['face_markup'] = 'true'
        crossref_config = parse_raw_config(raw_config)
        # generate the crossrefXML
        cXML = generate.crossrefXML([article], crossref_config, None, True)
        crossref_xml_string = cXML.output_XML()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for the expected string to test for tags and escape characters
        self.assertTrue(expected_subtitle in crossref_xml_string)
        # now set the config back to normal
        raw_config['face_markup'] = face_markup


class TestGenerateContributors(unittest.TestCase):

    def setUp(self):
        pass

    def test_generate_no_contributors(self):
        """
        Test when an article has no contributors
        """
        "build an article object and component, generate Crossref XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        # generate the crossrefXML
        cXML = generate.build_crossref_xml([article])
        crossref_xml_string = cXML.output_XML()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for a string value to test
        self.assertTrue('<contributors' not in crossref_xml_string)


class TestGenerateCrossrefSchemaVersion(unittest.TestCase):

    def setUp(self):
        pass

    def test_generate_crossref_schema_version_4_3_5(self):
        self.generate_crossref_schema_version(
            '4.3.5',
            'xmlns="http://www.crossref.org/schema/4.3.5"'
        )

    def test_generate_crossref_schema_version_4_3_7(self):
        self.generate_crossref_schema_version(
            '4.3.7',
            'xmlns="http://www.crossref.org/schema/4.3.7"'
        )

    def test_generate_crossref_schema_version_4_4_0(self):
        self.generate_crossref_schema_version(
            '4.4.0',
            'xmlns="http://www.crossref.org/schema/4.4.0"'
        )

    def generate_crossref_schema_version(self, crossref_schema_version, expected_snippet):
        """
        Test non-default crossref schema version
        """
        "build an article object and component, generate Crossref XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        # load a config and override the value
        raw_config = config['elife']
        original_crossref_schema_version = raw_config.get('crossref_schema_version')
        raw_config['crossref_schema_version'] = crossref_schema_version
        crossref_config = parse_raw_config(raw_config)
        # generate the crossrefXML
        cXML = generate.build_crossref_xml([article])
        crossref_xml_string = cXML.output_XML()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for a string value to test
        self.assertTrue(expected_snippet in crossref_xml_string)
        # now set the config back to normal
        raw_config['crossref_schema_version'] = original_crossref_schema_version


class TestGenerateCrossrefCitationPublisher(unittest.TestCase):

    def setUp(self):
        self.publisher_loc = "Nijmegen, The Netherlands"
        self.publisher_name = "Radboud University Nijmegen Medical Centre"

    def test_generate_citation_publisher_none(self):
        "no publisher name concatenation"
        citation = Citation()
        cXML = generate.crossrefXML([], {})
        self.assertIsNone(cXML.citation_publisher(citation))

    def test_generate_citation_publisher_loc_only(self):
        "no publisher name concatenation"
        citation = Citation()
        citation.publisher_loc = self.publisher_loc
        cXML = generate.crossrefXML([], {})
        self.assertEqual(
            cXML.citation_publisher(citation),
            "Nijmegen, The Netherlands")

    def test_generate_citation_publisher_name_only(self):
        "no publisher name concatenation"
        citation = Citation()
        citation.publisher_name = self.publisher_name
        cXML = generate.crossrefXML([], {})
        self.assertEqual(
            cXML.citation_publisher(citation),
            "Radboud University Nijmegen Medical Centre")

    def test_generate_citation_publisher_all(self):
        "no publisher name concatenation"
        citation = Citation()
        citation.publisher_loc = self.publisher_loc
        citation.publisher_name = self.publisher_name
        cXML = generate.crossrefXML([], {})
        self.assertEqual(
            cXML.citation_publisher(citation),
            "Nijmegen, The Netherlands: Radboud University Nijmegen Medical Centre")


class TestGenerateCrossrefUnstructuredCitation(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_unstructured_citation_no_face_markup(self):
        "unstructured citation example with no face markup"
        article_title = 'PhD thesis: Submicroscopic <italic>Plasmodium falciparum</italic> gametocytaemia and the contribution to malaria transmission'
        expected = '<citation><unstructured_citation>PhD thesis: Submicroscopic Plasmodium falciparum gametocytaemia and the contribution to malaria transmission.</unstructured_citation></citation>'
        crossref_config = {}
        citation = Citation()
        citation.article_title = article_title
        citation.publication_type = 'patent'
        cXML = generate.crossrefXML([], crossref_config)
        parent = Element('citation')
        citation_element = cXML.set_unstructured_citation(parent, citation)
        rough_string = ElementTree.tostring(citation_element)
        self.assertEqual(rough_string, expected)

    def test_set_unstructured_citation_face_markup(self):
        "unstructured citation example which does include face markup"
        article_title = 'PhD thesis: Submicroscopic <italic>Plasmodium falciparum</italic> gametocytaemia and the contribution to malaria transmission'
        expected = '<citation><unstructured_citation>PhD thesis: Submicroscopic <i>Plasmodium falciparum</i> gametocytaemia and the contribution to malaria transmission.</unstructured_citation></citation>'
        # load a config and override the value
        raw_config = config['elife']
        original_face_markup = raw_config.get('face_markup')
        raw_config['face_markup'] = 'true'
        crossref_config = parse_raw_config(raw_config)
        # continue
        citation = Citation()
        citation.article_title = article_title
        citation.publication_type = 'patent'
        cXML = generate.crossrefXML([], crossref_config)
        parent = Element('citation')
        citation_element = cXML.set_unstructured_citation(parent, citation)
        rough_string = ElementTree.tostring(citation_element)
        self.assertEqual(rough_string, expected)
        # now set the config back to normal
        raw_config['face_markup'] = original_face_markup



if __name__ == '__main__':
    unittest.main()
