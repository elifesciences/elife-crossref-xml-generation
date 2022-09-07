from elifearticle.article import Article, Component
from elifecrossref import elife


def generate_resource_url(obj, poa_article, crossref_config, pattern_type=None):
    # Generate a resource value for doi_data based on the object provided
    if isinstance(obj, Component) or pattern_type == "peer_review_doi_pattern":
        if (
            pattern_type == "component_doi_pattern"
            and crossref_config.get("elife_style_component_doi") is True
        ):
            id_value, prefix1 = elife.elife_style_component_attributes(obj)
        else:
            id_value = obj.id
            prefix1 = ""
        return crossref_config.get(pattern_type).format(
            doi=poa_article.doi,
            manuscript=poa_article.manuscript,
            volume=poa_article.volume,
            prefix1=prefix1,
            id=id_value,
        )
    if isinstance(obj, Article):
        version = elife.elife_style_article_attributes(obj)
        if crossref_config.get(pattern_type):
            return crossref_config.get(pattern_type).format(
                doi=obj.doi,
                manuscript=obj.manuscript,
                volume=obj.volume,
                version=version,
            )
        # if no doi_pattern is specified, try to get it from the self-uri value
        #  that has no content_type
        for self_uri in obj.self_uri_list:
            if self_uri.content_type is None:
                return self_uri.xlink_href
    return ""
