from xml.etree.ElementTree import SubElement
from elifecrossref import related

# order matters when choosing the identifier
IDENTIFIER_NAMES = ["doi", "accession_id", "uri"]

IDENTIFIER_MAP = {"doi": "doi", "accession_id": "accession", "uri": "uri"}


def set_datasets(relations_program_tag, poa_article):
    """
    Add related_item tags for each dataset
    """
    for dataset_object in poa_article.datasets:
        # Check for at least one identifier before adding the related_item
        if not related.do_dataset_related_item(dataset_object):
            continue
        set_dataset_related_item(relations_program_tag, dataset_object)


def set_dataset_related_item(parent, dataset_object):
    # add related_item tag
    related_item_tag = SubElement(parent, "rel:related_item")
    related_item_type = "inter_work_relation"
    description = None
    relationship_type = dataset_relationship_type(dataset_object)
    # set the description
    if dataset_object.title:
        description = dataset_object.title
    if description:
        related.set_related_item_description(related_item_tag, description)
    # Now add one inter_work_relation tag in order of priority
    identifier_attr_name = choose_dataset_identifier(dataset_object)
    if identifier_attr_name:
        identifier_type = IDENTIFIER_MAP.get(identifier_attr_name)
        related_item_text = getattr(dataset_object, identifier_attr_name)
        related.set_related_item_work_relation(
            related_item_tag,
            related_item_type,
            relationship_type,
            identifier_type,
            related_item_text,
        )


def choose_dataset_identifier(d_obj):
    """return the name of the first non blank attribute"""
    for attr_name in IDENTIFIER_NAMES:
        if hasattr(d_obj, attr_name) and getattr(d_obj, attr_name):
            return attr_name
    return None


def dataset_relationship_type(dataset_object):
    """relationship_type for the related_item depending on the dataset_type"""
    if dataset_object.dataset_type:
        if dataset_object.dataset_type == "prev_published_datasets":
            return "references"
        if dataset_object.dataset_type == "datasets":
            return "isSupplementedBy"
    # default if not specified
    return "isSupplementedBy"
