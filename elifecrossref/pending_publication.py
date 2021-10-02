from xml.etree.ElementTree import SubElement
from elifecrossref import dates, journal


def set_pending_publication(parent, poa_article, crossref_config):

    pending_publication_tag = SubElement(parent, "pending_publication")
    publication_tag = SubElement(pending_publication_tag, "publication")
    publication_full_title_tag = SubElement(publication_tag, "full_title")
    publication_full_title_tag.text = crossref_config.get("registrant")

    journal.set_issn_tag(publication_tag, poa_article)

    set_acceptance_date(pending_publication_tag, poa_article.get_date("accepted"))

    doi_tag = SubElement(pending_publication_tag, "doi")
    doi_tag.text = poa_article.doi


def set_acceptance_date(parent, article_date):
    # article_date is an ArticleDate object
    if article_date:
        date_tag = SubElement(parent, "acceptance_date")
        dates.set_date_detail(date_tag, article_date.date)
