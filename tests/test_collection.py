import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article, License, Uri
from elifecrossref import collection
from tests import create_crossref_config


class TestSetCollection(unittest.TestCase):
    def test_text_mining_vor(self):
        parent = Element("root")
        crossref_config = create_crossref_config("elife")
        article = Article("10.7554/eLife.00666", "Test article")
        article.manuscript = "00666"
        article.version = "1"
        # self_uri
        uri = Uri()
        uri.xlink_href = "elife-06666.pdf"
        uri.content_type = "pdf"
        article.self_uri_list = [uri]
        # create a license with a href value
        license_object = License()
        license_object.href = "http://example.org/license.txt"
        article.license = license_object
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<collection property="text-mining">'
            b"<item>"
            b'<resource mime_type="application/pdf">'
            b"https://cdn.elifesciences.org/articles/00666/elife-00666-v1.pdf"
            b"</resource>"
            b"</item>"
            b"<item>"
            b'<resource mime_type="application/xml">'
            b"https://cdn.elifesciences.org/articles/00666/elife-00666-v1.xml"
            b"</resource>"
            b"</item>"
            b"</collection>"
            b"</root>"
        )
        collection.set_collection(parent, article, "text-mining", crossref_config)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_crawler_based_preprint(self):
        parent = Element("root")
        crossref_config = create_crossref_config("elife_preprint")
        article = Article("10.7554/eLife.00666", "Test article")
        article.manuscript = "00666"
        article.article_type = "preprint"
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<collection property="crawler-based">'
            b'<item crawler="iParadigms">'
            b"<resource>https://elifesciences.org/reviewed-preprints/00666/pdf</resource>"
            b"</item>"
            b"</collection>"
            b"</root>"
        )
        collection.set_collection(parent, article, "crawler-based", crossref_config)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_crawler_based_poa(self):
        parent = Element("root")
        crossref_config = create_crossref_config("elife")
        article = Article("10.7554/eLife.00666", "Test article")
        article.manuscript = "00666"
        article.is_poa = True
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<collection property="crawler-based">'
            b'<item crawler="iParadigms">'
            b"<resource>https://cdn.elifesciences.org/articles/00666/elife-00666.pdf</resource>"
            b"</item>"
            b"</collection>"
            b"</root>"
        )
        collection.set_collection(parent, article, "crawler-based", crossref_config)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_crawler_based_vor(self):
        parent = Element("root")
        crossref_config = create_crossref_config("elife")
        article = Article("10.7554/eLife.00666", "Test article")
        article.manuscript = "00666"
        article.is_poa = False
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<collection property="crawler-based">'
            b'<item crawler="iParadigms">'
            b"<resource>https://elifesciences.org/articles/00666</resource>"
            b"</item>"
            b"</collection>"
            b"</root>"
        )
        collection.set_collection(parent, article, "crawler-based", crossref_config)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)


class TestDoSetCollection(unittest.TestCase):
    def setUp(self):
        self.crossref_config = create_crossref_config()

    def test_do_set_collection_no_license(self):
        """test when an article has no license"""
        # create CrossrefXML object to test
        article = Article("10.7554/eLife.00666", "Test article")
        # test assertion
        self.assertFalse(
            collection.do_set_collection(article, "text-mining", self.crossref_config)
        )

    def test_do_set_collection_empty_license(self):
        """test when an article has no license"""
        article = Article("10.7554/eLife.00666", "Test article")
        # create an empty license
        license_object = License()
        article.license = license_object
        # test assertion
        self.assertFalse(
            collection.do_set_collection(article, "text-mining", self.crossref_config)
        )

    def test_do_set_collection_with_license(self):
        """test when an article has no license"""
        article = Article("10.7554/eLife.00666", "Test article")
        # create a license with a href value
        license_object = License()
        license_object.href = "http://example.org/license.txt"
        article.license = license_object
        # test assertion
        self.assertTrue(
            collection.do_set_collection(article, "text-mining", self.crossref_config)
        )

    def test_iparadigms_preprint(self):
        "test a preprint article iparadigms setting"
        crossref_config = create_crossref_config("elife_preprint")
        article = Article("10.7554/eLife.00666", "Test article")
        article.article_type = "preprint"
        # test assertion
        self.assertTrue(
            collection.do_set_collection(article, "crawler-based", crossref_config)
        )

    def test_iparadigms_poa(self):
        "test for a poa article iparadigms setting"
        article = Article("10.7554/eLife.00666", "Test article")
        article.is_poa = True
        # test assertion
        self.assertTrue(
            collection.do_set_collection(article, "crawler-based", self.crossref_config)
        )

    def test_iparadigms_vor(self):
        "test for a poa article iparadigms setting"
        article = Article("10.7554/eLife.00666", "Test article")
        article.is_poa = False
        # test assertion
        self.assertTrue(
            collection.do_set_collection(article, "crawler-based", self.crossref_config)
        )


