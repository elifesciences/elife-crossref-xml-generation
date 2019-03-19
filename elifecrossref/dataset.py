from xml.etree.ElementTree import SubElement
from elifecrossref import related


def set_dataset_related_item(parent, dataset_object):
    # add related_item tag
    related_item_tag = SubElement(parent, 'rel:related_item')
    related_item_type = "inter_work_relation"
    description = None
    relationship_type = dataset_relationship_type(dataset_object)
    # set the description
    if dataset_object.title:
        description = dataset_object.title
    if description:
        related.set_related_item_description(related_item_tag, description)
    # Now add one inter_work_relation tag in order ot priority
    if dataset_object.doi:
        identifier_type = "doi"
        related_item_text = dataset_object.doi
        related.set_related_item_work_relation(
            related_item_tag, related_item_type, relationship_type,
            identifier_type, related_item_text)
    elif dataset_object.accession_id:
        identifier_type = "accession"
        related_item_text = dataset_object.accession_id
        related.set_related_item_work_relation(
            related_item_tag, related_item_type, relationship_type,
            identifier_type, related_item_text)
    elif dataset_object.uri:
        identifier_type = "uri"
        related_item_text = dataset_object.uri
        related.set_related_item_work_relation(
            related_item_tag, related_item_type, relationship_type,
            identifier_type, related_item_text)


def dataset_relationship_type(dataset_object):
    """relationship_type for the related_item depending on the dataset_type"""
    if dataset_object.dataset_type:
        if dataset_object.dataset_type == "prev_published_datasets":
            return "references"
        elif dataset_object.dataset_type == "datasets":
            return "isSupplementedBy"
    # default if not specified
    return "isSupplementedBy"
