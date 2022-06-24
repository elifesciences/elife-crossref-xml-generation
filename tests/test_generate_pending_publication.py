import unittest
import os
import sys
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


class TestGeneratePeerReview(unittest.TestCase):
    def setUp(self):
        self.passes = []
        self.passes.append(
            (
                "elife-00666.xml",
                "elife-crossref-pending_publication-00666-20170717071707.xml",
                "elife",
                DEFAULT_PUB_DATE,
            )
        )

    def test_generate_pending_publication(self):
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
            crossref_xml = generate.crossref_xml(
                articles,
                crossref_config,
                pub_date,
                False,
                "pending_publication",
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
