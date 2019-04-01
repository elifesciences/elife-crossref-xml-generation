import os


TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_DATA_PATH = TEST_BASE_PATH + "test_data" + os.sep


def read_file_content(file_name):
    with open(file_name, 'rb') as open_file:
        return open_file.read()
