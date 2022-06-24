from xml.etree.ElementTree import SubElement
from elifecrossref import access_indicators, clinical_trials, dates, funding


# article types currently supported for depositing simple updates via Crossmark
UPDATES_ARTICLE_TYPES = ["correction", "retraction"]


def do_crossmark(poa_article, crossref_config):
    """check if there are sufficient and correct values to set crossmark data"""
    return bool(
        crossref_config.get("crossmark")
        and (
            crossref_config.get("crossmark_policy")
            or (hasattr(poa_article, "doi") and poa_article.doi)
        )
    )


def set_crossmark(parent, poa_article, crossref_config):
    crossmark = SubElement(parent, "crossmark")

    crossmark_policy = SubElement(crossmark, "crossmark_policy")
    if crossref_config.get("crossmark_policy"):
        crossmark_policy.text = crossref_config.get("crossmark_policy")
    else:
        crossmark_policy.text = poa_article.doi

    if crossref_config.get("crossmark_domains"):
        crossmark_domains = SubElement(crossmark, "crossmark_domains")
        for domain in crossref_config.get("crossmark_domains"):
            crossmark_domain = SubElement(crossmark_domains, "crossmark_domain")
            crossmark_domain_domain = SubElement(crossmark_domain, "domain")
            crossmark_domain_domain.text = domain.get("domain")
            if domain.get("filter"):
                crossmark_domain_filter = SubElement(crossmark_domain, "filter")
                crossmark_domain_filter.text = domain.get("filter")

    if crossref_config.get("crossmark_domain_exclusive"):
        crossmark_domain_exclusive = SubElement(crossmark, "crossmark_domain_exclusive")
        crossmark_domain_exclusive.text = crossref_config.get(
            "crossmark_domain_exclusive"
        )

    if do_updates(poa_article):
        set_updates(crossmark, poa_article, crossref_config)

    set_custom_metadata(crossmark, poa_article, crossref_config)


def do_custom_metadata(poa_article, crossref_config):
    return bool(
        access_indicators.do_access_indicators(poa_article, crossref_config)
        or funding.do_funding(poa_article)
        or clinical_trials.do_clinical_trials(poa_article)
        or do_assertion_tags(poa_article, crossref_config)
    )


def do_assertion_tags(poa_article, crossref_config):
    "decide whether assertion tags should be added to the custom_metadata tag"
    if not poa_article.display_channel or not crossref_config.get(
        "assertion_display_channel_types"
    ):
        return False
    # convert list to lower case values
    display_channel_matches = [
        display_channel.lower()
        for display_channel in crossref_config.get("assertion_display_channel_types")
        if display_channel
    ]
    return bool(poa_article.display_channel.lower() in display_channel_matches)


def set_custom_metadata(parent, poa_article, crossref_config):
    if do_custom_metadata(poa_article, crossref_config):
        custom_metadata = SubElement(parent, "custom_metadata")
        if do_assertion_tags(poa_article, crossref_config):
            set_assertions(custom_metadata, poa_article, crossref_config)
        funding.set_fundref(custom_metadata, poa_article)
        access_indicators.set_access_indicators(
            custom_metadata, poa_article, crossref_config
        )
        clinical_trials.set_clinical_trials(
            custom_metadata, poa_article, crossref_config
        )


def do_updates(poa_article):
    """decide if crossmark updates tag can be added"""
    return bool(
        poa_article.article_type in UPDATES_ARTICLE_TYPES
        and poa_article.related_articles
        and poa_article.related_articles[0].xlink_href
    )


def set_updates(parent, poa_article, crossref_config):
    default_pub_date = None

    updates = SubElement(parent, "updates")
    if poa_article.article_type in UPDATES_ARTICLE_TYPES:
        set_update(
            updates,
            poa_article.article_type,
            dates.iso_date_string(
                dates.get_pub_date(poa_article, crossref_config, default_pub_date)
            ),
            poa_article.related_articles[0].xlink_href,
        )


def set_update(parent, article_type, date, doi):
    update = SubElement(parent, "update")
    update.set("date", date)
    update.set("type", article_type)
    update.text = doi


def set_assertions(parent, poa_article, crossref_config):
    tag_details = []
    tag_details.append(
        {
            "name": "peer_review_transparency",
            "label": "Peer review transparency",
            "group_name": "peer_review_taxonomy",
            "text": "single anonymised",
        }
    )
    tag_details.append(
        {
            "name": "peer_review_interaction",
            "label": "Peer review interaction",
            "group_name": "peer_review_taxonomy",
            "text": "other reviewer(s), editor",
        }
    )
    tag_details.append(
        {
            "name": "peer_review_published",
            "label": "Peer review published",
            "group_name": "peer_review_taxonomy",
            "text": (
                "review summaries, review reports, author/editor communication, "
                "reviewer identities reviewer opt in, editor identities"
            ),
        }
    )
    tag_details.append(
        {
            "name": "post_publication_commenting",
            "label": "Post publication commenting",
            "group_name": "post_publication_commenting",
            "text": "open (sign in with ORCID iD required)",
        }
    )

    for details in tag_details:
        assertion_tag = SubElement(parent, "assertion")
        for attribute in ["group_name", "label", "name"]:
            assertion_tag.set(attribute, details.get(attribute))
        assertion_tag.text = details.get("text")
