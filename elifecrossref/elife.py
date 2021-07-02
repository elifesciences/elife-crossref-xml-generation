def elife_style_article_attributes(obj):
    # Special logic for elife article style
    version = ""
    if obj.version:
        version = "-v" + str(obj.version)
    return version


def elife_style_component_attributes(obj):
    # Some special additional logic for elife style
    component_id = obj.id
    if obj.type and obj.type == "abstract":
        if obj.title and "digest" in obj.title.lower():
            component_id = "digest"
        else:
            component_id = "abstract"
    # Set the URL prefix for some types
    prefix1 = ""
    if (
        obj.asset
        and obj.asset in ["figsupp", "data"]
        or obj.type
        and obj.type in ["supplementary-material"]
    ):
        prefix1 = "/figures"
    return component_id, prefix1
