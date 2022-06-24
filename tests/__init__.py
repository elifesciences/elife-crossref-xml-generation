import os
import time
from elifecrossref.conf import raw_config, parse_raw_config


TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_DATA_PATH = TEST_BASE_PATH + "test_data" + os.sep
FIXTURES_PATH = TEST_BASE_PATH + "fixtures" + os.sep
DEFAULT_PUB_DATE = time.strptime("2017-07-17 07:17:07", "%Y-%m-%d %H:%M:%S")


def read_file_content(file_name):
    with open(file_name, "rb") as open_file:
        return open_file.read()


def create_crossref_config(config_section="elife"):
    """utility to create the crossref object"""
    raw_config_object = raw_config(config_section)
    return parse_raw_config(raw_config_object)


def replace_namespaces(xml_string):
    "for testing in pre-Python 3.8 the XML tag attributes are in a different order"
    return xml_string.replace(
        b'<doi_batch xmlns="http://www.crossref.org/schema/5.3.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:fr="http://www.crossref.org/fundref.xsd" xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:ct="http://www.crossref.org/clinicaltrials.xsd" xmlns:rel="http://www.crossref.org/relations.xsd" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" version="5.3.1" xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schemas/crossref5.3.1.xsd">',
        b'<doi_batch version="5.3.1" xmlns="http://www.crossref.org/schema/5.3.1" xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:ct="http://www.crossref.org/clinicaltrials.xsd" xmlns:fr="http://www.crossref.org/fundref.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:rel="http://www.crossref.org/relations.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schemas/crossref5.3.1.xsd">',
    )
