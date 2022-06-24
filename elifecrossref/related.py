from xml.etree.ElementTree import SubElement


def do_citation_related_item(ref):
    """decide whether to create a related_item for a citation"""
    if ref.publication_type and ref.publication_type == "data":
        return bool(ref.doi or ref.accession or ref.pmid or ref.uri)
    return False


def do_dataset_related_item(dataset):
    """decide whether to create a related_item for a dataset"""
    return bool(dataset.accession_id or dataset.doi or dataset.uri)


def do_preprint_related_item(poa_article):
    """decide whether to create a related_item for a preprint"""
    return bool(
        hasattr(poa_article, "preprint")
        and poa_article.preprint
        and (poa_article.preprint.uri or poa_article.preprint.doi)
    )


def do_relations_program(poa_article):
    """call at a specific moment during generation to set this tag if required"""
    do_relations = None
    for dataset in poa_article.datasets:
        if do_dataset_related_item(dataset) is True:
            do_relations = True
            break
    if do_relations is not True and poa_article.ref_list:
        for ref in poa_article.ref_list:
            if do_citation_related_item(ref) is True:
                do_relations = True
                break
    if do_relations is not True and do_preprint_related_item(poa_article):
        do_relations = True
    return do_relations


def set_relations_program(parent, relations_program_tag):
    """set the relations program parent tag only once"""
    if relations_program_tag is None:
        relations_program_tag = SubElement(parent, "rel:program")
    return relations_program_tag


def set_related_item_description(parent, description):
    if description:
        description_tag = SubElement(parent, "rel:description")
        description_tag.text = description


def set_related_item_work_relation(
    parent, related_item_type, relationship_type, identifier_type, related_item_text
):
    # only supporting inter_work_relation for now
    if related_item_type in ["intra_work_relation", "inter_work_relation"]:
        work_relation_tag = SubElement(parent, "rel:%s" % related_item_type)
        work_relation_tag.set("identifier-type", identifier_type)
        work_relation_tag.set("relationship-type", relationship_type)
        work_relation_tag.text = related_item_text
