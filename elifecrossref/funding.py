from xml.etree.ElementTree import SubElement
from elifecrossref import related


def do_funding(poa_article):
    return bool(poa_article.funding_awards)


def set_fundref(parent, poa_article):
    """
    Set the fundref data from the article funding_awards list
    """
    if do_funding(poa_article):
        fr_program_tag = SubElement(parent, "fr:program")
        fr_program_tag.set("name", "fundref")
    for award in poa_article.funding_awards:
        set_funding_award(fr_program_tag, award)


def set_funding_award(parent, award):
    fr_fundgroup_tag = SubElement(parent, "fr:assertion")
    fr_fundgroup_tag.set("name", "fundgroup")
    fr_funder_name_tag = set_funder_name(fr_fundgroup_tag, award)
    if fr_funder_name_tag is not None:
        set_funder_identifier(fr_fundgroup_tag, award)
    set_award_number(fr_fundgroup_tag, award)


def set_funder_name(parent, award):
    fr_funder_name_tag = None
    if award.get_funder_name():
        fr_funder_name_tag = SubElement(parent, "fr:assertion")
        fr_funder_name_tag.set("name", "funder_name")
        fr_funder_name_tag.text = award.get_funder_name()
    return fr_funder_name_tag


def set_funder_identifier(parent, award):
    if award.get_funder_name() and award.institution_id:
        fr_funder_identifier_tag = SubElement(parent, "fr:assertion")
        fr_funder_identifier_tag.set("name", "funder_identifier")
        fr_funder_identifier_tag.text = award.institution_id


def set_award_number(parent, award):
    for award_object in award.awards:
        fr_award_number_tag = SubElement(parent, "fr:assertion")
        fr_award_number_tag.set("name", "award_number")
        fr_award_number_tag.text = award_object.award_id


def set_finance_relation(relations_program_tag, poa_article):
    "create related_item tags for awards with a funding DOI"
    for award in poa_article.funding_awards:
        for award_object in [
            award_object
            for award_object in award.awards
            if award_object.award_id_type == "doi"
        ]:
            set_finance_related_item(
                relations_program_tag,
                "isFinancedBy",
                award_object.award_id_type,
                award_object.award_id,
            )


def set_finance_related_item(
    parent, relationship_type, identifier_type, related_item_text
):
    "add a related_item tag"
    related_item_tag = SubElement(parent, "rel:related_item")
    related_item_type = "inter_work_relation"
    related.set_related_item_work_relation(
        related_item_tag,
        related_item_type,
        relationship_type,
        identifier_type,
        related_item_text,
    )
