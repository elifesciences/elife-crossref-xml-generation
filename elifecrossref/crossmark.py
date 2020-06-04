from xml.etree.ElementTree import SubElement
from elifecrossref import access_indicators, dates, funding, journal


# article types currently supported for depositing simple updates via Crossmark
UPDATES_ARTICLE_TYPES = ['correction', 'retraction']


def do_crossmark(poa_article, crossref_config):
    """check if there are sufficient and correct values to set crossmark data"""
    return bool(
        crossref_config.get("crossmark") and (
            crossref_config.get('crossmark_policy') or (
                hasattr(poa_article, 'doi') and poa_article.doi)
            )
        )


def set_crossmark(parent, poa_article, crossref_config):
    crossmark = SubElement(parent, 'crossmark')

    crossmark_policy = SubElement(crossmark, 'crossmark_policy')
    if crossref_config.get('crossmark_policy'):
        crossmark_policy.text = crossref_config.get('crossmark_policy')
    else:
        crossmark_policy.text = poa_article.doi

    if crossref_config.get('crossmark_domains'):
        crossmark_domains = SubElement(crossmark, 'crossmark_domains')
        for domain in crossref_config.get('crossmark_domains'):
            crossmark_domain = SubElement(crossmark_domains, 'crossmark_domain')
            crossmark_domain_domain = SubElement(crossmark_domain, 'domain')
            crossmark_domain_domain.text = domain.get('domain')
            if domain.get('filter'):
                crossmark_domain_filter = SubElement(crossmark_domain, 'filter')
                crossmark_domain_filter.text = domain.get('filter')

    if crossref_config.get('crossmark_domain_exclusive'):
        crossmark_domain_exclusive = SubElement(crossmark, 'crossmark_domain_exclusive')
        crossmark_domain_exclusive.text = crossref_config.get('crossmark_domain_exclusive')

    if do_updates(poa_article):
        set_updates(crossmark, poa_article, crossref_config)

    set_custom_metadata(crossmark, poa_article, crossref_config)


def do_custom_metadata(poa_article, crossref_config):
    return bool(
        access_indicators.do_access_indicators(poa_article, crossref_config)
        or funding.do_funding(poa_article))


def set_custom_metadata(parent, poa_article, crossref_config):
    if do_custom_metadata(poa_article, crossref_config):
        custom_metadata = SubElement(parent, 'custom_metadata')
        funding.set_fundref(custom_metadata, poa_article)
        access_indicators.set_access_indicators(custom_metadata, poa_article, crossref_config)


def do_updates(poa_article):
    """decide if crossmark updates tag can be added"""
    return bool(
        poa_article.article_type in UPDATES_ARTICLE_TYPES and
        poa_article.related_articles and
        poa_article.related_articles[0].xlink_href)


def set_updates(parent, poa_article, crossref_config):
    default_pub_date = None

    updates = SubElement(parent, 'updates')
    update = SubElement(updates, 'update')
    update.set('type', poa_article.article_type)
    update.set('date', dates.iso_date_string(
        journal.get_pub_date(poa_article, crossref_config, default_pub_date)))
    update.text = poa_article.related_articles[0].xlink_href
