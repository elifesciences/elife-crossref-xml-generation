from elifearticle import utils as eautils
from elifetools import utils as etoolsutils
from elifecrossref import tags, utils


def set_abstract(parent, poa_article, crossref_config):
    if poa_article.abstract:
        abstract = poa_article.abstract
        set_abstract_tag(parent, abstract, abstract_type="abstract",
                         jats_abstract=crossref_config.get('jats_abstract'))


def set_digest(parent, poa_article, crossref_config):
    if hasattr(poa_article, 'digest') and poa_article.digest:
        set_abstract_tag(parent, poa_article.digest, abstract_type="executive-summary",
                         jats_abstract=crossref_config.get('jats_abstract'))


def set_abstract_tag(parent, abstract, abstract_type=None, jats_abstract=False):

    tag_name = 'jats:abstract'

    attributes = []
    attributes_text = ''
    if abstract_type == 'executive-summary':
        attributes = ['abstract-type']
        attributes_text = ' abstract-type="executive-summary" '

    # Convert the abstract to jats abstract tags, or strip all the inline tags
    if jats_abstract is True:
        tag_converted_abstract = abstract
        tag_converted_abstract = etoolsutils.escape_ampersand(tag_converted_abstract)
        tag_converted_abstract = etoolsutils.escape_unmatched_angle_brackets(
            tag_converted_abstract, utils.allowed_tags())
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'p', 'jats:p')
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'italic', 'jats:italic')
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'bold', 'jats:bold')
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'underline', 'jats:underline')
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'sub', 'jats:sub')
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'sup', 'jats:sup')
        tag_converted_abstract = eautils.replace_tags(
            tag_converted_abstract, 'sc', 'jats:sc')
        tag_converted_abstract = eautils.remove_tag('inline-formula', tag_converted_abstract)
        tag_converted_abstract = eautils.remove_tag('ext-link', tag_converted_abstract)
    else:
        # Strip inline tags, keep the p tags
        tag_converted_abstract = abstract
        tag_converted_abstract = etoolsutils.escape_ampersand(tag_converted_abstract)
        tag_converted_abstract = etoolsutils.escape_unmatched_angle_brackets(
            tag_converted_abstract, utils.allowed_tags())
        tag_converted_abstract = tags.clean_tags(
            tag_converted_abstract, do_not_clean=['<p>', '</p>', '<mml:', '</mml:'])
        tag_converted_abstract = eautils.replace_tags(tag_converted_abstract, 'p', 'jats:p')
        tag_converted_abstract = tag_converted_abstract

    minidom_tag = tags.reparsed_tag(tag_name, tag_converted_abstract,
                                    attributes_text=attributes_text)
    tags.append_tag(parent, minidom_tag, attributes=attributes)
