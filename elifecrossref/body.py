from xml.etree.ElementTree import SubElement
from elifecrossref import journal, peer_review


def set_body(parent, poa_articles, crossref_config, default_pub_date, submission_type):
    body_tag = SubElement(parent, "body")

    for poa_article in poa_articles:
        if submission_type == "journal":
            # Create a new journal record for each article
            journal.set_journal(
                body_tag, poa_article, crossref_config, default_pub_date
            )
        elif submission_type == "peer_review":
            peer_review.set_peer_review(body_tag, poa_article, crossref_config)
