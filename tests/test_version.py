import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article
from elifecrossref import version


class TestSetVersionInfo(unittest.TestCase):
    "tests for set_version_info()"

    def test_set_version_info(self):
        "test adding version_info tag and version tag to it"
        parent = Element("root")
        article = Article("10.7554/eLife.202200002")
        article.version = 2
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root><version_info>"
            b'<version xml:lang="en">2</version>'
            b"</version_info>"
            b"</root>"
        )
        version.set_version_info(parent, article)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)
