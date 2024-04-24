import unittest
import time
import os
import sys
from elifearticle.article import (
    Article,
    ArticleDate,
    Contributor,
    License,
    RelatedObject,
)
from elifecrossref import generate
from tests import (
    DEFAULT_PUB_DATE,
    TEST_BASE_PATH,
    TEST_DATA_PATH,
    helpers,
    read_file_content,
    create_crossref_config,
    replace_namespaces,
)


generate.TMP_DIR = TEST_BASE_PATH + "tmp" + os.sep


def sample_data(base_doi="10.7554/eLife.00666"):
    """some sample data for development until real object definition is final and XML is parsed"""
    reviews = []
    # editor's evaluation
    editor_evaluation = Article()
    editor_evaluation.article_type = "editor-report"
    editor_evaluation.id = "sa0"
    article_author = Contributor("author", "Harrison", "Melissa")
    editor_evaluation.contributors.append(article_author)
    article_collab_author = Contributor(
        "author", None, None, "eLife Editorial Production Group"
    )
    editor_evaluation.contributors.append(article_collab_author)
    editor_evaluation.title = "Editor's evaluation"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    editor_evaluation.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    editor_evaluation.license = license_object
    # related article doi
    related_article = Article()
    related_article.doi = base_doi
    related_article.title = "The eLife research article"
    editor_evaluation.related_articles = [related_article]
    # review article doi
    editor_evaluation.doi = "%s.sa0" % base_doi
    # related material with a uri
    related_object = RelatedObject()
    related_object.xlink_href = (
        "https://sciety.org/articles/activity/10.1101/2020.11.21.391326"
    )
    related_object.link_type = "continued-by"
    editor_evaluation.related_objects = [related_object]
    # append it
    reviews.append(editor_evaluation)

    # decision letter
    decision_letter = Article()
    decision_letter.article_type = "decision-letter"
    decision_letter.id = "SA1"
    dec_author = Contributor("editor", "Christian", "Rutz")
    decision_letter.contributors.append(dec_author)
    decision_letter.title = "Decision letter"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    decision_letter.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    decision_letter.license = license_object
    # related article doi
    related_article = Article()
    related_article.doi = base_doi
    related_article.title = "The eLife research article"
    decision_letter.related_articles = [related_article]
    # review article doi
    decision_letter.doi = "%s.029" % base_doi
    # append it
    reviews.append(decision_letter)

    # author response
    author_response = Article()
    author_response.article_type = "author-comment"
    author_response.id = "SA2"
    article_author = Contributor("author", "Harrison", "Melissa")
    author_response.contributors.append(article_author)
    article_collab_author = Contributor(
        "author", None, None, "eLife Editorial Production Group"
    )
    author_response.contributors.append(article_collab_author)
    author_response.title = "Author response"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    author_response.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    author_response.license = license_object
    # related article doi
    related_article = Article()
    related_article.doi = base_doi
    related_article.title = "The eLife research article"
    author_response.related_articles = [related_article]
    # review article doi
    author_response.doi = "%s.030" % base_doi
    # append it
    reviews.append(author_response)

    # anonymous review
    review_article = Article()
    review_article.article_type = "referee-report"
    review_article.id = "SA3"
    article_author = Contributor("author", None, None)
    article_author.anonymous = True
    review_article.contributors.append(article_author)
    review_article.title = "Reviewer #1 (Public Review)"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2018-01-12 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    review_article.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    review_article.license = license_object
    # related article doi
    related_article = Article()
    related_article.doi = base_doi
    related_article.title = "The eLife research article"
    review_article.related_articles = [related_article]
    # review article doi
    review_article.doi = "%s.sa3" % base_doi
    # append it
    reviews.append(review_article)

    return reviews


