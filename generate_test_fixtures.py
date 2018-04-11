from elifecrossref import generate
import time

if __name__ == '__main__':
    default_pub_date = time.strptime("2017-07-17 07:17:07", "%Y-%m-%d %H:%M:%S")
    xml_files = []
    xml_files.append(['tests/test_data/elife-00666.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife_poa_e02725.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-02020-v1.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-02043-v2.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-02935-v2.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-04637-v2.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-08206-v3.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-12444-v2.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-15743-v1.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-16988-v1.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-11134-v2.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/elife-00508-v1.xml', 'elife', default_pub_date, False])
    xml_files.append(['tests/test_data/cstp77-jats.xml', 'cstp', default_pub_date, False])
    xml_files.append(['tests/test_data/bmjopen-4-e003269.xml', 'bmjopen', default_pub_date, False])
    xml_files.append(['tests/test_data/up-sta-example.xml', None, default_pub_date, False])
    for xml_file, config_section, pub_date, add_comment in xml_files:
        generate.TMP_DIR = 'tests/test_data'
        articles = generate.build_articles_for_crossref([xml_file])
        generate.crossref_xml_to_disk(articles, config_section, pub_date, add_comment)
