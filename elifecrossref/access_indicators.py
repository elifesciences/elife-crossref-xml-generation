
def has_license(poa_article):
    """check if the article has the minimum requirements of a license"""
    if not poa_article.license:
        return False
    if not poa_article.license.href:
        return False
    return True
