import time
from elifearticle.article import (
    Affiliation,
    Article,
    ArticleDate,
    Award,
    Citation,
    Contributor,
    Event,
    FundingAward,
    License,
    Preprint,
    Uri,
)


def build_preprint_article():
    "populate an Article object with lots of test data"
    article = Article("10.7554/eLife.202200001")
    article.article_type = "preprint"
    article.version_doi = "10.7554/eLife.202200001.2"
    article.version = "2"
    article.manuscript = "202200001"
    article.elocation_id = "RP202200001"
    # use self_uri to set the doi resource address
    self_uri = Uri()
    self_uri.xlink_href = "https://example.org/articles/202200001"
    article.self_uri_list = [self_uri]
    # title
    article.title = (
        "Timely sleep coupling: spindle-slow wave synchrony is "
        "linked to early amyloid-β burden and predicts memory decline"
    )
    # abstract
    article.abstract = "<p>An <italic>abstract</italic> x<sup>2</sup>.</p>"
    # review date
    review_date = ArticleDate(
        "posted_date", time.strptime("2022-03-03 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    article.add_date(review_date)
    # license
    licence_object = License()
    licence_object.href = "http://creativecommons.org/licenses/by/4.0/"
    article.license = licence_object
    # group title
    article.group_title = "eLife RP"
    # author contributors
    author_1 = Contributor("author", "First", "Given names")
    author_1.orcid = "https://orcid.org/0000-0000-0000-0000"
    author_1.orcid_authenticated = False
    aff = Affiliation()
    aff.department = "Department"
    aff.institution = "Institution"
    aff.city = "City"
    aff.country = "Country"
    author_1.set_affiliation(aff)
    article.add_contributor(author_1)
    author_2 = Contributor("author", "Second", "Given names")
    author_2.set_affiliation(aff)
    article.add_contributor(author_2)
    # preprint publicaiton history events
    event_object_1 = Event()
    event_object_1.doi = "10.7554/article_version_with_doi"
    event_object_1.event_type = "preprint"
    article.publication_history.append(event_object_1)
    event_object_2 = Event()
    event_object_2.uri = "10.7554/article_version_with_uri"
    event_object_2.event_type = "reviewed-preprint"
    article.publication_history.append(event_object_2)
    # citations
    citation_object = Citation()
    citation_object.article_title = "An article title"
    article.ref_list = [citation_object]
    # funding
    funding_award_object = FundingAward()
    funding_award_object.institution_name = "Example Funding Institution"
    funding_award_object.institution_id = "example_ror_id"
    funding_award_object.institution_id_type = "ror"
    award_object = Award()
    award_object.award_id = "example_award_id"
    award_object.award_id_type = "doi"
    funding_award_object.awards = [award_object]
    article.funding_awards = [funding_award_object]

    return article


def build_preprint_article_version():
    article = build_preprint_article()
    # reset the self_uri values
    article.self_uri_list = []
    return article
