from xml.etree.ElementTree import Element
from elifearticle import utils as eautils
from elifecrossref import tags


def set_titles(parent, title, crossref_config):
    """
    Set the titles and title tags allowing sub tags within title
    """
    root_tag_name = "titles"
    tag_name = "title"
    root_xml_element = Element(root_tag_name)
    # remove unwanted tags
    tag_converted_title = eautils.remove_tag("ext-link", title)
    if crossref_config.get("face_markup") is True:
        tags.add_inline_tag(root_xml_element, tag_name, tag_converted_title)
    else:
        tags.add_clean_tag(root_xml_element, tag_name, tag_converted_title)
    parent.append(root_xml_element)
