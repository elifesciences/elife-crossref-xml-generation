from elifearticle.article import Article, Component
from elifecrossref import elife


def generate_resource_url(obj, poa_article, crossref_config, pattern_type=None):
    # Generate a resource value for doi_data based on the object provided
    if isinstance(obj, Article):
        if not pattern_type:
            pattern_type = "doi_pattern"
        version = elife.elife_style_article_attributes(obj)
        doi_pattern = crossref_config.get(pattern_type)
        if doi_pattern != '':
            return crossref_config.get(pattern_type).format(
                doi=obj.doi,
                manuscript=obj.manuscript,
                volume=obj.volume,
                version=version)
        else:
            # if no doi_pattern is specified, try to get it from the self-uri value
            #  that has no content_type
            for self_uri in obj.self_uri_list:
                if self_uri.content_type is None:
                    return self_uri.xlink_href

    elif isinstance(obj, Component):
        component_id = obj.id
        prefix1 = ''
        if crossref_config.get('elife_style_component_doi') is True:
            component_id, prefix1 = elife.elife_style_component_attributes(obj)
        return crossref_config.get("component_doi_pattern").format(
            doi=poa_article.doi,
            manuscript=poa_article.manuscript,
            volume=poa_article.volume,
            prefix1=prefix1,
            id=component_id)
    return None
