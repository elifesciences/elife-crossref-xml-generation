import unittest
import time
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article, ArticleDate
from elifecrossref import pending_publication
from tests import create_crossref_config


class TestSetPendingPublication(unittest.TestCase):
    "tests for set_pending_publication()"

    def test_set_pending_publication(self):
        parent = Element("root")
        crossref_config = create_crossref_config("elife")
        article = Article()
        article.title = "Title to be confirmed"
        article.journal_issn = "2050-084X"
        article.doi = "10.7554/eLife.00666"
        sent_for_review_date = ArticleDate(
            "sent-for-review", time.strptime("2024-07-19", "%Y-%m-%d")
        )
        article.add_date(sent_for_review_date)
        expected = bytes(
            (
                "<root>"
                "<pending_publication>"
                "<publication>"
                "<full_title>eLife</full_title>"
                '<issn media_type="electronic">2050-084X</issn>'
                "</publication>"
                "<titles>"
                "<title>Title to be confirmed</title>"
                "</titles>"
                "<acceptance_date>"
                "<month>07</month>"
                "<day>19</day>"
                "<year>2024</year>"
                "</acceptance_date>"
                "<doi>10.7554/eLife.00666</doi>"
                "</pending_publication>"
                "</root>"
            ),
            encoding="utf-8",
        )
        pending_publication.set_pending_publication(parent, article, crossref_config)
        parent_string = ElementTree.tostring(parent, "utf-8")
        self.assertEqual(parent_string, expected)
