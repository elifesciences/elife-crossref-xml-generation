import unittest
from elifearticle.article import Article, License
from elifecrossref import collection
from elifecrossref.conf import raw_config, parse_raw_config


class TestSetCollection(unittest.TestCase):

    def setUp(self):
        self.crossref_config = create_crossref_config()

    def test_do_set_collection_no_license(self):
        """test when an article has no license"""
        # create CrossrefXML object to test
        article = create_aricle_object()
        # test assertion
        self.assertFalse(collection.do_set_collection(article, "text-mining", self.crossref_config))

    def test_do_set_collection_empty_license(self):
        """test when an article has no license"""
        article = create_aricle_object()
        # create an empty license
        license_object = License()
        article.license = license_object
        # test assertion
        self.assertFalse(collection.do_set_collection(article, "text-mining", self.crossref_config))

    def test_do_set_collection_with_license(self):
        """test when an article has no license"""
        article = create_aricle_object()
        # create a license with a href value
        license_object = License()
        license_object.href = "http://example.org/license.txt"
        article.license = license_object
        # test assertion
        self.assertTrue(collection.do_set_collection(article, "text-mining", self.crossref_config))


def create_aricle_object():
    """create a basic article object"""
    doi = "10.7554/eLife.00666"
    title = "Test article"
    article = Article(doi, title)
    return article


def create_crossref_config():
    """utility to create the crossref object"""
    raw_config_object = raw_config('elife')
    return parse_raw_config(raw_config_object)



if __name__ == '__main__':
    unittest.main()
