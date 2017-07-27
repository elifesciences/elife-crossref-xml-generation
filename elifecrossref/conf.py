import configparser as configparser
import json

config = configparser.ConfigParser(interpolation=None)
config.read('crossref.cfg')

def parse_raw_config(raw_config):
    "parse the raw config to something good"
    crossref_config = {}
    boolean_values = []
    int_values = []
    list_values = []

    boolean_values.append("crossmark")
    int_values.append("year_of_first_volume")
    list_values.append("contrib_types")
    list_values.append("archive_locations")

    for value_name in raw_config:
        if value_name in boolean_values:
            crossref_config[value_name] = raw_config.getboolean(value_name)
        elif value_name in int_values:
            crossref_config[value_name] = raw_config.getint(value_name)
        elif value_name in list_values:
            crossref_config[value_name] = json.loads(raw_config.get(value_name))
        else:
            # default
            crossref_config[value_name] = raw_config.get(value_name)
    return crossref_config
