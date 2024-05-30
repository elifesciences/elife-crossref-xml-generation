import unittest

from elifearticle.article import (
    Article,
    Award,
    Component,
    Citation,
    Dataset,
    FundingAward,
    Contributor,
    Affiliation,
    Preprint,
)

from elifecrossref import generate
from elifecrossref.conf import raw_config, parse_raw_config


class TestGenerateComponentList(unittest.TestCase):
    def setUp(self):
        pass

    def test_component_subtitle_no_face_markup(self):
        """build an article object and component, generate Crossref XML"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        component = Component()
        component.title = "A component"
        component.subtitle = (
            "A <sc>STRANGE</sc> <italic>subtitle</italic>, "
            + "and this tag is <not_allowed>!</not_allowed>"
        )
        expected_subtitle = (
            "A STRANGE subtitle, and this tag is"
            " &lt;not_allowed&gt;!&lt;/not_allowed&gt;"
        )
        article.component_list = [component]
        # generate the crossrefXML
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for the expected string to test for tags and escape characters
        self.assertTrue(expected_subtitle in crossref_xml_string)

    def test_component_subtitle_with_face_markup(self):
        """build an article object and component, generate Crossref XML"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        component = Component()
        component.title = "A component"
        component.subtitle = (
            "A <sc>STRANGE</sc> <italic>subtitle</italic>, "
            + "and this tag is <not_allowed>!</not_allowed>"
        )
        expected_subtitle = (
            "A <sc>STRANGE</sc> <i>subtitle</i>, and this tag "
            + "is &lt;not_allowed&gt;!&lt;/not_allowed&gt;"
        )
        article.component_list = [component]
        # load a config and override the value
        raw_config_object = raw_config("elife")
        face_markup = raw_config_object.get("face_markup")
        raw_config_object["face_markup"] = "true"
        crossref_config = parse_raw_config(raw_config_object)
        # generate the crossrefXML
        c_xml = generate.CrossrefXML([article], crossref_config, None, True)
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for the expected string to test for tags and escape characters
        self.assertTrue(expected_subtitle in crossref_xml_string)
        # now set the config back to normal
        raw_config_object["face_markup"] = face_markup


