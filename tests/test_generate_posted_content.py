import unittest
import time
import sys
from elifearticle.article import (
    Article,
    ArticleDate,
    Uri,
)
from elifecrossref import generate
from tests import (
    DEFAULT_PUB_DATE,
    TEST_DATA_PATH,
    helpers,
    read_file_content,
    create_crossref_config,
    replace_namespaces,
)


class TestGeneratePostedContentMinimal(unittest.TestCase):
    def test_generate_minimal(self):
        "minimal data to generate a posted_content deposit"
        article = Article("10.7554/eLife.202200002")
        article.manuscript = "202200002"
        article.article_type = "preprint"
        # use self_uri to set the doi resource address
        self_uri = Uri()
        self_uri.xlink_href = "https://example.org/articles/202200002"
        article.self_uri_list = [self_uri]
        # title
        article.title = (
            "Timely sleep coupling: spindle-slow wave synchrony is "
            "linked to early amyloid-β burden and predicts memory decline"
        )
        # review date
        review_date = ArticleDate(
            "posted_date", time.strptime("2022-03-03 00:00:00", "%Y-%m-%d %H:%M:%S")
        )
        article.add_date(review_date)

        crossref_xml_file = (
            "elife-crossref-preprint-posted_content-202200002-20170717071707.xml"
        )
        config_section = "elife_preprint"
        pub_date = DEFAULT_PUB_DATE

        if config_section:
            crossref_config = create_crossref_config(config_section)
        articles = [article]
        crossref_xml = generate.crossref_xml(
            articles,
            crossref_config,
            pub_date,
            False,
            "posted_content",
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


class TestGeneratePostedContent(unittest.TestCase):
    def setUp(self):
        article = helpers.build_preprint_article()
        # add the test to the passing test list
        self.passes = []
        self.passes.append(
            (
                [article],
                "elife-crossref-preprint-posted_content-202200001-20170717071707.xml",
                "elife_preprint",
                DEFAULT_PUB_DATE,
            )
        )

    def test_generate_posted_content(self):
        for (
            articles,
            crossref_xml_file,
            config_section,
            pub_date,
        ) in self.passes:
            crossref_config = None
            if config_section:
                crossref_config = create_crossref_config(config_section)
                crossref_config["jats_abstract"] = True
            crossref_xml = generate.crossref_xml(
                articles,
                crossref_config,
                pub_date,
                False,
                "posted_content",
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
