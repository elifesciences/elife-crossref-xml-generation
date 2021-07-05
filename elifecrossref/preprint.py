from xml.etree.ElementTree import Element, SubElement
from elifearticle import utils as eautils
from elifecrossref import related


def set_preprint(parent, preprint):
    """
    add rel:inter_work_relation tag for a preprint
    """
    related_item_tag = SubElement(parent, "rel:related_item")
    related_item_type = "intra_work_relation"
    relationship_type = "hasPreprint"
    if preprint.doi:
        identifier_type = "doi"
        related_item_text = preprint.doi
    elif preprint.uri:
        identifier_type = "uri"
        related_item_text = preprint.uri
    related.set_related_item_work_relation(
        related_item_tag,
        related_item_type,
        relationship_type,
        identifier_type,
        related_item_text,
    )
