from xml.dom import minidom
from elifetools import utils as etoolsutils
from elifetools import xmlio
from elifearticle import utils as eautils
from elifecrossref import utils


def clean_tags(original_string, do_not_clean=None):
    """remove all unwanted inline tags from the string"""
    do_not_clean_tags = do_not_clean if do_not_clean else []
    tag_converted_string = original_string
    for tag in utils.allowed_tags():
        if tag not in do_not_clean_tags:
            # first do exact tag replacements
            if tag.startswith('<') and tag.endswith('>'):
                tag_converted_string = tag_converted_string.replace(tag, '')
            # then replace by fragments for mml tags if present
            if tag.startswith('<') and not tag.endswith('>'):
                tag_fragment = tag.lstrip('</')
                tag_converted_string = eautils.remove_tag(tag_fragment, tag_converted_string)
    remove_tags = ['inline-formula']
    for tag in remove_tags:
        if tag not in do_not_clean_tags:
            tag_converted_string = eautils.remove_tag(tag, tag_converted_string)
    return tag_converted_string


def add_clean_tag(parent, tag_name, original_string, reparsing_namespaces=''):
    """remove allowed tags and then add a tag the parent"""
    tag_converted_string = clean_tags(original_string)
    tag_converted_string = etoolsutils.escape_ampersand(tag_converted_string)
    tag_converted_string = etoolsutils.escape_unmatched_angle_brackets(
        tag_converted_string)
    tagged_string = ('<' + tag_name + reparsing_namespaces + '>' +
                     tag_converted_string + '</' + tag_name + '>')
    reparsed = minidom.parseString(tagged_string.encode('utf-8'))
    xmlio.append_minidom_xml_to_elementtree_xml(parent, reparsed)


def add_inline_tag(parent, tag_name, original_string, reparsing_namespaces=''):
    """replace inline tags found in the original_string and then add a tag the parent"""
    tag_converted_string = convert_inline_tags(original_string)
    tagged_string = ('<' + tag_name + reparsing_namespaces + '>' +
                     tag_converted_string + '</' + tag_name + '>')
    reparsed = minidom.parseString(tagged_string.encode('utf-8'))
    xmlio.append_minidom_xml_to_elementtree_xml(parent, reparsed)


def convert_inline_tags(original_string):
    tag_converted_string = etoolsutils.escape_ampersand(original_string)
    tag_converted_string = etoolsutils.escape_unmatched_angle_brackets(
        tag_converted_string, utils.allowed_tags())
    tag_converted_string = eautils.replace_tags(tag_converted_string, 'italic', 'i')
    tag_converted_string = eautils.replace_tags(tag_converted_string, 'bold', 'b')
    tag_converted_string = eautils.replace_tags(tag_converted_string, 'underline', 'u')
    return tag_converted_string
