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
        elif collection_property == "crawler-based":
            if do_set_collection_iparadigms(poa_article, crossref_config) is True:
                setting_name = iparadigms_setting_name(poa_article)
                collection_tag = SubElement(parent, "collection")
                collection_tag.set("property", collection_property)
                item_tag = SubElement(collection_tag, "item")
                item_tag.set("crawler", "iParadigms")
                resource_tag = SubElement(item_tag, "resource")
                resource_tag.text = resource_url.generate_resource_url(
                    poa_article, poa_article, crossref_config, setting_name
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


def iparadigms_setting_name(poa_article):
    "return the iParadigms setting name based on the article properties"
    if poa_article.article_type == "preprint":
        return "iparadigms_preprint_pattern"
    elif poa_article.is_poa is True:
        return "iparadigms_poa_pattern"
    elif poa_article.is_poa is False:
        return "iparadigms_vor_pattern"
    return None


def do_set_collection_iparadigms(poa_article, crossref_config):
    "decide whether to add iParadigms crawling tag"
    setting_name = iparadigms_setting_name(poa_article)
    if (
        setting_name
        and crossref_config.get(setting_name)
        and crossref_config.get(setting_name) != ""
    ):
        return True
    return False


def do_set_collection(poa_article, collection_property, crossref_config):
    """decide whether to set collection tags"""
    # only add text and data mining details if the article has a license
    if (
        access_indicators.has_license(poa_article)
        and collection_property == "text-mining"
    ):
        if (
            do_set_collection_text_mining_xml(crossref_config) is True
            or do_set_collection_text_mining_pdf(poa_article, crossref_config) is True
        ):
            return True
    elif collection_property == "crawler-based":
        if do_set_collection_iparadigms(poa_article, crossref_config) is True:
            return True
    return False
