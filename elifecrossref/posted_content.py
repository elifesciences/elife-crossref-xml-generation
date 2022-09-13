from xml.etree.ElementTree import SubElement
from elifecrossref import (
    abstract,
    access_indicators,
    contributor,
    dates,
    doi,
    related,
    title,
)


def set_posted_content(parent, poa_article, crossref_config):
    "build a Crossref deposit for a posted_content tag"
    posted_content_tag = SubElement(parent, "posted_content")
    posted_content_tag.set("type", "preprint")

    # group_title
    if hasattr(poa_article, "group_title") and poa_article.group_title:
        group_title_tag = SubElement(posted_content_tag, "group_title")
        group_title_tag.text = poa_article.group_title

    # contributors
    contrib_types = ["author"]
    contributor.set_article_contributors(posted_content_tag, poa_article, contrib_types)

    # title is required
    title.set_titles(posted_content_tag, poa_article.title, crossref_config)

    # date is required
    dates.set_posted_date(posted_content_tag, poa_article.get_date("posted_date"))

    # item_number
    if poa_article.elocation_id:
        item_number_tag = SubElement(posted_content_tag, "item_number")
        item_number_tag.set("item_number_type", "article_number")
        item_number_tag.text = poa_article.elocation_id

    # abstract
    abstract.set_abstract(posted_content_tag, poa_article, crossref_config)

    # ai:program license
    access_indicators.set_access_indicators(
        posted_content_tag, poa_article, crossref_config
    )

    # rel:program related_item tags for preprint versions
    if poa_article.related_articles:
        program_tag = related.set_relations_program(posted_content_tag, None)
        for preprint in poa_article.related_articles:
            related_item_tag = SubElement(program_tag, "rel:related_item")
            related_item_type = "intra_work_relation"
            relationship_type = "isVersionOf"
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

    doi.set_doi_data(posted_content_tag, poa_article, poa_article, crossref_config)
