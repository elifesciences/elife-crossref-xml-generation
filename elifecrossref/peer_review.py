from xml.etree.ElementTree import SubElement
from elifecrossref import contributor, dates, doi, related, title


def set_peer_review(parent, poa_article, crossref_config):
    for review_article in poa_article.review_articles:
        # Add peer_review for each review
        peer_review_tag = SubElement(parent, 'peer_review')
        peer_review_tag.set('stage', 'pre-publication')
        peer_review_tag.set('type', review_article.article_type)

        if review_article.contributors:
            contributor.set_contributors(peer_review_tag, review_article.contributors)

        if review_article.title:
            title.set_titles(peer_review_tag, review_article, crossref_config)

        set_review_date(peer_review_tag, review_article.get_date('review_date'))

        if review_article.related_articles:
            # set the related article DOI to the first of the related_articles doi
            related_article_doi = review_article.related_articles[0].doi
            relations_program_tag = related.set_relations_program(peer_review_tag, None)
            related_item_tag = SubElement(relations_program_tag, 'rel:related_item')
            related.set_related_item_work_relation(
                related_item_tag, 'inter_work_relation', 'isReviewOf', 'doi', related_article_doi)

        doi.set_doi_data(peer_review_tag, review_article, crossref_config)


def set_review_date(parent, article_date):
    # article_date is an ArticleDate object
    if article_date:
        date_tag = SubElement(parent, 'review_date')
        dates.set_date_detail(date_tag, article_date.date)