class TestGenerateContributors(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_no_contributors(self):
        """Test when an article has no contributors"""
        # build an article object and component, generate Crossref XML
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        # generate the crossrefXML
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for a string value to test
        self.assertTrue("<contributors" not in crossref_xml_string)

    def test_generate_blank_affiliation(self):
        """Test when a contributor has a blank affiliation"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        author = Contributor("author", "Surname", "Given names")
        aff = Affiliation()
        aff.text = ""
        author.set_affiliation(aff)
        # generate the crossrefXML
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for a string value to test
        self.assertTrue("<affiliation>" not in crossref_xml_string)


class TestGenerateCrossrefSchemaVersion(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_crossref_schema_version_4_3_5(self):
        self.generate_crossref_schema_version(
            "4.3.5", 'xmlns="http://www.crossref.org/schema/4.3.5"'
        )

    def test_generate_crossref_schema_version_4_3_7(self):
        self.generate_crossref_schema_version(
            "4.3.7", 'xmlns="http://www.crossref.org/schema/4.3.7"'
        )

    def test_generate_crossref_schema_version_4_4_0(self):
        self.generate_crossref_schema_version(
            "4.4.0", 'xmlns="http://www.crossref.org/schema/4.4.0"'
        )

    def test_generate_crossref_schema_version_4_4_1(self):
        self.generate_crossref_schema_version(
            "4.4.1", 'xmlns="http://www.crossref.org/schema/4.4.1"'
        )

    def generate_crossref_schema_version(
        self, crossref_schema_version, expected_snippet
    ):
        """Test non-default crossref schema version"""
        # build an article object and component, generate Crossref XML
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        # load a config and override the value
        raw_config_object = raw_config("elife")
        original_schema_version = raw_config_object.get("crossref_schema_version")
        raw_config_object["crossref_schema_version"] = crossref_schema_version
        crossref_config = parse_raw_config(raw_config_object)
        # generate the crossrefXML
        c_xml = generate.CrossrefXML([article], crossref_config, None, True)
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # A quick test just look for a string value to test
        self.assertTrue(expected_snippet in crossref_xml_string)
        # now set the config back to normal
        raw_config_object["crossref_schema_version"] = original_schema_version


class TestGenerateCrossrefCitationId(unittest.TestCase):
    def setUp(self):
        pass

    def test_ref_list_citation_with_no_id(self):
        """for test coverage an article with a ref_list with a citation that has no id attribute"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        citation = Citation()
        citation.article_title = "An article title"
        article.ref_list = [citation]
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        self.assertTrue('<citation key="1">' in crossref_xml_string)


class TestGenerateCrossrefCitationElocationId(unittest.TestCase):
    def test_ref_list_citation_elocation_id(self):
        """for test coverage for schema where elocation_id goes into first_page element"""
        # load a config and override the value
        raw_config_object = raw_config("elife")
        original_schema_version = raw_config_object.get("crossref_schema_version")
        raw_config_object["crossref_schema_version"] = "4.4.0"
        crossref_config = parse_raw_config(raw_config_object)
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        citation = Citation()
        citation.elocation_id = "e00003"
        article.ref_list = [citation]
        c_xml = generate.CrossrefXML([article], crossref_config, None, True)
        crossref_xml_string = c_xml.output_xml()
        self.assertTrue("<first_page>e00003</first_page>" in crossref_xml_string)
        # now set the config back to normal
        raw_config_object["crossref_schema_version"] = original_schema_version


class TestGenerateCrossrefDatasets(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_datasets(self):
        """a basic non-XML example for set_datasets"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        # dataset_1 example with a uri
        dataset_1 = Dataset()
        dataset_1.dataset_type = "datasets"
        dataset_1.uri = (
            "https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml"
        )
        dataset_1.title = "Kitchen sink"
        # dataset_2 example with accession_id
        dataset_2 = Dataset()
        dataset_2.dataset_type = "prev_published_datasets"
        dataset_2.accession_id = "EGAS00001000968"
        # dataset_3 example with doi
        dataset_3 = Dataset()
        dataset_3.dataset_type = "prev_published_datasets"
        dataset_3.doi = "10.5061/dryad.cv323"
        # dataset_4 example with no dataset_type will be treated as a generated dataset by default
        dataset_4 = Dataset()
        dataset_4.uri = "http://cghub.ucsc.edu"
        # dataset_5 example with an unsupported dataset_type
        dataset_5 = Dataset()
        dataset_5.dataset_type = "foo"
        dataset_5.uri = "https://elifesciences.org"
        # dataset_6 example with no identifier, not get added to the XML output, for test coverage
        dataset_6 = Dataset()
        dataset_6.dataset_type = "prev_published_datasets"
        # add the datasets to the article object
        article.add_dataset(dataset_1)
        article.add_dataset(dataset_2)
        article.add_dataset(dataset_3)
        article.add_dataset(dataset_4)
        article.add_dataset(dataset_5)
        article.add_dataset(dataset_6)
        # add a software citation
        citation = Citation()
        citation.publication_type = "software"
        citation.article_title = "Data citation"
        citation.uri = "https://archive.softwareheritage.org"
        article.ref_list = [citation]
        # expected values
        expected_xml_snippet_1 = (
            "<rel:program><rel:related_item><rel:description>Kitchen sink</rel:description>"
            + '<rel:inter_work_relation identifier-type="uri" '
            + 'relationship-type="isSupplementedBy">'
            + "https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml"
            + "</rel:inter_work_relation></rel:related_item>"
        )
        expected_xml_snippet_2 = (
            '<rel:related_item><rel:inter_work_relation identifier-type="accession" '
            + 'relationship-type="references">EGAS00001000968</rel:inter_work_relation>'
            + "</rel:related_item>"
        )
        expected_xml_snippet_3 = (
            '<rel:related_item><rel:inter_work_relation identifier-type="doi" '
            + 'relationship-type="references">10.5061/dryad.cv323</rel:inter_work_relation>'
            + "</rel:related_item>"
        )
        expected_xml_snippet_4 = (
            '<rel:related_item><rel:inter_work_relation identifier-type="uri" '
            + 'relationship-type="isSupplementedBy">http://cghub.ucsc.edu'
            + "</rel:inter_work_relation></rel:related_item>"
        )
        expected_xml_snippet_5 = (
            '<rel:related_item><rel:inter_work_relation identifier-type="uri" '
            + 'relationship-type="isSupplementedBy">https://elifesciences.org'
            + "</rel:inter_work_relation></rel:related_item>"
        )
        expected_xml_snippet_6 = (
            '<rel:related_item><rel:inter_work_relation identifier-type="uri" '
            'relationship-type="isSupplementedBy">https://archive.softwareheritage.org'
            "</rel:inter_work_relation></rel:related_item>"
        )
        # generate output
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # Test for expected strings in the XML output
        self.assertTrue(expected_xml_snippet_1 in crossref_xml_string)
        self.assertTrue(expected_xml_snippet_2 in crossref_xml_string)
        self.assertTrue(expected_xml_snippet_3 in crossref_xml_string)
        self.assertTrue(expected_xml_snippet_4 in crossref_xml_string)
        self.assertTrue(expected_xml_snippet_5 in crossref_xml_string)
        self.assertTrue(expected_xml_snippet_6 in crossref_xml_string)


class TestGenerateCrossrefDataCitation(unittest.TestCase):
    def setUp(self):
        pass

    def test_ref_list_data_citation_with_pmid(self):
        """
        for test coverage an article with a ref_list with a
        data citation that has a pmid attribute
        """
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        citation = Citation()
        citation.data_title = "An data title"
        citation.publication_type = "data"
        citation.pmid = "pmid"
        article.ref_list = [citation]
        expected_contains = (
            "<rel:program><rel:related_item><rel:description>An data title</rel:description>"
            + '<rel:inter_work_relation identifier-type="pmid" relationship-type="references">'
            + "pmid</rel:inter_work_relation></rel:related_item></rel:program>"
        )
        # generate
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)


class TestGenerateAbstract(unittest.TestCase):
    def setUp(self):
        self.abstract = (
            '<p><bold><italic><underline><sub><sup>An abstract. <ext-link ext-link-type="uri" '
            + 'xlink:href="http://dx.doi.org/10.1601/nm.3602">Desulfocapsa sulfexigens</ext-link>.'
            + "</sup></sub></underline></italic></bold>"
            + ' <xref ref-type="bibr" rid="bib18">Stock and Wise (1990)</xref>.</p>'
        )

    def test_set_abstract(self):
        """test stripping unwanted tags from abstract"""
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        article.abstract = self.abstract
        expected_contains = (
            "<jats:abstract><jats:p>An abstract. Desulfocapsa sulfexigens."
            + " Stock and Wise (1990).</jats:p></jats:abstract>"
        )
        # generate
        crossref_object = generate.build_crossref_xml([article])
        crossref_xml_string = crossref_object.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)


class TestGenerateTitles(unittest.TestCase):
    def setUp(self):
        self.title = (
            '\n<bold>Test article</bold>\n for \n<ext-link ext-link-type="uri" '
            + 'xlink:href="http://dx.doi.org/10.1601/nm.3602">Desulfocapsa sulfexigens</ext-link>\n'
        )

    def test_set_titles(self):
        """test stripping unwanted tags from title"""
        doi = "10.7554/eLife.00666"
        article = Article(doi, self.title)
        expected_contains = (
            "<titles><title>Test article for Desulfocapsa sulfexigens</title></titles>"
        )
        # generate
        crossref_object = generate.build_crossref_xml([article])
        crossref_xml_string = crossref_object.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)

    def test_set_titles_face_markup_format(self):
        """test the title using face markup set to true"""
        doi = "10.7554/eLife.00666"
        article = Article(doi, self.title)
        expected_contains = (
            "<titles><title><b>Test article</b> for"
            " Desulfocapsa sulfexigens</title></titles>"
        )
        # generate
        raw_config_object = raw_config("elife")
        face_markup = raw_config_object.get("face_markup")
        raw_config_object["face_markup"] = "true"
        crossref_config = parse_raw_config(raw_config_object)
        crossref_object = generate.CrossrefXML([article], crossref_config, None, True)
        crossref_xml_string = crossref_object.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)
        # now set the config back to normal
        raw_config_object["face_markup"] = face_markup


class TestGeneratePreprint(unittest.TestCase):
    def test_article_preprint(self):
        """test for an article with preprint data"""
        doi = "10.7554/eLife.00666"
        article = Article(doi, title="Sample article")
        article.preprint = Preprint(uri="https://example.org/")
        expected_contains = (
            "<rel:program>"
            "<rel:related_item>"
            '<rel:intra_work_relation identifier-type="uri"'
            ' relationship-type="hasPreprint">https://example.org/'
            "</rel:intra_work_relation>"
            "</rel:related_item>"
            "</rel:program>"
        )
        # generate
        crossref_object = generate.build_crossref_xml([article])
        crossref_xml_string = crossref_object.output_xml()
        # test assertion
        self.assertTrue(expected_contains in crossref_xml_string)


class TestGenerateFunding(unittest.TestCase):
    def test_set_funding(self):
        "a basic non-XML example for funding data"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        article = Article(doi, title)
        award = Award()
        award.award_id = "10.13039/501100001824"
        award.award_id_type = "doi"
        funding_award = FundingAward()
        funding_award.add_award(award)
        article.funding_awards = [funding_award]
        # expected values
        expected_xml_snippet = (
            "<rel:program>"
            "<rel:related_item>"
            '<rel:inter_work_relation identifier-type="doi" relationship-type="isFinancedBy">'
            "10.13039/501100001824"
            "</rel:inter_work_relation>"
            "</rel:related_item>"
            "</rel:program>"
        )
        # generate output
        c_xml = generate.build_crossref_xml([article])
        crossref_xml_string = c_xml.output_xml()
        self.assertIsNotNone(crossref_xml_string)
        # Test for expected strings in the XML output
        self.assertTrue(expected_xml_snippet in crossref_xml_string)


if __name__ == "__main__":
    unittest.main()
