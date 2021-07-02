from elifetools import utils as etoolsutils
from elifetools import xmlio
from elifearticle import utils as eautils
from elifecrossref import utils


# namespaces for when reparsing XML strings
REPARSING_NAMESPACES = """ xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
 xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" """


def clean_tags(original_string, do_not_clean=None):
    """remove all unwanted inline tags from the string"""
    do_not_clean_tags = do_not_clean if do_not_clean else []
    tag_converted_string = original_string
    for tag in utils.allowed_tags():
        if tag not in do_not_clean_tags:
            # first do exact tag replacements
            if tag.startswith("<") and tag.endswith(">"):
                tag_converted_string = tag_converted_string.replace(tag, "")
            # then replace by fragments for mml tags if present
            if tag.startswith("<") and not tag.endswith(">"):
                tag_fragment = tag.lstrip("</")
                tag_converted_string = eautils.remove_tag(
                    tag_fragment, tag_converted_string
                )
    remove_tags = ["inline-formula"]
    for tag in remove_tags:
        if tag not in do_not_clean_tags:
            tag_converted_string = eautils.remove_tag(tag, tag_converted_string)
    return tag_converted_string


def add_clean_tag(
    parent,
    tag_name,
    original_string,
    namespaces=REPARSING_NAMESPACES,
    attributes=None,
    attributes_text="",
):
    """remove allowed tags and then add a tag the parent"""
    tag_converted_string = clean_tags(original_string)
    tag_converted_string = etoolsutils.escape_ampersand(tag_converted_string)
    tag_converted_string = etoolsutils.escape_unmatched_angle_brackets(
        tag_converted_string
    )
    minidom_tag = xmlio.reparsed_tag(
        tag_name, tag_converted_string, namespaces, attributes_text
    )
    append_tag(parent, minidom_tag, attributes=attributes)


def add_inline_tag(
    parent,
    tag_name,
    original_string,
    namespaces=REPARSING_NAMESPACES,
    attributes=None,
    attributes_text="",
):
    """replace inline tags found in the original_string and then add a tag the parent"""
    tag_converted_string = convert_inline_tags(original_string)
    minidom_tag = xmlio.reparsed_tag(
        tag_name, tag_converted_string, namespaces, attributes_text
    )
    append_tag(parent, minidom_tag, attributes=attributes)


def append_tag(parent, minidom_tag, attributes=None):
    """given final minidom tag and details, append a tag to the parent tag"""
    xmlio.append_minidom_xml_to_elementtree_xml(
        parent, minidom_tag, attributes=attributes, child_attributes=True
    )


def convert_inline_tags(original_string):
    tag_converted_string = etoolsutils.escape_ampersand(original_string)
    tag_converted_string = etoolsutils.escape_unmatched_angle_brackets(
        tag_converted_string, utils.allowed_tags()
    )
    tag_converted_string = eautils.replace_tags(tag_converted_string, "italic", "i")
    tag_converted_string = eautils.replace_tags(tag_converted_string, "bold", "b")
    tag_converted_string = eautils.replace_tags(tag_converted_string, "underline", "u")
    return tag_converted_string
