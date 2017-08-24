import unittest
import time
import os
import re
from elifecrossref import generate
from elifecrossref.conf import config, parse_raw_config
from elifearticle.article import Article, Component

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

    def test_generate_crossref_schema_version(self):
        """
        Test non-default crossref schema version
        """
        "build an article object and component, generate Crossref XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        # load a config and override the value
        raw_config = config['elife']
        crossref_schema_version = raw_config.get('crossref_schema_version')
        raw_config['crossref_schema_version'] = '4.3.5'
        crossref_config = parse_raw_config(raw_config)
        # generate the crossrefXML
        cXML = generate.build_crossref_xml([article])
        crossref_xml_string = cXML.output_XML()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for a string value to test
        self.assertTrue('xmlns="http://www.crossref.org/schema/4.3.5"' in crossref_xml_string)
        # now set the config back to normal
        raw_config['crossref_schema_version'] = crossref_schema_version




if __name__ == '__main__':
    unittest.main()