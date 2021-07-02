from xml.etree.ElementTree import SubElement
from elifecrossref import access_indicators, resource_url


def set_collection(parent, poa_article, collection_property, crossref_config):
    if do_set_collection(poa_article, collection_property, crossref_config):
        if collection_property == "text-mining":
            collection_tag = SubElement(parent, "collection")
            collection_tag.set("property", collection_property)
            if do_set_collection_text_mining_pdf(poa_article, crossref_config) is True:
                item_tag = SubElement(collection_tag, "item")
                resource_tag = SubElement(item_tag, "resource")
                resource_tag.set("mime_type", "application/pdf")
                resource_tag.text = resource_url.generate_resource_url(
                    poa_article, poa_article, crossref_config, "text_mining_pdf_pattern"
                )
            if do_set_collection_text_mining_xml(crossref_config) is True:
                item_tag = SubElement(collection_tag, "item")
                resource_tag = SubElement(item_tag, "resource")
                resource_tag.set("mime_type", "application/xml")
                resource_tag.text = resource_url.generate_resource_url(
                    poa_article, poa_article, crossref_config, "text_mining_xml_pattern"
                )


def do_set_collection_text_mining_xml(crossref_config):
    """decide whether to text mining xml resource"""
    if (
        crossref_config.get("text_mining_xml_pattern")
        and crossref_config.get("text_mining_pdf_pattern") != ""
    ):
        return True
    return False


def do_set_collection_text_mining_pdf(poa_article, crossref_config):
    """decide whether to text mining pdf resource"""
    if (
        crossref_config.get("text_mining_pdf_pattern")
        and crossref_config.get("text_mining_pdf_pattern") != ""
        and poa_article.get_self_uri("pdf") is not None
    ):
        return True
    return False


def do_set_collection(poa_article, collection_property, crossref_config):
    """decide whether to set collection tags"""
    # only add text and data mining details if the article has a license
    if not access_indicators.has_license(poa_article):
        return False
    if collection_property == "text-mining":
        if (
            do_set_collection_text_mining_xml(crossref_config) is True
            or do_set_collection_text_mining_pdf(poa_article, crossref_config) is True
        ):
            return True
    return False
