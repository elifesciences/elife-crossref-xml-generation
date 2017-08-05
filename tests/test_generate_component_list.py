import unittest
import time
import os
import re
from elifecrossref import generate
from elifecrossref.conf import config
from elifearticle.article import Article, Component

class TestGenerateComponentList(unittest.TestCase):

    def setUp(self):
        pass

    def test_component_subtitle(self):
        "build an article object and component, generate Crossref XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        component = Component()
        component.title = "A component"
        component.subtitle = "A <sc>STRANGE</sc> <italic>subtitle</italic>, and this tag is <not_allowed>!</not_allowed>"
        expected_subtitle = "A <sc>STRANGE</sc> <i>subtitle</i>, and this tag is &lt;not_allowed&gt;!&lt;/not_allowed&gt;"
        article.component_list = [component]
        # generate the crossrefXML
        cXML = generate.build_crossref_xml([article])
        crossref_xml_string = cXML.output_XML()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for the expected string to test for tags and escape characters
        self.assertTrue(expected_subtitle in crossref_xml_string)


if __name__ == '__main__':
    unittest.main()
