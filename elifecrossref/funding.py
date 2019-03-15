from xml.etree.ElementTree import SubElement


def set_fundref(parent, poa_article):
    """
    Set the fundref data from the article funding_awards list
    """
    if poa_article.funding_awards:
        fr_program_tag = SubElement(parent, 'fr:program')
        fr_program_tag.set("name", "fundref")
        for award in poa_article.funding_awards:
            fr_fundgroup_tag = SubElement(fr_program_tag, 'fr:assertion')
            fr_fundgroup_tag.set("name", "fundgroup")

            if award.get_funder_name():
                fr_funder_name_tag = SubElement(fr_fundgroup_tag, 'fr:assertion')
                fr_funder_name_tag.set("name", "funder_name")
                fr_funder_name_tag.text = award.get_funder_name()

            if award.get_funder_name() and award.institution_id:
                fr_funder_identifier_tag = SubElement(fr_funder_name_tag, 'fr:assertion')
                fr_funder_identifier_tag.set("name", "funder_identifier")
                fr_funder_identifier_tag.text = award.institution_id

            for award_id in award.award_ids:
                fr_award_number_tag = SubElement(fr_fundgroup_tag, 'fr:assertion')
                fr_award_number_tag.set("name", "award_number")
                fr_award_number_tag.text = award_id
