from xml.etree.ElementTree import SubElement
from elifecrossref import dates, journal, title


def set_pending_publication(parent, poa_article, crossref_config):

    pending_publication_tag = SubElement(parent, "pending_publication")
    publication_tag = SubElement(pending_publication_tag, "publication")
    publication_full_title_tag = SubElement(publication_tag, "full_title")
    publication_full_title_tag.text = crossref_config.get("registrant")

    journal.set_issn_tag(publication_tag, poa_article)

    title.set_titles(pending_publication_tag, poa_article.title, crossref_config)

    dates.set_acceptance_date(pending_publication_tag, poa_article.get_date("accepted"))

    doi_tag = SubElement(pending_publication_tag, "doi")
    doi_tag.text = poa_article.doi
