from xml.etree.ElementTree import SubElement
from elifecrossref import journal


def set_body(parent, poa_articles, crossref_config, default_pub_date):
    body_tag = SubElement(parent, 'body')

    for poa_article in poa_articles:
        # Create a new journal record for each article
        journal.set_journal(body_tag, poa_article, crossref_config, default_pub_date)
