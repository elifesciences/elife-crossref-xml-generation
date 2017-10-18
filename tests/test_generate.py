import unittest
import time
import os
import re
from elifecrossref import generate
from elifearticle.article import Article
from elifecrossref.conf import config, parse_raw_config

TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_DATA_PATH = TEST_BASE_PATH + "test_data" + os.sep
generate.TMP_DIR = TEST_BASE_PATH + "tmp" + os.sep

class TestGenerate(unittest.TestCase):

    def setUp(self):
        self.passes = []
        self.default_pub_date = time.strptime("2017-07-17 07:17:07", "%Y-%m-%d %H:%M:%S")
        self.passes.append(('elife-02935-v2.xml', 'elife-crossref-02935-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife_poa_e02725.xml', 'elife-crossref-02725-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-15743-v1.xml', 'elife-crossref-15743-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-02020-v1.xml', 'elife-crossref-02020-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-08206-v3.xml', 'elife-crossref-08206-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-04637-v2.xml', 'elife-crossref-04637-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-02043-v2.xml', 'elife-crossref-02043-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-16988-v1.xml', 'elife-crossref-16988-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-12444-v2.xml', 'elife-crossref-12444-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-00666.xml', 'elife-crossref-00666-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-11134-v2.xml', 'elife-crossref-11134-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('elife-00508-v1.xml', 'elife-crossref-00508-20170717071707.xml', 'elife', self.default_pub_date))
        self.passes.append(('cstp77-jats.xml', 'cstp-crossref-77-20170717071707.xml', 'cstp', self.default_pub_date))
        self.passes.append(('bmjopen-4-e003269.xml', 'crossref-bmjopen-2013-003269-20170717071707.xml', 'bmjopen', self.default_pub_date))

    def read_file_content(self, file_name):
        fp = open(file_name, 'rb')
        content = fp.read()
        fp.close()
        return content

    def test_parse(self):
        for (article_xml_file, crossref_xml_file, config_section, pub_date) in self.passes:
            file_path = TEST_DATA_PATH + article_xml_file
            articles = generate.build_articles_for_crossref([file_path])
            crossref_xml = generate.crossref_xml(articles, config_section, pub_date, False)
            model_crossref_xml = self.read_file_content(TEST_DATA_PATH + crossref_xml_file)
            self.assertEqual(crossref_xml, model_crossref_xml)

    def test_parse_do_no_pass_pub_date(self):
        """
        For test coverage build a crossrefXML object without passing in a pub_date
        and also test pretty output too for coverage
        """
        article_xml_file = 'elife_poa_e02725.xml'
        file_path = TEST_DATA_PATH + article_xml_file
        articles = generate.build_articles_for_crossref([file_path])
        raw_config = config['elife']
        crossref_config = parse_raw_config(raw_config)
        crossref_object = generate.CrossrefXML(articles, crossref_config, None, True)
        self.assertIsNotNone(crossref_object.pub_date)
        self.assertIsNotNone(crossref_object.generated)
        self.assertIsNotNone(crossref_object.last_commit)
        self.assertIsNotNone(crossref_object.comment)
        self.assertIsNotNone(crossref_object.output_xml(pretty=True, indent='\t'))


    def test_generate_jats_abstract_face_markup(self):
        """
        For coverage test JATS and inline output by overriding the config
        """
        article_xml_file = 'elife-16988-v1.xml'
        file_path = TEST_DATA_PATH + article_xml_file
        articles = generate.build_articles_for_crossref([file_path])
        raw_config = config['elife']
        # override config values - need to save the originals first then set them back
        #  so that other tests will pass
        jats_abstract = raw_config.get('jats_abstract')
        face_markup = raw_config.get('face_markup')
        raw_config['jats_abstract'] = 'true'
        raw_config['face_markup'] = 'true'
        crossref_config = parse_raw_config(raw_config)
        # create the Crossref XML
        crossref_object = generate.CrossrefXML(articles, crossref_config, None, True)
        # Check for some tags we expect to find in the output
        self.assertTrue('<jats:italic>' in crossref_object.output_xml())
        self.assertTrue('</b>' in crossref_object.output_xml())
        # now set the config back to normal
        raw_config['jats_abstract'] = jats_abstract
        raw_config['face_markup'] = face_markup


    def test_crossref_xml_to_disk(self):
        "test writing to disk for test coverage"
        article_xml_file = 'elife_poa_e02725.xml'
        crossref_xml_file = 'elife-crossref-02725-20170717071707.xml'
        config_section = 'elife'
        pub_date = self.default_pub_date
        file_path = TEST_DATA_PATH + article_xml_file
        # build the article object
        articles = generate.build_articles_for_crossref([file_path])
        # generate and write to disk
        generate.crossref_xml_to_disk(articles, config_section, pub_date, False)
        # check the output matches
        with open(TEST_DATA_PATH + crossref_xml_file, 'rb') as fp:
            expected_output = fp.read()
        with open(generate.TMP_DIR + crossref_xml_file, 'rb') as fp:
            generated_output = fp.read()
        self.assertEqual(generated_output, expected_output)



if __name__ == '__main__':
    unittest.main()
