import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifecrossref import tags


class TestAddCleanTag(unittest.TestCase):
    def test_add_clean_tag(self):
        """test add_clean_tag to check edge cases"""
        root = Element("root")
        # add the element
        tags.add_clean_tag(root, "p", "<test>")
        self.assertEqual(
            ElementTree.tostring(root).decode("utf-8"),
            "<root><p>&lt;test&gt;</p></root>",
        )
        # strange example based on eLife 28716 v2 Figure 2 caption
        root = Element("root")
        tags.add_clean_tag(
            root,
            "subtitle",
            "...polarization, <<italic>p</italic>>, and its variance...",
        )
        self.assertEqual(
            ElementTree.tostring(root).decode("utf-8"),
            "<root><subtitle>...polarization, &lt;p&gt;, and its variance...</subtitle></root>",
        )


if __name__ == "__main__":
    unittest.main()
