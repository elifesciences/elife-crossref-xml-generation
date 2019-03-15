from xml.etree.ElementTree import SubElement

def set_contributors(parent, poa_article, contrib_types=None):
    # First check for any contributors
    if not poa_article.contributors:
        return
    # If contrib_type is None, all contributors will be added regardless of their type
    contributors_tag = SubElement(parent, "contributors")

    # Ready to add to XML
    # Use the natural list order of contributors when setting the first author
    sequence = "first"
    for contributor in poa_article.contributors:
        if contrib_types:
            # Filter by contrib_type if supplied
            if contributor.contrib_type not in contrib_types:
                continue

        if contributor.contrib_type == "on-behalf-of":
            contributor_role = "author"
        else:
            contributor_role = contributor.contrib_type

        # Skip contributors with no surname
        if contributor.surname == "" or contributor.surname is None:
            # Most likely a group author
            if contributor.collab:
                organization_tag = SubElement(contributors_tag, "organization")
                organization_tag.text = contributor.collab
                organization_tag.set("contributor_role", contributor_role)
                organization_tag.set("sequence", sequence)

        else:
            person_name_tag = SubElement(contributors_tag, "person_name")

            person_name_tag.set("contributor_role", contributor_role)

            person_name_tag.set("sequence", sequence)

            given_name_tag = SubElement(person_name_tag, "given_name")
            given_name_tag.text = contributor.given_name

            surname_tag = SubElement(person_name_tag, "surname")
            surname_tag.text = contributor.surname

            if contributor.suffix:
                suffix_tag = SubElement(person_name_tag, "suffix")
                suffix_tag.text = contributor.suffix

            if contributor.affiliations:
                # Crossref schema limits the number of affilations an author can have
                max_affiliations = 5
                for aff in contributor.affiliations[0:max_affiliations]:
                    if aff.text and aff.text != '':
                        affiliation_tag = SubElement(person_name_tag, "affiliation")
                        affiliation_tag.text = aff.text

            if contributor.orcid:
                orcid_tag = SubElement(person_name_tag, "ORCID")
                orcid_tag.set("authenticated", "true")
                orcid_tag.text = contributor.orcid

        # Reset sequence value after the first sucessful loop
        sequence = "additional"
