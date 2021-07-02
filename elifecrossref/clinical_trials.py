from collections import OrderedDict
from xml.etree import ElementTree
from xml.etree.ElementTree import SubElement
import requests


# to convert to Crossref type values they accept
CONTENT_TYPE_MAP = {
    "pre-results": "preResults",
    "preResults": "preResults",
    "results": "results",
    "post-results": "postResults",
    "postResults": "postResults",
}


def do_clinical_trials(poa_article):
    return bool(hasattr(poa_article, "clinical_trials") and poa_article.clinical_trials)


def parse_registries_xml(registries_xml):
    """convert registries XML into a name to doi map"""
    name_to_doi_map = OrderedDict()
    tree = ElementTree.fromstring(registries_xml)
    # simplified namespace name for easier finding
    namespaces = {"xschema": "http://www.crossref.org/xschema/1.1"}
    for component in tree.findall(
        ".//xschema:component_list/xschema:component", namespaces
    ):
        name_tag = component.find(".//xschema:titles/xschema:subtitle", namespaces)
        doi_tag = component.find(".//xschema:doi_data/xschema:doi", namespaces)
        name_to_doi_map[name_tag.text] = doi_tag.text
    return name_to_doi_map


def registry_name_to_doi_map(registry_url):
    """get XML for clinical trials registries and turn into a name to doi map"""
    response = requests.get(registry_url)
    return parse_registries_xml(response.content)


def set_clinical_trials(parent, poa_article, crossref_config):
    if do_clinical_trials(poa_article):
        # get a map of name to registry DOI
        name_to_doi_map = (
            registry_name_to_doi_map(crossref_config.get("clinical_trials_registries"))
            if crossref_config.get("clinical_trials_registries")
            else None
        )
        ai_program_tag = set_ct_program(parent)
        for clinical_trial in poa_article.clinical_trials:
            clinical_trial_number = SubElement(
                ai_program_tag, "ct:clinical-trial-number"
            )
            clinical_trial_number.set(
                "registry", clinical_trial.get_registry_doi(name_to_doi_map)
            )
            if (
                clinical_trial.content_type
                and clinical_trial.content_type in CONTENT_TYPE_MAP
            ):
                clinical_trial_number.set(
                    "type", CONTENT_TYPE_MAP.get(clinical_trial.content_type)
                )
            clinical_trial_number.text = clinical_trial.document_id


def set_ct_program(parent):
    ct_program_tag = SubElement(parent, "ct:program")
    return ct_program_tag
