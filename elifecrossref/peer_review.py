from xml.etree.ElementTree import SubElement
from elifearticle import utils as eautils


def set_peer_review(parent, poa_article, crossref_config, default_pub_date):
    # Add peer_review for each article
    peer_review_tag = SubElement(parent, 'peer_review')
