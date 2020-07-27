import re
from elifearticle import utils as eautils
from elifetools import utils_html
from elifetools import xmlio
from elifetools import utils as etoolsutils
from elifetools.parseJATS import XML_NAMESPACES
from elifecrossref import tags, utils


def set_abstract(parent, poa_article, crossref_config):
    if hasattr(poa_article, 'abstract_xml') and poa_article.abstract_xml:
        set_abstract_tag(parent, abstract=poa_article.abstract_xml, abstract_type="abstract",
                         jats_abstract=crossref_config.get('jats_abstract'))
    elif poa_article.abstract:
        set_abstract_tag(parent, abstract=poa_article.abstract, abstract_type="abstract",
                         jats_abstract=crossref_config.get('jats_abstract'))


def set_digest(parent, poa_article, crossref_config):
    if hasattr(poa_article, 'digest') and poa_article.digest:
        set_abstract_tag(parent, abstract=poa_article.digest, abstract_type="executive-summary",
                         jats_abstract=crossref_config.get('jats_abstract'))


def get_abstract_attributes(abstract_type):
    if abstract_type == 'executive-summary':
        return ['abstract-type']
    return []


def get_abstract_attributes_text(abstract_type):
    if abstract_type == 'executive-summary':
        return ' abstract-type="executive-summary" '
    return ''


def replace_jats_tag(from_tag_name, to_tag_name, string):
    pattern_from = r'(<%s)(.*?)>' % from_tag_name
    pattern_to = r'<%s\g<2>>' % to_tag_name
    string = re.sub(pattern_from, pattern_to, string)
    string = eautils.replace_tags(string, from_tag_name, to_tag_name)
    return string


def convert_sec_tags(string):
    # convert section title tags to paragraphs
    string = replace_jats_tag('title', 'jats:p', string)
    return etoolsutils.remove_tag('sec', string)


def get_basic_abstract(abstract):
    # Strip inline tags, keep the p tags
    abstract = etoolsutils.remove_tag_and_text('object-id', abstract)
    abstract = etoolsutils.remove_tag('related-object', abstract)
    abstract = etoolsutils.remove_tag('abstract', abstract)
    abstract = utils_html.remove_comment_tags(abstract)
    abstract = etoolsutils.escape_ampersand(abstract)
    abstract = etoolsutils.escape_unmatched_angle_brackets(abstract, utils.allowed_tags())
    abstract = convert_sec_tags(abstract)
    abstract = tags.clean_tags(abstract, do_not_clean=['<p>', '</p>', '<mml:', '</mml:'])
    abstract = eautils.replace_tags(abstract, 'p', 'jats:p')
    return abstract


def get_jats_abstract(abstract):
    # Convert the abstract to jats abstract tags
    abstract = etoolsutils.remove_tag_and_text('object-id', abstract)
    abstract = etoolsutils.remove_tag('abstract', abstract)
    abstract = utils_html.remove_comment_tags(abstract)
    abstract = etoolsutils.escape_ampersand(abstract)
    abstract = etoolsutils.escape_unmatched_angle_brackets(abstract, utils.allowed_tags())

    abstract = replace_jats_tag('sec', 'jats:sec', abstract)
    abstract = replace_jats_tag('related-object', 'jats:related-object', abstract)
    abstract = replace_jats_tag('title', 'jats:title', abstract)

    abstract = eautils.replace_tags(abstract, 'p', 'jats:p')
    abstract = eautils.replace_tags(abstract, 'italic', 'jats:italic')
    abstract = eautils.replace_tags(abstract, 'bold', 'jats:bold')
    abstract = eautils.replace_tags(abstract, 'underline', 'jats:underline')
    abstract = eautils.replace_tags(abstract, 'sub', 'jats:sub')
    abstract = eautils.replace_tags(abstract, 'sup', 'jats:sup')
    abstract = eautils.replace_tags(abstract, 'sc', 'jats:sc')

    abstract = replace_jats_tag('inline-formula', 'jats:inline-formula', abstract)
    abstract = replace_jats_tag('ext-link', 'jats:ext-link', abstract)
    abstract = replace_jats_tag('xref', 'jats:xref', abstract)

    return abstract


def set_abstract_tag(parent, abstract, abstract_type=None, jats_abstract=False):

    tag_name = 'jats:abstract'

    attributes = get_abstract_attributes(abstract_type)
    attributes_text = get_abstract_attributes_text(abstract_type)

    if jats_abstract is True:
        tag_converted_abstract = get_jats_abstract(abstract)
    else:
        tag_converted_abstract = get_basic_abstract(abstract)

    tag_converted_abstract = re.sub('>\n', '>', tag_converted_abstract)

    # add extra namespace attributes if applicable
    for namespace in XML_NAMESPACES:
        tag_match = '<%s' % namespace.get('prefix')
        attribute_match = ' %s' % namespace.get('prefix')
        if (tag_match not in attributes and
                (tag_match in tag_converted_abstract or attribute_match in tag_converted_abstract)):
            attributes.append(namespace.get('attribute'))

    minidom_tag = xmlio.reparsed_tag(
        tag_name, tag_converted_abstract, attributes_text=attributes_text)
    tags.append_tag(parent, minidom_tag, attributes=attributes)
