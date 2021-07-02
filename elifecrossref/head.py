import time
from xml.etree.ElementTree import SubElement


def set_head(parent, batch_id, pub_date, crossref_config):
    head_tag = SubElement(parent, "head")
    doi_batch_id_tag = SubElement(head_tag, "doi_batch_id")
    doi_batch_id_tag.text = batch_id
    timestamp_tag = SubElement(head_tag, "timestamp")
    timestamp_tag.text = time.strftime("%Y%m%d%H%M%S", pub_date)
    set_depositor(head_tag, crossref_config)
    registrant_tag = SubElement(head_tag, "registrant")
    registrant_tag.text = crossref_config.get("registrant")


def set_depositor(parent, crossref_config):
    depositor_tag = SubElement(parent, "depositor")
    name_tag = SubElement(depositor_tag, "depositor_name")
    name_tag.text = crossref_config.get("depositor_name")
    email_address_tag = SubElement(depositor_tag, "email_address")
    email_address_tag.text = crossref_config.get("email_address")
