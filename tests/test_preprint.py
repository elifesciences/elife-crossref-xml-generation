import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Preprint
from elifecrossref import preprint, related


class TestSetPreprint(unittest.TestCase):
    def test_set_preprint_doi(self):
        doi = "https://doi.org/10.7554/eLife.00666"
        preprint_object = Preprint(doi=doi, uri="https://ignored-value.example.org/")
        parent = Element("root")
        related_tag = related.set_relations_program(parent, None)
        expected_parent = (
            b"<?xml version='1.0' encoding='utf8'?>"
            b"\n<root>"
            b"<rel:program>"
            b"<rel:related_item>"
            b'<rel:intra_work_relation identifier-type="doi" relationship-type="hasPreprint">'
            b"%s</rel:intra_work_relation>"
            b"</rel:related_item>"
            b"</rel:program>"
            b"</root>" % bytes(doi, "utf8")
        )
        preprint.set_preprint(related_tag, preprint_object)
        self.assertEqual(ElementTree.tostring(parent, "utf8"), expected_parent)

    def test_set_preprint_uri(self):
        uri = "https://example.org"
        preprint_object = Preprint(uri=uri)
        parent = Element("root")
        related_tag = related.set_relations_program(parent, None)
        expected_parent = (
            b"<?xml version='1.0' encoding='utf8'?>"
            b"\n<root>"
            b"<rel:program>"
            b"<rel:related_item>"
            b'<rel:intra_work_relation identifier-type="uri" relationship-type="hasPreprint">'
            b"%s</rel:intra_work_relation>"
            b"</rel:related_item>"
            b"</rel:program>"
            b"</root>" % bytes(uri, "utf8")
        )
        preprint.set_preprint(related_tag, preprint_object)
        self.assertEqual(ElementTree.tostring(parent, "utf8"), expected_parent)
