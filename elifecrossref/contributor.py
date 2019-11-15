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
    for contributor in contributors:
        set_contributor(contributors_tag, contributor, sequence)

        # Reset sequence value after the first sucessful loop
        sequence = "additional"


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
        orcid_tag.set("authenticated", "true")
        orcid_tag.text = contributor.orcid


def set_affiliations(parent, contributor):
    # Crossref schema limits the number of affilations an author can have
    max_affiliations = 5
    non_blank_affiliations = [aff for aff in contributor.affiliations if aff.text]
    affiliations_to_add = non_blank_affiliations[0:max_affiliations]
    for aff in affiliations_to_add:
        affiliation_tag = SubElement(parent, "affiliation")
        affiliation_tag.text = aff.text
