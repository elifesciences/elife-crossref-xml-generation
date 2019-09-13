from elifearticle import utils as eautils
from elifetools import xmlio
from elifetools import utils as etoolsutils
from elifecrossref import tags, utils


def set_abstract(parent, poa_article, crossref_config):
    if poa_article.abstract:
        set_abstract_tag(parent, poa_article.abstract, abstract_type="abstract",
                         jats_abstract=crossref_config.get('jats_abstract'))


def set_digest(parent, poa_article, crossref_config):
    if hasattr(poa_article, 'digest') and poa_article.digest:
        set_abstract_tag(parent, poa_article.digest, abstract_type="executive-summary",
                         jats_abstract=crossref_config.get('jats_abstract'))


def get_abstract_attributes(abstract_type):
    if abstract_type == 'executive-summary':
        return ['abstract-type']
    return None


def get_abstract_attributes_text(abstract_type):
    if abstract_type == 'executive-summary':
        return ' abstract-type="executive-summary" '
    return ''


def get_basic_abstract(abstract):
    # Strip inline tags, keep the p tags
    abstract = etoolsutils.escape_ampersand(abstract)
    abstract = etoolsutils.escape_unmatched_angle_brackets(abstract, utils.allowed_tags())
    abstract = tags.clean_tags(abstract, do_not_clean=['<p>', '</p>', '<mml:', '</mml:'])
    abstract = eautils.replace_tags(abstract, 'p', 'jats:p')
    abstract = abstract
    return abstract


def get_jats_abstract(abstract):
    # Convert the abstract to jats abstract tags
    abstract = etoolsutils.escape_ampersand(abstract)
    abstract = etoolsutils.escape_unmatched_angle_brackets(abstract, utils.allowed_tags())
    abstract = eautils.replace_tags(abstract, 'p', 'jats:p')
    abstract = eautils.replace_tags(abstract, 'italic', 'jats:italic')
    abstract = eautils.replace_tags(abstract, 'bold', 'jats:bold')
    abstract = eautils.replace_tags(abstract, 'underline', 'jats:underline')
    abstract = eautils.replace_tags(abstract, 'sub', 'jats:sub')
    abstract = eautils.replace_tags(abstract, 'sup', 'jats:sup')
    abstract = eautils.replace_tags(abstract, 'sc', 'jats:sc')
    abstract = eautils.remove_tag('inline-formula', abstract)
    abstract = eautils.remove_tag('ext-link', abstract)
    return abstract


def set_abstract_tag(parent, abstract, abstract_type=None, jats_abstract=False):

    tag_name = 'jats:abstract'

    attributes = get_abstract_attributes(abstract_type)
    attributes_text = get_abstract_attributes_text(abstract_type)

    if jats_abstract is True:
        tag_converted_abstract = get_jats_abstract(abstract)
    else:
        tag_converted_abstract = get_basic_abstract(abstract)

    minidom_tag = xmlio.reparsed_tag(tag_name, tag_converted_abstract,
                                    attributes_text=attributes_text)
    tags.append_tag(parent, minidom_tag, attributes=attributes)
