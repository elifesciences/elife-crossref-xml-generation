from xml.etree.ElementTree import SubElement


def set_article_contributors(parent, poa_article, contrib_types=None):
    # First check for any contributors
    if not poa_article.contributors:
        return
    article_contributors = []
    for contributor in poa_article.contributors:
        if contrib_types:
            # Filter by contrib_type if supplied
            if contributor.contrib_type not in contrib_types:
                continue
        article_contributors.append(contributor)
    set_contributors(parent, article_contributors)


def set_contributors(parent, contributors):
    # If contrib_type is None, all contributors will be added regardless of their type
    contributors_tag = SubElement(parent, "contributors")

    # Ready to add to XML
    # Use the natural list order of contributors when setting the first author
    sequence = "first"
    prev_equal_contrib = None
    for contributor in contributors:
        if (sequence == "first" and prev_equal_contrib is False) or (
            sequence == "first"
            and prev_equal_contrib is True
            and not contributor.equal_contrib
        ):
            # Reset sequence value unless the first contributor and
            # next contributor is also equal_contrib
            sequence = "additional"

        set_contributor(contributors_tag, contributor, sequence)

        # set value for the next loop interation
        prev_equal_contrib = contributor.equal_contrib


def set_contributor(parent, contributor, sequence):
    """add tags for a contributor to the parent tag"""
    if contributor.contrib_type == "on-behalf-of":
        contributor_role = "author"
    else:
        contributor_role = contributor.contrib_type

    # Skip contributors with no surname
    if contributor.surname == "" or contributor.surname is None:
        # Most likely a group author
        set_org_contributor(parent, contributor, contributor_role, sequence)

    else:
        set_person_contributor(parent, contributor, contributor_role, sequence)


def set_org_contributor(parent, contributor, contributor_role, sequence):
    if contributor.collab:
        organization_tag = SubElement(parent, "organization")
        organization_tag.text = contributor.collab
        organization_tag.set("contributor_role", contributor_role)
        organization_tag.set("sequence", sequence)


def set_person_contributor(parent, contributor, contributor_role, sequence):
    person_name_tag = set_person_name(parent, contributor, contributor_role, sequence)
    set_affiliations(person_name_tag, contributor)
    set_orcid(person_name_tag, contributor)


def set_person_name(parent, contributor, contributor_role, sequence):
    person_name_tag = SubElement(parent, "person_name")
    person_name_tag.set("contributor_role", contributor_role)
    person_name_tag.set("sequence", sequence)

    if contributor.given_name:
        given_name_tag = SubElement(person_name_tag, "given_name")
        given_name_tag.text = contributor.given_name

    surname_tag = SubElement(person_name_tag, "surname")
    surname_tag.text = contributor.surname

    if contributor.suffix:
        suffix_tag = SubElement(person_name_tag, "suffix")
        suffix_tag.text = contributor.suffix

    return person_name_tag


def set_orcid(parent, contributor):
    if contributor.orcid:
        orcid_tag = SubElement(parent, "ORCID")
        if hasattr(contributor, "orcid_authenticated"):
            if contributor.orcid_authenticated is True:
                orcid_tag.set("authenticated", "true")
            elif contributor.orcid_authenticated is False:
                orcid_tag.set("authenticated", "false")
        orcid_tag.text = contributor.orcid


def set_affiliations(parent, contributor):
    # Crossref schema limits the number of affilations an author can have
    max_affiliations = 5
    non_blank_affiliations = [
        aff for aff in contributor.affiliations if affiliation_name_place(aff)[0]
    ]
    affiliations_to_add = non_blank_affiliations[0:max_affiliations]
    if affiliations_to_add:
        affiliations_tag = SubElement(parent, "affiliations")
    for aff in affiliations_to_add:
        # format name and place tag strings
        text_name, text_place = affiliation_name_place(aff)
        # add tags
        institution_tag = SubElement(affiliations_tag, "institution")
        institution_name_tag = SubElement(institution_tag, "institution_name")
        institution_name_tag.text = text_name
        if hasattr(aff, "ror") and aff.ror:
            institution_id_tag = SubElement(institution_tag, "institution_id")
            institution_id_tag.set("type", "ror")
            institution_id_tag.text = aff.ror
        if text_place:
            institution_place_tag = SubElement(institution_tag, "institution_place")
            institution_place_tag.text = text_place


def affiliation_name_place(aff):
    "from an Affiliation object, set name and place values to be used in institution tags"
    text_name = ", ".join(
        [value for value in [aff.department, aff.institution] if value]
    )
    text_place = ", ".join([value for value in [aff.city, aff.country] if value])
    if not text_name and aff.text:
        text_name = aff.text
    elif not text_name and text_place:
        # use the place value as the name to satisfy fields required in the Crossref schema
        text_name = text_place
        text_place = ""
    return text_name, text_place
