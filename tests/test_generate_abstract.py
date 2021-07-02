import unittest
from elifearticle.article import Article
from elifecrossref import generate
from elifecrossref.conf import raw_config, parse_raw_config


class TestGenerateAbstract(unittest.TestCase):
    def setUp(self):
        self.abstract = (
            '<p><bold><italic><underline><sub><sup>An abstract. <ext-link ext-link-type="uri" '
            'xlink:href="http://dx.doi.org/10.1601/nm.3602">Desulfocapsa sulfexigens</ext-link>.'
            "</sup></sub></underline></italic></bold>"
            ' <xref ref-type="bibr" rid="bib18">Stock and Wise (1990)</xref>.</p>'
        )
        self.abstract_xml = (
            '<abstract id="foo" xlmns:mml="http://www.w3.org/1998/Math/MathML">'
            '<object-id pub-id-type="doi">10.7554/eLife.39122.001</object-id>'
            '<p><bold><italic><underline><sub><sup>An abstract. <ext-link ext-link-type="uri" '
            'xlink:href="http://dx.doi.org/10.1601/nm.3602">Desulfocapsa sulfexigens</ext-link>.'
            "</sup></sub></underline></italic></bold>"
            ' <xref ref-type="bibr" rid="bib18">Stock and Wise (1990)</xref>.</p></abstract>'
        )

    def test_set_abstract(self):
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        article.abstract = self.abstract
        article.abstract_xml = self.abstract_xml
        expected_contains = (
            "<jats:abstract><jats:p>An abstract. Desulfocapsa sulfexigens."
            " Stock and Wise (1990).</jats:p></jats:abstract>"
        )
        # generate
        crossref_object = generate.build_crossref_xml([article])
        crossref_xml_string = crossref_object.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)

    def test_set_abstract_jats_abstract_format(self):
        """test the abstract using jats abstract format set to true"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        article.abstract = self.abstract
        article.abstract_xml = self.abstract_xml
        expected_contains = (
            '<jats:abstract xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<jats:p xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<jats:bold><jats:italic><jats:underline><jats:sub><jats:sup>"
            "An abstract. "
            '<jats:ext-link ext-link-type="uri" xlink:href="http://dx.doi.org/10.1601/nm.3602">'
            "Desulfocapsa sulfexigens</jats:ext-link>."
            "</jats:sup></jats:sub></jats:underline></jats:italic></jats:bold> "
            '<jats:xref ref-type="bibr">Stock and Wise (1990)</jats:xref>.'
            "</jats:p></jats:abstract>"
        )
        # generate
        raw_config_object = raw_config("elife")
        jats_abstract = raw_config_object.get("jats_abstract")
        raw_config_object["jats_abstract"] = "true"
        crossref_config = parse_raw_config(raw_config_object)
        crossref_object = generate.CrossrefXML([article], crossref_config, None, True)
        crossref_xml_string = crossref_object.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)
        # now set the config back to normal
        raw_config_object["jats_abstract"] = jats_abstract
