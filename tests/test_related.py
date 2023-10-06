import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import (
    Article,
    Award,
    Citation,
    Dataset,
    FundingAward,
    Preprint,
)
from elifecrossref import related


class TestDoCitationRelatedItem(unittest.TestCase):
    def test_do_citation_related_item(self):
        citation = Citation()
        citation.publication_type = "data"
        citation.doi = "10.7554/eLife.00666"
        do_result = related.do_citation_related_item(citation)
        self.assertTrue(do_result)

    def test_do_citation_related_item_false(self):
        citation = Citation()
        do_result = related.do_citation_related_item(citation)
        self.assertEqual(do_result, False)


class TestDoDatasetRelatedItem(unittest.TestCase):
    def test_do_dataset_related_item(self):
        dataset = Dataset()
        dataset.accession_id = "something"
        do_result = related.do_dataset_related_item(dataset)
        self.assertTrue(do_result)


class TestDoPreprintRelatedItem(unittest.TestCase):
    def test_do_preprint_related_item(self):
        article = Article()
        article.preprint = Preprint(uri="https://example.org")
        do_result = related.do_preprint_related_item(article)
        self.assertTrue(do_result)


class TestDoRelationsProgram(unittest.TestCase):
    def test_do_relations_program_dataset(self):
        article = Article("10.7554/eLife.00666")
        dataset = Dataset()
        dataset.accession_id = "something"
        article.datasets = [dataset]
        do_result = related.do_relations_program(article)
        self.assertTrue(do_result)

    def test_do_relations_program_citation(self):
        article = Article("10.7554/eLife.00666")
        citation = Citation()
        citation.publication_type = "data"
        citation.doi = "10.7554/eLife.00666"
        article.ref_list = [citation]
        do_result = related.do_relations_program(article)
        self.assertTrue(do_result)

    def test_do_relations_program_preprint(self):
        article = Article("10.7554/eLife.00666")
        article.preprint = Preprint(uri="https://example.org")
        do_result = related.do_relations_program(article)
        self.assertTrue(do_result)

    def test_funding_doi(self):
        "test when an article has a funding DOI"
        article = Article("10.7554/eLife.00666")
        award = Award()
        award.award_id = "award_id"
        award.award_id_type = "doi"
        funding_award = FundingAward()
        funding_award.add_award(award)
        article.funding_awards = [funding_award]
        do_result = related.do_relations_program(article)
        self.assertTrue(do_result)

    def test_no_funding_doi(self):
        "test if article award has no funding DOI"
        article = Article("10.7554/eLife.00666")
        award = Award()
        award.award_id = "award_id"
        funding_award = FundingAward()
        funding_award.add_award(award)
        article.funding_awards = [funding_award]
        do_result = related.do_relations_program(article)
        self.assertEqual(do_result, None)


class TestSetRelationsProgram(unittest.TestCase):
    def test_set_relations_program(self):
        parent = Element("root")
        expected_tag = b"<?xml version='1.0' encoding='utf8'?>\n<rel:program />"
        expected_parent = (
            b"<?xml version='1.0' encoding='utf8'?>\n<root><rel:program /></root>"
        )
        tag = related.set_relations_program(parent, None)
        self.assertEqual(ElementTree.tostring(tag, "utf8"), expected_tag)
        self.assertEqual(ElementTree.tostring(parent, "utf8"), expected_parent)


class TestSetRelatedItemDescription(unittest.TestCase):
    def test_set_related_item_description(self):
        description = "a description"
        parent = Element("root")
        expected_parent = (
            b"<?xml version='1.0' encoding='utf8'?>\n<root>"
            b"<rel:description>%s</rel:description></root>" % bytes(description, "utf8")
        )
        related.set_related_item_description(parent, description)
        self.assertEqual(ElementTree.tostring(parent, "utf8"), expected_parent)


class TestSetRelatedItemWorkRelation(unittest.TestCase):
    def test_set_related_item_work_relation_inter(self):
        related_item_type = "inter_work_relation"
        relationship_type = "references"
        identifier_type = "doi"
        related_item_text = "10.5061/dryad.cv323"
        parent = Element("root")
        expected_parent = (
            b"<?xml version='1.0' encoding='utf8'?>\n<root>"
            b'<rel:%s identifier-type="%s" relationship-type="%s">%s</rel:%s></root>'
            % (
                bytes(related_item_type, "utf8"),
                bytes(identifier_type, "utf8"),
                bytes(relationship_type, "utf8"),
                bytes(related_item_text, "utf8"),
                bytes(related_item_type, "utf8"),
            )
        )
        related.set_related_item_work_relation(
            parent,
            related_item_type,
            relationship_type,
            identifier_type,
            related_item_text,
        )
        self.assertEqual(ElementTree.tostring(parent, "utf8"), expected_parent)