class TestGeneratePeerReview(unittest.TestCase):
    def setUp(self):
        self.passes = []
        self.passes.append(
            (
                "elife-00666.xml",
                "10.7554/eLife.00666",
                "elife-crossref-peer_review-00666-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-12444-v2.xml",
                "10.7554/eLife.12444",
                "elife-crossref-peer_review-12444-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )

    def test_generate_peer_review(self):
        for (
            article_xml_file,
            base_doi,
            crossref_xml_file,
            config_section,
            pub_date,
        ) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = generate.build_articles_for_crossref([file_path])
            # set some review sample data
            articles[0].review_articles = sample_data(base_doi)
            crossref_config = None
            if config_section:
                crossref_config = create_crossref_config(config_section)
            crossref_xml = generate.crossref_xml(
                articles,
                crossref_config,
                pub_date,
                False,
                "peer_review",
                pretty=True,
                indent="    ",
            )
            model_crossref_xml = read_file_content(TEST_DATA_PATH + crossref_xml_file)
            if sys.version_info < (3, 8):
                # pre Python 3.8 tag attributes are in a different order
                model_crossref_xml = replace_namespaces(model_crossref_xml)
            self.assertEqual(
                crossref_xml,
                model_crossref_xml.decode("utf-8"),
                "Failed parse test on file %s" % article_xml_file,
            )


def preprint_reviews_sample_data():
    "sample data for peer reviews of a preprint"
    reviews = []
    # eLife assessment
    elife_assessment = Article()
    elife_assessment.article_type = "editor-report"
    elife_assessment.id = "sa0"
    article_author = Contributor("author", "Itor", "Ed")
    elife_assessment.contributors.append(article_author)
    elife_assessment.title = "eLife assessment"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2023-05-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    elife_assessment.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    elife_assessment.license = license_object
    # related article
    elife_assessment.related_articles = [helpers.build_preprint_article()]
    # review article doi
    elife_assessment.doi = "10.7554/eLife.202200001.2.sa0"
    # append it
    reviews.append(elife_assessment)

    # public review 1
    public_review_1 = Article()
    public_review_1.article_type = "referee-report"
    public_review_1.id = "sa1"
    reviewer = Contributor("author", None, None)
    reviewer.anonymous = True
    public_review_1.contributors.append(reviewer)
    public_review_1.title = "Reviewer #1 (Public Review)"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2023-05-02 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    public_review_1.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    public_review_1.license = license_object
    # related article
    public_review_1.related_articles = [helpers.build_preprint_article()]
    # review article doi
    public_review_1.doi = "10.7554/eLife.202200001.2.sa1"
    # append it
    reviews.append(public_review_1)

    # public review 2
    public_review_2 = Article()
    public_review_2.article_type = "referee-report"
    public_review_2.id = "sa2"
    reviewer = Contributor("author", None, None)
    reviewer.anonymous = True
    public_review_2.contributors.append(reviewer)
    public_review_2.title = "Reviewer #2 (Public Review)"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2023-05-02 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    public_review_2.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    public_review_2.license = license_object
    # related article
    public_review_2.related_articles = [helpers.build_preprint_article()]
    # review article doi
    public_review_2.doi = "10.7554/eLife.202200001.2.sa2"
    # append it
    reviews.append(public_review_2)

    # public review 3
    public_review_3 = Article()
    public_review_3.article_type = "referee-report"
    public_review_3.id = "sa3"
    reviewer = Contributor("author", None, None)
    reviewer.anonymous = True
    public_review_3.contributors.append(reviewer)
    public_review_3.title = "Reviewer #3 (Public Review)"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2023-05-02 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    public_review_3.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    public_review_3.license = license_object
    # related article
    public_review_3.related_articles = [helpers.build_preprint_article()]
    # review article doi
    public_review_3.doi = "10.7554/eLife.202200001.2.sa3"
    # append it
    reviews.append(public_review_3)

    # author response
    author_response = Article()
    author_response.article_type = "author-comment"
    author_response.id = "sa4"
    article_author = Contributor("author", "Or", "Auth")
    author_response.contributors.append(article_author)
    article_collab_author = Contributor("author", None, None, "Research Group")
    author_response.contributors.append(article_collab_author)
    author_response.title = "Author response"
    # review date
    review_date = ArticleDate(
        "review_date", time.strptime("2023-05-03 00:00:00", "%Y-%m-%d %H:%M:%S")
    )
    author_response.add_date(review_date)
    # license
    license_object = License()
    license_object.href = "http://creativecommons.org/licenses/by/4.0/"
    author_response.license = license_object
    # related article
    author_response.related_articles = [helpers.build_preprint_article()]
    # review article doi
    author_response.doi = "10.7554/eLife.202200001.2.sa4"
    # append it
    reviews.append(author_response)

    return reviews


class TestGeneratePreprintPeerReview(unittest.TestCase):
    def setUp(self):
        self.passes = []
        article = helpers.build_preprint_article()
        self.passes.append(
            (
                [article],
                "elife-crossref-preprint-peer_review-202200001-v2-20170717071707.xml",
                "elife_preprint",
                DEFAULT_PUB_DATE,
            )
        )

    def test_generate_peer_review(self):
        for (
            articles,
            crossref_xml_file,
            config_section,
            pub_date,
        ) in self.passes:
            # set some review sample data
            articles[0].review_articles = preprint_reviews_sample_data()
            crossref_config = None
            if config_section:
                crossref_config = create_crossref_config(config_section)
            crossref_xml = generate.crossref_xml(
                articles,
                crossref_config,
                pub_date,
                False,
                "peer_review",
                pretty=True,
                indent="    ",
            )
            model_crossref_xml = read_file_content(TEST_DATA_PATH + crossref_xml_file)
            if sys.version_info < (3, 8):
                # pre Python 3.8 tag attributes are in a different order
                model_crossref_xml = replace_namespaces(model_crossref_xml)
            self.assertEqual(
                crossref_xml,
                model_crossref_xml.decode("utf-8"),
                "Failed parse test on articles %s"
                % ", ".join([article.doi for article in articles]),
            )
