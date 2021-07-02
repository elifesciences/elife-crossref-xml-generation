import os
import unittest
from unittest.mock import patch
from collections import OrderedDict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import requests
from elifearticle.article import Article, ClinicalTrial
from elifecrossref import clinical_trials
from tests import FIXTURES_PATH, read_file_content


class FakeResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code
        self.content = None


class TestDoClinicalTrials(unittest.TestCase):
    def test_do_clinical_trials(self):
        article = Article("10.7554/eLife.00666")
        article.clinical_trials = [ClinicalTrial()]
        do_result = clinical_trials.do_clinical_trials(article)
        self.assertTrue(do_result)


class TestSetClinicalTrials(unittest.TestCase):
    @patch.object(clinical_trials, "registry_name_to_doi_map")
    def test_set_clinical_trials(self, fake_name_map):
        fake_name_map.return_value = OrderedDict(
            [("ClinicalTrials.gov", "10.18810/clinical-trials-gov")]
        )
        parent = Element("custom_metadata")
        article = Article("10.7554/eLife.00666")
        clinical_trial = ClinicalTrial()
        clinical_trial.source_id = "ClinicalTrials.gov"
        clinical_trial.source_id_type = "registry-name"
        clinical_trial.document_id = "TEST999"
        clinical_trial.content_type = "preResults"
        article.clinical_trials = [clinical_trial]
        expected = (
            "<custom_metadata>"
            "<ct:program>"
            '<ct:clinical-trial-number registry="10.18810/clinical-trials-gov" type="preResults">'
            "TEST999"
            "</ct:clinical-trial-number>"
            "</ct:program>"
            "</custom_metadata>"
        )
        clinical_trials.set_clinical_trials(
            parent,
            article,
            {"clinical_trials_registries": "https://doi.org/10.18810/registries"},
        )
        rough_string = ElementTree.tostring(parent).decode("utf-8")
        self.assertEqual(rough_string, expected)

    @patch.object(clinical_trials, "registry_name_to_doi_map")
    def test_set_clinical_trials_edge_case(self, fake_name_map):
        """test edge case of crossref-doi type and alternate content-type value"""
        fake_name_map.return_value = OrderedDict(
            [("ClinicalTrials.gov", "10.18810/clinical-trials-gov")]
        )
        parent = Element("custom_metadata")
        article = Article("10.7554/eLife.00666")
        clinical_trial = ClinicalTrial()
        clinical_trial.source_id = "10.18810/clinical-trials-gov"
        clinical_trial.source_id_type = "crossref-doi"
        clinical_trial.document_id = "TEST999"
        clinical_trial.content_type = "post-results"
        article.clinical_trials = [clinical_trial]
        expected = (
            "<custom_metadata>"
            "<ct:program>"
            '<ct:clinical-trial-number registry="10.18810/clinical-trials-gov" type="postResults">'
            "TEST999"
            "</ct:clinical-trial-number>"
            "</ct:program>"
            "</custom_metadata>"
        )
        clinical_trials.set_clinical_trials(
            parent,
            article,
            {"clinical_trials_registries": "https://doi.org/10.18810/registries"},
        )
        rough_string = ElementTree.tostring(parent).decode("utf-8")
        self.assertEqual(rough_string, expected)


class TestRegistryNameMap(unittest.TestCase):
    @patch.object(requests, "get")
    def test_registry_name_to_doi_map(self, fake_get):
        registries_response = FakeResponse()
        registries_response.content = "<xml />"
        fake_get.return_value = registries_response
        # expected value
        expected = OrderedDict()
        # issue call for the registries XML
        registry_url = "https://example.org"
        name_map = clinical_trials.registry_name_to_doi_map(registry_url)
        # assertions
        self.assertEqual(name_map, expected)


class TestParseRegistriesXml(unittest.TestCase):
    def test_parse_registries_xml(self):
        expected = OrderedDict(
            [
                ("UTN", "10.18810/utn"),
                ("ClinicalTrials.gov", "10.18810/clinical-trials-gov"),
                ("ISRCTN", "10.18810/isrctn"),
                ("ANZCTR", "10.18810/anzctr"),
                ("DRKS", "10.18810/drks"),
                ("ChiCTR", "10.18810/chictr"),
                ("ReBec", "10.18810/rebec"),
                ("NTR", "10.18810/dutch-trial-register"),
                ("CTRI", "10.18810/clinical-trial-registry-india"),
                ("UMIN", "10.18810/umin-japan"),
                ("PACTR", "10.18810/pactr"),
                ("SLCTR", "10.18810/slctr"),
                ("JMACCT", "10.18810/jma"),
                ("IRCT", "10.18810/irct"),
                ("CRiS", "10.18810/cris"),
                ("RPCEC", "10.18810/rpec"),
                ("EU-CTR", "10.18810/euctr"),
                ("JPRN", "10.18810/jprn"),
                ("TCTR", "10.18810/tctr"),
            ]
        )
        name_map = clinical_trials.parse_registries_xml(
            read_file_content(
                os.path.join(FIXTURES_PATH, "clinical_trial_registries.xml")
            )
        )
        self.assertEqual(name_map, expected)
