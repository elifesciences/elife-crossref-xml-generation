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
        self.passes.append(('elife-02935-v2.xml', 'elife-crossref-02935-20160728134203.xml'))
        self.passes.append(('elife_poa_e02725.xml', 'elife-crossref-02725-20160513174001.xml'))
        self.passes.append(('elife-15743-v1.xml', 'elife-crossref-15743-20160513133358.xml'))
        self.passes.append(('elife-02020-v1.xml', 'elife-crossref-02020-20160728134532.xml'))
        self.passes.append(('elife-08206-v3.xml', 'elife-crossref-08206-20160728134951.xml'))
        self.passes.append(('elife-04637-v2.xml', 'elife-crossref-04637-20160513134549.xml'))
        self.passes.append(('elife-02043-v2.xml', 'elife-crossref-02043-20160728135127.xml'))
        self.passes.append(('elife-16988-v1.xml', 'elife-crossref-16988-20160728133801.xml'))
        self.passes.append(('elife-12444-v2.xml', 'elife-crossref-12444-20160729011053.xml'))
        self.passes.append(('elife-00666.xml', 'elife-crossref-00666-20170320102118.xml'))

    def clean_crossref_xml_for_comparison(self, xml_content):
        # For now running a test on a PoA article ignore the
        # <publication_date media_type="online"> which is set to the date it is generated
        if '<doi_batch_id>elife-crossref-02725' in xml_content:
            xml_content = re.sub(ur'<publication_date media_type="online">.*</publication_date>',
                                 '', xml_content)

        xml_content = re.sub(ur'<!--.*-->', '', xml_content)
        xml_content = re.sub(ur'<doi_batch_id>.*</doi_batch_id>', '', xml_content)
        xml_content = re.sub(ur'<timestamp>.*</timestamp>', '', xml_content)
        return xml_content

    def read_file_content(self, file_name):
        fp = open(file_name, 'rb')
        content = fp.read()
        fp.close()
        return content

    def test_parse(self):
        for (article_xml_file, crossref_xml_file) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = parse.build_articles_from_article_xmls([file_path])
            crossref_xml = generate.build_crossref_xml_for_articles(articles)

            model_crossref_xml = self.read_file_content(TEST_DATA_PATH + crossref_xml_file)

            clean_generated_crossref_xml = self.clean_crossref_xml_for_comparison(crossref_xml)
            clean_model_crossref_xml = self.clean_crossref_xml_for_comparison(model_crossref_xml)

            self.assertEqual(clean_generated_crossref_xml, clean_model_crossref_xml)


if __name__ == '__main__':
    unittest.main()
