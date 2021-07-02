import unittest
from elifearticle.article import Article, License
from elifecrossref import collection
from tests import create_crossref_config


class TestSetCollection(unittest.TestCase):
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
