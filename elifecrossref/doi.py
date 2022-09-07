from xml.etree.ElementTree import SubElement
from elifecrossref import collection, resource_url


def set_article_doi_data(parent, poa_article, crossref_config):
    doi_data_tag = set_doi_data(
        parent, poa_article, poa_article, crossref_config, "doi_pattern"
    )
    collection.set_collection(doi_data_tag, poa_article, "text-mining", crossref_config)


def set_doi_data(parent, obj, poa_article, crossref_config, pattern_type=None):
    doi_data_tag = SubElement(parent, "doi_data")

    doi_tag = SubElement(doi_data_tag, "doi")
    doi_tag.text = obj.doi

    resource_tag = SubElement(doi_data_tag, "resource")

    resource = resource_url.generate_resource_url(
        obj, poa_article, crossref_config, pattern_type
    )
    resource_tag.text = resource

    return doi_data_tag
