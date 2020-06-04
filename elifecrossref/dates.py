import time
from xml.etree.ElementTree import SubElement


def set_publication_date(parent, pub_date):
    # pub_date is a python time object
    if pub_date:
        publication_date_tag = SubElement(parent, 'publication_date')
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
    """format a date object into an iso format date string e.g. 2019-12-31"""
    return time.strftime('%Y-%m-%d', pub_date) if pub_date else None
