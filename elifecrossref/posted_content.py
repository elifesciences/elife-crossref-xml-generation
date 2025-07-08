from xml.etree.ElementTree import SubElement
from elifecrossref import (
    abstract,
    access_indicators,
    citation,
    collection,
    contributor,
    dates,
    doi,
    related,
    status,
    title,
    version,
)

# description tag text for a retracted article
WITHDRAWN_DESCRIPTION = "This article is retracted."


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

    # status tag for a retracted article
    if poa_article.get_date("retracted"):
        status.set_status_tag(
            posted_content_tag,
            "withdrawn",
            poa_article.get_date("retracted").date,
            WITHDRAWN_DESCRIPTION,
        )

    # item_number
    if poa_article.elocation_id:
        item_number_tag = SubElement(posted_content_tag, "item_number")
        item_number_tag.set("item_number_type", "article_number")
        item_number_tag.text = poa_article.elocation_id

    # abstract
    abstract.set_abstract(posted_content_tag, poa_article, crossref_config)

    # ai:program license
    if poa_article.license and poa_article.license.href:
        ai_program_tag = access_indicators.set_ai_program(posted_content_tag)
        access_indicators.set_ai_license_ref(ai_program_tag, poa_article.license.href)

    relations_program_tag = None
    # rel:program related_item tags for preprint versions
    if poa_article.publication_history:
        relations_program_tag = related.set_relations_program(
            posted_content_tag, relations_program_tag
        )
        for event in poa_article.publication_history:
            related_item_tag = SubElement(relations_program_tag, "rel:related_item")
            related_item_type = "intra_work_relation"
            relationship_type = "isVersionOf"
            if event.doi:
                identifier_type = "doi"
                related_item_text = event.doi
            elif event.uri:
                identifier_type = "uri"
                related_item_text = event.uri
            related.set_related_item_work_relation(
                related_item_tag,
                related_item_type,
                relationship_type,
                identifier_type,
                related_item_text,
            )

    if poa_article.version:
        version.set_version_info(posted_content_tag, poa_article)

    doi_data_tag = doi.set_doi_data(
        posted_content_tag,
        poa_article,
        poa_article,
        crossref_config,
        pattern_type="doi_pattern",
    )

    collection.set_collection(
        doi_data_tag, poa_article, "crawler-based", crossref_config
    )

    if related.do_relations_program(poa_article) is True:
        relations_program_tag = related.set_relations_program(
            posted_content_tag, relations_program_tag
        )
    citation.set_citation_list(
        posted_content_tag, poa_article, relations_program_tag, crossref_config
    )
