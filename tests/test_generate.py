import unittest
import time
import os
import re
from elifecrossref import generate
from elifearticle import parse

TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_DATA_PATH = TEST_BASE_PATH + "test_data" + os.sep
generate.TMP_DIR = TEST_BASE_PATH + "tmp" + os.sep

class TestGenerate(unittest.TestCase):

    def setUp(self):
        self.passes = []
        default_pub_date = time.gmtime(1500275827)
        self.passes.append(('elife-02935-v2.xml', 'elife-crossref-02935-20170717071707.xml', default_pub_date))
        self.passes.append(('elife_poa_e02725.xml', 'elife-crossref-02725-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-15743-v1.xml', 'elife-crossref-15743-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-02020-v1.xml', 'elife-crossref-02020-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-08206-v3.xml', 'elife-crossref-08206-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-04637-v2.xml', 'elife-crossref-04637-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-02043-v2.xml', 'elife-crossref-02043-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-16988-v1.xml', 'elife-crossref-16988-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-12444-v2.xml', 'elife-crossref-12444-20170717071707.xml', default_pub_date))
        self.passes.append(('elife-00666.xml', 'elife-crossref-00666-20170717071707.xml', default_pub_date))

    def clean_crossref_xml_for_comparison(self, xml_content):
        # For now running a test on a PoA article ignore the
        # <publication_date media_type="online"> which is set to the date it is generated

        xml_content = re.sub(ur'<!--.*-->', '', xml_content)
        return xml_content

    def read_file_content(self, file_name):
        fp = open(file_name, 'rb')
        content = fp.read()
        fp.close()
        return content

    def test_parse(self):
        for (article_xml_file, crossref_xml_file, pub_date) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = parse.build_articles_from_article_xmls([file_path])

            crossref_xml = generate.build_crossref_xml_for_articles(articles, pub_date)

            model_crossref_xml = self.read_file_content(TEST_DATA_PATH + crossref_xml_file)

            clean_generated_crossref_xml = self.clean_crossref_xml_for_comparison(crossref_xml)
            clean_model_crossref_xml = self.clean_crossref_xml_for_comparison(model_crossref_xml)

            self.assertEqual(clean_generated_crossref_xml, clean_model_crossref_xml)

    def test_parse_do_no_pass_pub_date(self):
        # For test coverage build a crossrefXML object without passing in a pub_date
        article_xml_file = 'elife_poa_e02725.xml'
        pub_date = None
        file_path = TEST_DATA_PATH + article_xml_file
        articles = parse.build_articles_from_article_xmls([file_path])
        crossref_object = generate.crossrefXML(articles, pub_date)
        self.assertIsNotNone(crossref_object.pub_date)

if __name__ == '__main__':
    unittest.main()
