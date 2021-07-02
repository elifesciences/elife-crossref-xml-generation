from xml.etree.ElementTree import SubElement


def do_access_indicators(poa_article, crossref_config):
    return bool(
        crossref_config.get("access_indicators_applies_to") and has_license(poa_article)
    )


def set_access_indicators(parent, poa_article, crossref_config):
    """
    Set the AccessIndicators
    """
    if do_access_indicators(poa_article, crossref_config):
        ai_program_tag = set_ai_program(parent)
        applies_to_list = crossref_config.get("access_indicators_applies_to")
        for applies_to in applies_to_list:
            set_ai_license_ref(ai_program_tag, poa_article.license.href, applies_to)


def has_license(poa_article):
    """check if the article has the minimum requirements of a license"""
    if not poa_article.license:
        return False
    if not poa_article.license.href:
        return False
    return True


def set_ai_program(parent):
    ai_program_tag = SubElement(parent, "ai:program")
    ai_program_tag.set("name", "AccessIndicators")
    return ai_program_tag


def set_ai_license_ref(parent, href, applies_to=None):
    ai_program_ref_tag = SubElement(parent, "ai:license_ref")
    if applies_to:
        ai_program_ref_tag.set("applies_to", applies_to)
    ai_program_ref_tag.text = href
