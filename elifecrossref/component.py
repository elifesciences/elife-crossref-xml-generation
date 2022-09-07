from xml.etree.ElementTree import SubElement
from elifecrossref import mime_type, resource_url, tags


def set_component_list(parent, poa_article, crossref_config):
    """
    Set the component_list from the article object component_list objects
    """
    if not poa_article.component_list:
        return

    component_list_tag = SubElement(parent, "component_list")
    # ignore excluded components based on the configuration settings
    component_list = [
        comp
        for comp in poa_article.component_list
        if comp.type not in crossref_config.get("component_exclude_types", [])
    ]
    for comp in component_list:
        set_component(component_list_tag, poa_article, comp, crossref_config)


def set_component(parent, poa_article, comp, crossref_config):
    component_tag = SubElement(parent, "component")
    component_tag.set("parent_relation", "isPartOf")

    set_component_titles(component_tag, comp, crossref_config)
    set_component_mime_type(component_tag, comp)
    set_component_permissions(component_tag, comp, crossref_config)
    set_component_doi(component_tag, poa_article, comp, crossref_config)


def set_component_titles(parent, comp, crossref_config):
    titles_tag = SubElement(parent, "titles")
    title_tag = SubElement(titles_tag, "title")
    title_tag.text = comp.title
    if comp.subtitle:
        set_subtitle(titles_tag, comp, crossref_config.get("face_markup"))


def set_component_mime_type(parent, comp):
    if comp.mime_type:
        # Convert to allowed mime types for Crossref, if found
        if mime_type.crossref_mime_type(comp.mime_type):
            format_tag = SubElement(parent, "format")
            format_tag.set("mime_type", mime_type.crossref_mime_type(comp.mime_type))


def set_component_permissions(parent, comp, crossref_config):
    """Specific license for the component"""
    license_href = crossref_config.get("component_license_ref")
    # First check if a license should be added
    if not license_href or not comp.permissions:
        return
    if do_set_component_permissions(comp):
        component_ai_program_tag = SubElement(parent, "ai:program")
        component_ai_program_tag.set("name", "AccessIndicators")
        license_ref_tag = SubElement(component_ai_program_tag, "ai:license_ref")
        license_ref_tag.text = license_href


def do_set_component_permissions(comp):
    """decide whether to set a component permissions"""
    if not comp.permissions:
        return None
    for permission in comp.permissions:
        # set the component permissions if it has any copyright statement or license value
        if permission.get("copyright_statement") or permission.get("license"):
            return True
    return False


def set_component_doi(parent, poa_article, comp, crossref_config):
    if not comp.doi:
        return
    # Try generating a resource value then continue
    resource = resource_url.generate_resource_url(
        comp, poa_article, crossref_config, "component_doi_pattern"
    )
    if resource:
        doi_data_tag = SubElement(parent, "doi_data")
        doi_tag_tag = SubElement(doi_data_tag, "doi")
        doi_tag_tag.text = comp.doi
        resource_tag = SubElement(doi_data_tag, "resource")
        resource_tag.text = resource


def set_subtitle(parent, component, face_markup=None):
    tag_name = "subtitle"
    # Use <i> tags, not <italic> tags, <b> tags not <bold>
    if component.subtitle:
        if face_markup is True:
            tags.add_inline_tag(parent, tag_name, component.subtitle)
        else:
            tags.add_clean_tag(parent, tag_name, component.subtitle)
