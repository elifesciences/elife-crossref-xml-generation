import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Article, Award, FundingAward, License
from elifecrossref import crossmark
from tests import create_crossref_config


class TestDoCrossmark(unittest.TestCase):
    def setUp(self):
        self.crossref_config = create_crossref_config()

    def test_do_crossref(self):
        article = Article("10.7554/eLife.00666")
        do_result = crossmark.do_crossmark(article, self.crossref_config)
        self.assertTrue(do_result)

    def test_do_crossref_false(self):
        article = Article("10.7554/eLife.00666")
        self.crossref_config["crossmark"] = False
        do_result = crossmark.do_crossmark(article, self.crossref_config)
        self.assertFalse(do_result)

    def test_do_crossref_no_doi(self):
        article = Article()
        do_result = crossmark.do_crossmark(article, self.crossref_config)
        self.assertFalse(do_result)


class TestSetCrossmark(unittest.TestCase):
    def setUp(self):
        self.crossref_config = create_crossref_config()
        self.article = Article("10.7554/eLife.00666")
        self.parent = Element("journal_article")

    def test_set_crossmark(self):
        expected = (
            "<journal_article>"
            "<crossmark>"
            "<crossmark_policy>10.7554/eLife.00666</crossmark_policy>"
            "<crossmark_domains>"
            "<crossmark_domain>"
            "<domain>elifesciences.org</domain>"
            "</crossmark_domain>"
            "</crossmark_domains>"
            "<crossmark_domain_exclusive>false</crossmark_domain_exclusive>"
            "</crossmark>"
            "</journal_article>"
        )
        crossmark.set_crossmark(self.parent, self.article, self.crossref_config)
        rough_string = ElementTree.tostring(self.parent).decode("utf-8")
        self.assertEqual(rough_string, expected)

    def test_set_crossmark_crossmark_policy(self):
        """test if an explicity crossmark_policy DOI is specified in config"""
        self.crossref_config["crossmark_policy"] = "10.7554/example"
        expected = (
            "<journal_article>"
            "<crossmark>"
            "<crossmark_policy>10.7554/example</crossmark_policy>"
            "<crossmark_domains>"
            "<crossmark_domain>"
            "<domain>elifesciences.org</domain>"
            "</crossmark_domain>"
            "</crossmark_domains>"
            "<crossmark_domain_exclusive>false</crossmark_domain_exclusive>"
            "</crossmark>"
            "</journal_article>"
        )
        crossmark.set_crossmark(self.parent, self.article, self.crossref_config)
        rough_string = ElementTree.tostring(self.parent).decode("utf-8")
        self.assertEqual(rough_string, expected)

    def test_set_crossmark_domain_filter(self):
        """test config with a domain with a filter value"""
        self.crossref_config["crossmark_domains"][0]["filter"] = "foo"
        expected = (
            "<journal_article>"
            "<crossmark>"
            "<crossmark_policy>10.7554/eLife.00666</crossmark_policy>"
            "<crossmark_domains>"
            "<crossmark_domain>"
            "<domain>elifesciences.org</domain>"
            "<filter>foo</filter>"
            "</crossmark_domain>"
            "</crossmark_domains>"
            "<crossmark_domain_exclusive>false</crossmark_domain_exclusive>"
            "</crossmark>"
            "</journal_article>"
        )
        crossmark.set_crossmark(self.parent, self.article, self.crossref_config)
        rough_string = ElementTree.tostring(self.parent).decode("utf-8")
        self.assertEqual(rough_string, expected)


class TestDoCustomMetadata(unittest.TestCase):
    def setUp(self):
        self.crossref_config = create_crossref_config()
        self.article = Article()

    def test_do_custom_metadata(self):
        self.assertFalse(
            crossmark.do_custom_metadata(self.article, self.crossref_config)
        )

    def test_do_custom_metadata_has_funding(self):
        self.article.funding_awards = ["Mock funding award"]
        self.assertTrue(
            crossmark.do_custom_metadata(self.article, self.crossref_config)
        )

    def test_do_custom_metadata_has_access_indicators(self):
        article_license = License()
        article_license.href = "https://example.org"
        self.article.license = article_license
        self.assertTrue(
            crossmark.do_custom_metadata(self.article, self.crossref_config)
        )


class TestSetCustomMetadata(unittest.TestCase):
    def setUp(self):
        self.crossref_config = create_crossref_config()
        self.article = Article()
        article_license = License()
        article_license.href = "https://example.org"
        self.article.license = article_license
        self.parent = Element("crossmark")

    def test_set_custom_metadata_license_only(self):
        expected = (
            "<crossmark>"
            "<custom_metadata>"
            '<ai:program name="AccessIndicators">'
            '<ai:license_ref applies_to="vor">https://example.org</ai:license_ref>'
            '<ai:license_ref applies_to="am">https://example.org</ai:license_ref>'
            '<ai:license_ref applies_to="tdm">https://example.org</ai:license_ref>'
            "</ai:program>"
            "</custom_metadata>"
            "</crossmark>"
        )
        crossmark.set_custom_metadata(self.parent, self.article, self.crossref_config)
        rough_string = ElementTree.tostring(self.parent).decode("utf-8")
        self.assertEqual(rough_string, expected)

    def test_set_custom_metadata_license_funding(self):
        funding_award = FundingAward()
        funding_award.award_group_id = "group_id"
        award_object = Award()
        award_object.award_id = "award_id"
        funding_award.awards = [award_object]
        funding_award.institution_name = "Institution"
        funding_award.institution_id = "institution_id"
        funding_award.principal_award_recipients = ["Recipient One", "Recipient Two"]

        self.article.funding_awards = [funding_award]
        expected = (
            "<crossmark>"
            "<custom_metadata>"
            '<fr:program name="fundref">'
            '<fr:assertion name="fundgroup">'
            '<fr:assertion name="funder_name">Institution</fr:assertion>'
            '<fr:assertion name="funder_identifier">institution_id</fr:assertion>'
            '<fr:assertion name="award_number">award_id</fr:assertion>'
            "</fr:assertion>"
            "</fr:program>"
            '<ai:program name="AccessIndicators">'
            '<ai:license_ref applies_to="vor">https://example.org</ai:license_ref>'
            '<ai:license_ref applies_to="am">https://example.org</ai:license_ref>'
            '<ai:license_ref applies_to="tdm">https://example.org</ai:license_ref>'
            "</ai:program>"
            "</custom_metadata>"
            "</crossmark>"
        )
        crossmark.set_custom_metadata(self.parent, self.article, self.crossref_config)
        rough_string = ElementTree.tostring(self.parent).decode("utf-8")
        self.assertEqual(rough_string, expected)
