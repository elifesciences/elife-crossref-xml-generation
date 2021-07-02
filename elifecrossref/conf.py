import configparser
import json

CONFIG_FILE = "crossref.cfg"


def load_config(config_file=None):
    if not config_file:
        config_file = CONFIG_FILE
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_file)
    return config


def raw_config(config_section, config_file=None):
    """try to load the config section"""
    if not config_file:
        config_file = CONFIG_FILE
    config = load_config(config_file)
    if config.has_section(config_section):
        return config[config_section]
    # default
    return config["DEFAULT"]


def parse_raw_config(raw_config_object):
    """parse the raw config to something good"""
    crossref_config = {}
    boolean_values = []
    int_values = []
    list_values = []

    boolean_values.append("jats_abstract")
    boolean_values.append("face_markup")
    boolean_values.append("crossmark")
    boolean_values.append("elocation_id")
    boolean_values.append("elife_style_component_doi")
    int_values.append("year_of_first_volume")
    list_values.append("contrib_types")
    list_values.append("archive_locations")
    list_values.append("access_indicators_applies_to")
    list_values.append("pub_date_types")
    list_values.append("component_exclude_types")
    list_values.append("crossmark_domains")
    list_values.append("assertion_display_channel_types")

    for value_name in raw_config_object:
        if value_name in boolean_values:
            crossref_config[value_name] = raw_config_object.getboolean(value_name)
        elif value_name in int_values:
            crossref_config[value_name] = raw_config_object.getint(value_name)
        elif value_name in list_values:
            crossref_config[value_name] = json.loads(raw_config_object.get(value_name))
        else:
            # default
            crossref_config[value_name] = raw_config_object.get(value_name)
    return crossref_config
