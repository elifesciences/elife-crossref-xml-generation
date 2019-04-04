from xml.etree.ElementTree import SubElement


def set_publication_date(parent, pub_date):
    # pub_date is a python time object
    if pub_date:
        publication_date_tag = SubElement(parent, 'publication_date')
        publication_date_tag.set("media_type", "online")
        month_tag = SubElement(publication_date_tag, "month")
        month_tag.text = str(pub_date.tm_mon).zfill(2)
        day_tag = SubElement(publication_date_tag, "day")
        day_tag.text = str(pub_date.tm_mday).zfill(2)
        year_tag = SubElement(publication_date_tag, "year")
        year_tag.text = str(pub_date.tm_year)
