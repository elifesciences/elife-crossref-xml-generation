from xml.etree.ElementTree import SubElement
from elifecrossref import mime_type, resource_url, tags


def set_component_list(parent, poa_article, crossref_config):
    """
    Set the component_list from the article object component_list objects
    """
    if not poa_article.component_list:
        return

    component_list_tag = SubElement(parent, 'component_list')
    for comp in poa_article.component_list:
        component_tag = SubElement(component_list_tag, 'component')
        component_tag.set("parent_relation", "isPartOf")

        titles_tag = SubElement(component_tag, 'titles')

        title_tag = SubElement(titles_tag, 'title')
        title_tag.text = comp.title

        if comp.subtitle:
            set_subtitle(titles_tag, comp, crossref_config)

        if comp.mime_type:
            # Convert to allowed mime types for Crossref, if found
            if mime_type.crossref_mime_type(comp.mime_type):
                format_tag = SubElement(component_tag, 'format')
                format_tag.set("mime_type", mime_type.crossref_mime_type(comp.mime_type))

        if comp.permissions:
            set_component_permissions(component_tag, comp.permissions, crossref_config)

        if comp.doi:
            # Try generating a resource value then continue
            resource = resource_url.generate_resource_url(
                comp, poa_article, crossref_config)
            if resource and resource != '':
                doi_data_tag = SubElement(component_tag, 'doi_data')
                doi_tag_tag = SubElement(doi_data_tag, 'doi')
                doi_tag_tag.text = comp.doi
                resource_tag = SubElement(doi_data_tag, 'resource')
                resource_tag.text = resource

def set_component_permissions(parent, permissions, crossref_config):
    """Specific license for the component"""
    # First check if a license ref is in the config
    if crossref_config.get('component_license_ref') != '':
        # set the component permissions if it has any copyright statement or license value
        set_permissions = False
        for permission in permissions:
            if permission.get('copyright_statement') or permission.get('license'):
                set_permissions = True
        if set_permissions is True:
            component_ai_program_tag = SubElement(parent, 'ai:program')
            component_ai_program_tag.set('name', 'AccessIndicators')
            license_ref_tag = SubElement(component_ai_program_tag, 'ai:license_ref')
            license_ref_tag.text = crossref_config.get('component_license_ref')

def set_subtitle(parent, component, crossref_config):
    tag_name = 'subtitle'
    # Use <i> tags, not <italic> tags, <b> tags not <bold>
    if component.subtitle:
        if crossref_config.get('face_markup') is True:
            tags.add_inline_tag(parent, tag_name, component.subtitle)
        else:
            tags.add_clean_tag(parent, tag_name, component.subtitle)