class TestTextMiningXml(unittest.TestCase):
    def test_do_set_collection_text_mining_xml(self):
        "test for XML text-mining setting"
        crossref_config = create_crossref_config()
        # test assertion
        self.assertTrue(collection.do_set_collection_text_mining_xml(crossref_config))

    def test_no_setting(self):
        "test if setting is blank"
        crossref_config = create_crossref_config("DEFAULT")
        # test assertion
        self.assertEqual(
            collection.do_set_collection_text_mining_xml(crossref_config), False
        )


class TestTextMiningPdf(unittest.TestCase):
    def test_do_set_collection_text_mining_pdf(self):
        "test for PDF text-mining setting"
        crossref_config = create_crossref_config()
        article = Article("10.7554/eLife.00666", "Test article")
        # self_uri
        uri = Uri()
        uri.xlink_href = "elife-06666.pdf"
        uri.content_type = "pdf"
        article.self_uri_list = [uri]
        # test assertion
        self.assertTrue(
            collection.do_set_collection_text_mining_pdf(article, crossref_config)
        )

    def test_no_iparadigms(self):
        crossref_config = create_crossref_config("DEFAULT")
        "test if setting is blank"
        article = Article("10.7554/eLife.00666", "Test article")
        # test assertion
        self.assertEqual(
            collection.do_set_collection_text_mining_pdf(article, crossref_config),
            False,
        )


class TestIParadigmsSettingName(unittest.TestCase):
    def test_iparadigms_setting_name_preprint(self):
        article = Article("10.7554/eLife.00666", "Test article")
        article.article_type = "preprint"
        self.assertEqual(
            collection.iparadigms_setting_name(article), "iparadigms_preprint_pattern"
        )

    def test_iparadigms_setting_name_poa(self):
        article = Article("10.7554/eLife.00666", "Test article")
        article.is_poa = True
        self.assertEqual(
            collection.iparadigms_setting_name(article), "iparadigms_poa_pattern"
        )

    def test_iparadigms_setting_name_vor(self):
        article = Article("10.7554/eLife.00666", "Test article")
        article.is_poa = False
        self.assertEqual(
            collection.iparadigms_setting_name(article), "iparadigms_vor_pattern"
        )

    def test_iparadigms_setting_name_unknown(self):
        article = Article("10.7554/eLife.00666", "Test article")
        article.is_poa = None
        self.assertEqual(collection.iparadigms_setting_name(article), None)


class TestIParadigms(unittest.TestCase):
    def test_do_set_collection_iparadigms(self):
        "test for iparadigms setting"
        crossref_config = create_crossref_config()
        article = Article("10.7554/eLife.00666", "Test article")
        article.is_poa = False
        # test assertion
        self.assertTrue(
            collection.do_set_collection_iparadigms(article, crossref_config)
        )

    def test_no_iparadigms(self):
        "test settings with no iparadigms"
        crossref_config = create_crossref_config("DEFAULT")
        article = Article("10.7554/eLife.00666", "Test article")
        # test assertion
        self.assertEqual(
            collection.do_set_collection_iparadigms(article, crossref_config), False
        )
