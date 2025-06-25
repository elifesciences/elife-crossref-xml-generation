"""
Module for adding version data to Crossref deposii
"""

from xml.etree.ElementTree import SubElement


def set_version_info(parent, poa_article):
    "add version_info tag and sub elements"
    version_info_tag = SubElement(parent, "version_info")
    version_tag = SubElement(version_info_tag, "version")
    version_tag.set("xml:lang", "en")
    version_tag.text = str(poa_article.version)
