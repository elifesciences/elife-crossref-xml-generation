from xml.etree.ElementTree import SubElement
from elifecrossref import contributor, dates, doi, related, title, access_indicators


def set_peer_review(parent, poa_article, crossref_config):
    for review_article in poa_article.review_articles:
        # Add peer_review for each review
        peer_review_tag = SubElement(parent, "peer_review")
        set_stage(peer_review_tag)
        set_type(peer_review_tag, review_article)

        if review_article.contributors:
            contributor.set_contributors(peer_review_tag, review_article.contributors)

        set_title(peer_review_tag, review_article, poa_article, crossref_config)

        set_review_date(peer_review_tag, review_article.get_date("review_date"))

        # set access indicators
        if review_article.license and review_article.license.href:
            ai_program_tag = access_indicators.set_ai_program(peer_review_tag)
            access_indicators.set_ai_license_ref(
                ai_program_tag, review_article.license.href
            )

        if review_article.related_articles:
            # set the related article DOI to the first of the related_articles doi
            related_article_doi = review_article.related_articles[0].doi
            relations_program_tag = related.set_relations_program(peer_review_tag, None)
            related_item_tag = SubElement(relations_program_tag, "rel:related_item")
            related.set_related_item_work_relation(
                related_item_tag,
                "inter_work_relation",
                "isReviewOf",
                "doi",
                related_article_doi,
            )
            for related_object in review_article.related_objects:
                link_type = related_object.link_type
                if related_object.link_type == "continued-by":
                    link_type = "hasRelatedMaterial"
                related_item_tag = SubElement(relations_program_tag, "rel:related_item")
                related.set_related_item_work_relation(
                    related_item_tag,
                    "inter_work_relation",
                    link_type,
                    "uri",
                    related_object.xlink_href,
                )

        doi.set_doi_data(
            peer_review_tag,
            review_article,
            poa_article,
            crossref_config,
            "peer_review_doi_pattern",
        )


def set_stage(parent):
    parent.set("stage", "pre-publication")


def set_type(parent, review_article):
    if review_article.article_type in [
        "article-commentary",
        "editor-report",
        "decision-letter",
    ]:
        parent.set("type", "editor-report")
    elif review_article.article_type in ["author-comment", "reply"]:
        parent.set("type", "author-comment")


def set_title(parent, review_article, poa_article, crossref_config):
    """concatenate the review and parent article titles"""
    title_value = ": ".join(
        [value for value in [review_article.title, poa_article.title] if value]
    )
    title.set_titles(parent, title_value, crossref_config)


def set_review_date(parent, article_date):
    # article_date is an ArticleDate object
    if article_date:
        date_tag = SubElement(parent, "review_date")
        dates.set_date_detail(date_tag, article_date.date)
