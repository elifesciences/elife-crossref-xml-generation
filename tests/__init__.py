import os
from elifecrossref.conf import raw_config, parse_raw_config


TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_DATA_PATH = TEST_BASE_PATH + "test_data" + os.sep


def read_file_content(file_name):
    with open(file_name, 'rb') as open_file:
        return open_file.read()


def create_crossref_config(config_section='elife'):
    """utility to create the crossref object"""
    raw_config_object = raw_config(config_section)
    return parse_raw_config(raw_config_object)
