from xml.etree.ElementTree import SubElement
from elifecrossref import dates


def set_status_tag(parent, status_type, status_date, description):
    "add a status tag with a date and description"
    status_tag = SubElement(parent, "status")
    status_tag.set("date", dates.iso_date_string(status_date))
    status_tag.set("type", status_type)
    status_description_tag = SubElement(status_tag, "description")
    status_description_tag.text = description
