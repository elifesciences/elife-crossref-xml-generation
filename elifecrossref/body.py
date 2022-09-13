from xml.etree.ElementTree import SubElement
from elifecrossref import journal, peer_review, pending_publication, posted_content


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
        elif submission_type == "pending_publication":
            pending_publication.set_pending_publication(
                body_tag, poa_article, crossref_config
            )
        elif submission_type == "posted_content":
            posted_content.set_posted_content(body_tag, poa_article, crossref_config)
