from xml.etree.ElementTree import SubElement


def set_archive_locations(parent, archive_location_list):
    "add archive_locations tag to Crossref deposit"
    if archive_location_list:
        archive_locations_tag = SubElement(parent, "archive_locations")
        for archive_location in archive_location_list:
            archive_tag = SubElement(archive_locations_tag, "archive")
            archive_tag.set("name", archive_location)
