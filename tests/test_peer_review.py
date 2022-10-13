import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article
from elifecrossref import peer_review


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
