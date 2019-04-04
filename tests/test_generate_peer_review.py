import unittest
import time
import os
from elifearticle.article import Article, ArticleDate, Contributor
from elifecrossref import generate
from elifecrossref.conf import raw_config, parse_raw_config
from tests import TEST_BASE_PATH, TEST_DATA_PATH, read_file_content


generate.TMP_DIR = TEST_BASE_PATH + "tmp" + os.sep


def sample_data():
    """some sample data for development until real object definition is final and XML is parsed"""
    reviews = []
    # decision letter
    decision_letter = Article()
    decision_letter.article_type = 'editor-report'
    dec_author = Contributor('editor', 'Christian', 'Rutz')
    decision_letter.contributors.append(dec_author)
    decision_letter.title = (
        'Decision letter: Immune mediated hookworm clearance and survival of a marine mammal ' +
        'decreases with warmer ocean temperatures')
    # review date
    review_date = ArticleDate(
        'review_date', time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S"))
    decision_letter.add_date(review_date)
    # related article doi
    related_article = Article()
    related_article.doi = '10.7554/eLife.00666'
    decision_letter.related_articles = [related_article]
    # review article doi
    decision_letter.doi = '10.7554/eLife.00666.029'
    # a hack to get the resource url right for now
    decision_letter.manuscript = '00666#SA1'
    # append it
    reviews.append(decision_letter)

    # author response
    author_response = Article()
    author_response.article_type = 'author-comment'
    article_author = Contributor('author', 'Harrison', 'Melissa')
    author_response.contributors.append(article_author)
    author_response.title = (
        'Author response: Immune mediated hookworm clearance and survival of a marine mammal ' +
        'decreases with warmer ocean temperatures')
    # review date
    review_date = ArticleDate(
        'review_date', time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S"))
    author_response.add_date(review_date)
    # related article doi
    related_article = Article()
    related_article.doi = '10.7554/eLife.00666'
    author_response.related_articles = [related_article]
    # review article doi
    author_response.doi = '10.7554/eLife.00666.030'
    # a hack to get the resource url right for now
    author_response.manuscript = '00666#SA2'
    # append it
    reviews.append(author_response)

    return reviews


class TestGeneratePeerReview(unittest.TestCase):

    def setUp(self):
        self.passes = []
        self.default_pub_date = time.strptime("2017-07-17 07:17:07", "%Y-%m-%d %H:%M:%S")
        self.passes.append(
            ('elife-00666.xml', 'elife-crossref-peer_review-00666-20170717071707.xml',
             'elife', self.default_pub_date))

    def test_parse(self):
        for (article_xml_file, crossref_xml_file, config_section, pub_date) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = generate.build_articles_for_crossref([file_path])
            # set some review sample data
            articles[0].review_articles = sample_data()
            crossref_config = None
            if config_section:
                crossref_config = parse_raw_config(raw_config(config_section))
            crossref_xml = generate.crossref_xml(articles, crossref_config, pub_date, False,
                                                 'peer_review', pretty=True, indent="    ")
            model_crossref_xml = read_file_content(TEST_DATA_PATH + crossref_xml_file)
            self.assertEqual(crossref_xml, model_crossref_xml.decode('utf-8'),
                             'Failed parse test on file %s' % article_xml_file)
