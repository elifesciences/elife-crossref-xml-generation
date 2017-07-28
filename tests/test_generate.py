import unittest
import time
import os
import re
from elifecrossref import generate
from elifearticle import parse
from elifecrossref.conf import config

TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_DATA_PATH = TEST_BASE_PATH + "test_data" + os.sep
generate.TMP_DIR = TEST_BASE_PATH + "tmp" + os.sep

class TestGenerate(unittest.TestCase):

    def setUp(self):
        self.passes = []
        default_pub_date = time.strptime("2017-07-17 07:17:07", "%Y-%m-%d %H:%M:%S")
        self.passes.append(('elife-02935-v2.xml', 'elife-crossref-02935-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife_poa_e02725.xml', 'elife-crossref-02725-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-15743-v1.xml', 'elife-crossref-15743-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-02020-v1.xml', 'elife-crossref-02020-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-08206-v3.xml', 'elife-crossref-08206-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-04637-v2.xml', 'elife-crossref-04637-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-02043-v2.xml', 'elife-crossref-02043-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-16988-v1.xml', 'elife-crossref-16988-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-12444-v2.xml', 'elife-crossref-12444-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-00666.xml', 'elife-crossref-00666-20170717071707.xml', 'elife', default_pub_date))
        self.passes.append(('elife-11134-v2.xml', 'elife-crossref-11134-20170717071707.xml', 'elife', default_pub_date))

    def read_file_content(self, file_name):
        fp = open(file_name, 'rb')
        content = fp.read()
        fp.close()
        return content

    def test_parse(self):
        for (article_xml_file, crossref_xml_file, config_section, pub_date) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = parse.build_articles_from_article_xmls([file_path])
            crossref_xml = generate.build_crossref_xml_for_articles(articles, config_section, pub_date, False)
            model_crossref_xml = self.read_file_content(TEST_DATA_PATH + crossref_xml_file)
            self.assertEqual(crossref_xml, model_crossref_xml)

    def test_parse_do_no_pass_pub_date(self):
        # For test coverage build a crossrefXML object without passing in a pub_date
        article_xml_file = 'elife_poa_e02725.xml'
        file_path = TEST_DATA_PATH + article_xml_file
        articles = parse.build_articles_from_article_xmls([file_path])
        crossref_config = config['elife']
        crossref_object = generate.crossrefXML(articles, crossref_config, None, True)
        self.assertIsNotNone(crossref_object.pub_date)
        self.assertIsNotNone(crossref_object.generated)
        self.assertIsNotNone(crossref_object.last_commit)
        self.assertIsNotNone(crossref_object.comment)

if __name__ == '__main__':
    unittest.main()
