import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article, Award, FundingAward
from elifecrossref import funding
from tests import create_crossref_config


class TestDoFunding(unittest.TestCase):
    def test_do_funding(self):
        "test an article with funding"
        # create CrossrefXML object to test
        article = Article("10.7554/eLife.00666", "Test article")
        article.funding_awards = FundingAward()
        # test assertion
        self.assertEqual(funding.do_funding(article), True)

    def test_do_funding_false(self):
        "test and article without funding"
        # create CrossrefXML object to test
        article = Article("10.7554/eLife.00666", "Test article")
        # test assertion
        self.assertEqual(funding.do_funding(article), False)


class TestSetFundref(unittest.TestCase):
    def test_set_fundref(self):
        parent = Element("root")
        article = Article("10.7554/eLife.00666", "Test article")
        award = Award()
        award.award_id = "award_id"
        award.award_id_type = "doi"
        funding_award = FundingAward()
        funding_award.institution_name = "Test Funder"
        funding_award.institution_id = "123456"
        funding_award.id_type = "Fundref"
        funding_award.awards = [award]
        article.funding_awards = [funding_award]
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<fr:program name="fundref">'
            b'<fr:assertion name="fundgroup">'
            b'<fr:assertion name="funder_name">Test Funder</fr:assertion>'
            b'<fr:assertion name="funder_identifier">123456</fr:assertion>'
            b'<fr:assertion name="award_number">award_id</fr:assertion>'
            b"</fr:assertion>"
            b"</fr:program>"
            b"</root>"
        )
        # invoke
        funding.set_fundref(parent, article)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_set_fundref_no_funding(self):
        parent = Element("root")
        article = Article("10.7554/eLife.00666", "Test article")
        expected = b"<?xml version='1.0' encoding='utf8'?>\n" b"<root />"
        # invoke
        funding.set_fundref(parent, article)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)


class TestSetFinanceRelation(unittest.TestCase):
    def test_set_finance_relation(self):
        parent = Element("fr:program")
        parent.set("xmlns:fr", "http://www.crossref.org/fundref.xsd")
        article = Article("10.7554/eLife.00666", "Test article")
        award = Award()
        award.award_id = "award_id"
        award.award_id_type = "doi"
        funding_award = FundingAward()
        funding_award.institution_name = "Test Funder"
        funding_award.institution_id = "123456"
        funding_award.id_type = "Fundref"
        funding_award.awards = [award]
        article.funding_awards = [funding_award]
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b'<fr:program xmlns:fr="http://www.crossref.org/fundref.xsd">'
            b"<rel:related_item>"
            b'<rel:inter_work_relation identifier-type="doi" relationship-type="isFinancedBy">'
            b"award_id"
            b"</rel:inter_work_relation>"
            b"</rel:related_item>"
            b"</fr:program>"
        )
        # invoke
        funding.set_finance_relation(parent, article)
        parent_string = ElementTree.tostring(parent, "utf8")

        self.assertEqual(parent_string, expected)

    def test_set_finance_relation_no_funding(self):
        parent = Element("root")
        article = Article("10.7554/eLife.00666", "Test article")
        expected = b"<?xml version='1.0' encoding='utf8'?>\n" b"<root />"
        # invoke
        funding.set_finance_relation(parent, article)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)
