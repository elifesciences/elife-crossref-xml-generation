import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article
from elifecrossref import peer_review
from tests import create_crossref_config


class TestSetType(unittest.TestCase):
    def test_set_type(self):
        passes = [
            {"article_type": "_not_yet_supported", "expected": b"<root />"},
            {
                "article_type": "article-commentary",
                "expected": b'<root type="editor-report" />',
            },
            {
                "article_type": "reply",
                "expected": b'<root type="author-comment" />',
            },
            {
                "article_type": "referee-report",
                "expected": b'<root type="referee-report" />',
            },
        ]
        for data in passes:
            parent = Element("root")
            article = Article()
            article.article_type = data.get("article_type")
            peer_review.set_type(parent, article)
            parent_string = ElementTree.tostring(parent, "utf-8")
            self.assertEqual(
                parent_string,
                data.get("expected"),
                "failed on article_type %s" % data.get("article_type"),
            )


class TestSetTitle(unittest.TestCase):
    def test_set_title(self):
        "test formatting some peer review article titles"
        passes = [
            {
                "title": "",
                "expected": b"<root><titles><title>"
                b"Main article title"
                b"</title></titles></root>",
            },
            {
                "title": "eLife assessment",
                "expected": b"<root><titles><title>"
                b"eLife assessment: Main article title"
                b"</title></titles></root>",
            },
            {
                "title": "Reviewer #1 (Public Review):",
                "expected": (
                    b"<root><titles><title>"
                    b"Reviewer #1 (Public Review): Main article title"
                    b"</title></titles></root>"
                ),
            },
        ]
        for data in passes:
            parent = Element("root")
            article = Article()
            article.title = "Main article title"
            review_article = Article()
            review_article.title = data.get("title")
            crossref_config = create_crossref_config("elife")
            # invoke
            peer_review.set_title(parent, review_article, article, crossref_config)
            # assert
            parent_string = ElementTree.tostring(parent, "utf-8")
            self.assertEqual(
                parent_string,
                data.get("expected"),
                "failed on title %s" % data.get("title"),
            )
