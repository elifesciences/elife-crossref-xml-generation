import unittest
import os
import sys
from xml.etree.ElementTree import Comment
from elifecrossref import generate
from tests import (
    DEFAULT_PUB_DATE,
    TEST_BASE_PATH,
    TEST_DATA_PATH,
    read_file_content,
    create_crossref_config,
    replace_namespaces,
)


generate.TMP_DIR = TEST_BASE_PATH + "tmp" + os.sep


def contributor_orcid_authenticated(article, orcid_authenticated):
    "set the orcid_authenticated attribute of contributor objects in the article"
    for contributor in article.contributors:
        if hasattr(contributor, "orcid_authenticated"):
            contributor.orcid_authenticated = orcid_authenticated
    return article


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.passes = []
        self.passes.append(
            (
                "elife-02935-v2.xml",
                "elife-crossref-02935-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife_poa_e02725.xml",
                "elife-crossref-02725-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-15743-v1.xml",
                "elife-crossref-15743-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-02020-v1.xml",
                "elife-crossref-02020-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-08206-v3.xml",
                "elife-crossref-08206-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-04637-v2.xml",
                "elife-crossref-04637-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-02043-v2.xml",
                "elife-crossref-02043-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-16988-v1.xml",
                "elife-crossref-16988-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-12444-v2.xml",
                "elife-crossref-12444-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-00666.xml",
                "elife-crossref-00666-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-11134-v2.xml",
                "elife-crossref-11134-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "elife-00508-v1.xml",
                "elife-crossref-00508-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "cstp77-jats.xml",
                "cstp-crossref-77-20170717071707.xml",
                "cstp",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "bmjopen-4-e003269.xml",
                "crossref-bmjopen-2013-003269-20170717071707.xml",
                "bmjopen",
                DEFAULT_PUB_DATE,
            )
        )
        self.passes.append(
            (
                "up-sta-example.xml",
                "crossref-606-20170717071707.xml",
                None,
                DEFAULT_PUB_DATE,
            )
        )

    def test_generate(self):
        for (
            article_xml_file,
            crossref_xml_file,
            config_section,
            pub_date,
        ) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = generate.build_articles_for_crossref([file_path])
            crossref_config = None
            if config_section:
                crossref_config = create_crossref_config(config_section)
                # set orcid_authenticated values for elife articles for this test
                if config_section == "elife":
                    for i, article in enumerate(articles):
                        articles[i] = contributor_orcid_authenticated(article, True)
            # generate pretty XML
            crossref_xml = generate.crossref_xml(
                articles, crossref_config, pub_date, False, pretty=True, indent="\t"
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

    def test_parse_do_no_pass_pub_date(self):
        """
        For test coverage build a crossrefXML object without passing in a pub_date
        """
        article_xml_file = "elife_poa_e02725.xml"
        file_path = TEST_DATA_PATH + article_xml_file
        articles = generate.build_articles_for_crossref([file_path])
        crossref_config = create_crossref_config("elife")
        crossref_object = generate.CrossrefXML(articles, crossref_config, None, True)
        self.assertIsNotNone(crossref_object.pub_date)
        self.assertIsNotNone(crossref_object.generated)
        self.assertIsNotNone(
            [tag for tag in crossref_object.root.iter() if tag is Comment]
        )
        self.assertIsNotNone(crossref_object.output_xml())

    def test_generate_jats_abstract_face_markup(self):
        """
        For coverage test JATS and inline output by overriding the config
        """
        article_xml_file = "elife-16988-v1.xml"
        file_path = TEST_DATA_PATH + article_xml_file
        articles = generate.build_articles_for_crossref([file_path])
        crossref_config = create_crossref_config("elife")
        # override config values
        crossref_config["jats_abstract"] = True
        crossref_config["face_markup"] = True
        # create the Crossref XML
        crossref_object = generate.CrossrefXML(articles, crossref_config, None, True)
        # Check for some tags we expect to find in the output
        self.assertTrue("<jats:italic>" in crossref_object.output_xml())
        self.assertTrue("</b>" in crossref_object.output_xml())

    def test_crossref_xml_to_disk(self):
        """test writing to disk for test coverage and also not pass crossref_config"""
        article_xml_file = "up-sta-example.xml"
        crossref_xml_file = "crossref-606-20170717071707.xml"
        crossref_config = None
        pub_date = DEFAULT_PUB_DATE
        file_path = TEST_DATA_PATH + article_xml_file
        # build the article object
        articles = generate.build_articles_for_crossref([file_path])
        # generate and write to disk
        generate.crossref_xml_to_disk(
            articles,
            crossref_config,
            pub_date,
            False,
            "journal",
            pretty=True,
            indent="\t",
        )
        # check the output matches
        expected_output = read_file_content(TEST_DATA_PATH + crossref_xml_file)
        if sys.version_info < (3, 8):
            # pre Python 3.8 tag attributes are in a different order
            expected_output = replace_namespaces(expected_output)
        generated_output = read_file_content(generate.TMP_DIR + crossref_xml_file)
        self.assertEqual(generated_output, expected_output)
