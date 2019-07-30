import time
from elifecrossref import generate
from elifecrossref.conf import raw_config, parse_raw_config


if __name__ == '__main__':
    DEFAULT_PUB_DATE = time.strptime("2017-07-17 07:17:07", "%Y-%m-%d %H:%M:%S")
    XML_FILES = []
    XML_FILES.append(['tests/test_data/elife-00666.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife_poa_e02725.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-02020-v1.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-02043-v2.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-02935-v2.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-04637-v2.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-08206-v3.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-12444-v2.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-15743-v1.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-16988-v1.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-11134-v2.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/elife-00508-v1.xml', 'elife', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/cstp77-jats.xml', 'cstp', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/bmjopen-4-e003269.xml', 'bmjopen', DEFAULT_PUB_DATE, False])
    XML_FILES.append(['tests/test_data/up-sta-example.xml', None, DEFAULT_PUB_DATE, False])
    for xml_file, config_section, pub_date, add_comment in XML_FILES:
        generate.TMP_DIR = 'tests/test_data'
        articles = generate.build_articles_for_crossref([xml_file])
        crossref_config = parse_raw_config(raw_config(config_section))
        generate.crossref_xml_to_disk(
            articles, crossref_config, pub_date, add_comment, "journal", pretty=True, indent="\t")
