import time
from xml.etree.ElementTree import SubElement


def get_pub_date(poa_article, crossref_config, default_pub_date):
    """
    For using in XML generation, use the article pub date
    or by default use the run time pub date
    """
    pub_date = None

    for date_type in crossref_config.get("pub_date_types"):
        pub_date_obj = poa_article.get_date(date_type)
        if pub_date_obj:
            break

    if pub_date_obj:
        pub_date = pub_date_obj.date
    else:
        # Default use the run time date
        pub_date = default_pub_date
    return pub_date


def set_acceptance_date(parent, article_date):
    # article_date is an ArticleDate object
    if article_date:
        date_tag = SubElement(parent, "acceptance_date")
        set_date_detail(date_tag, article_date.date)


def set_posted_date(parent, article_date):
    # article_date is an ArticleDate object
    if article_date:
        date_tag = SubElement(parent, "posted_date")
        set_date_detail(date_tag, article_date.date)


def set_publication_date(parent, pub_date):
    # pub_date is a python time object
    if pub_date:
        publication_date_tag = SubElement(parent, "publication_date")
        publication_date_tag.set("media_type", "online")
        set_date_detail(publication_date_tag, pub_date)


def set_date_detail(parent, pub_date):
    month_tag = SubElement(parent, "month")
    month_tag.text = str(pub_date.tm_mon).zfill(2)
    day_tag = SubElement(parent, "day")
    day_tag.text = str(pub_date.tm_mday).zfill(2)
    year_tag = SubElement(parent, "year")
    year_tag.text = str(pub_date.tm_year)


def iso_date_string(pub_date):
    """format a time.struct_time object into an iso format date string e.g. 2019-12-31"""
    return time.strftime("%Y-%m-%d", pub_date) if pub_date else None
