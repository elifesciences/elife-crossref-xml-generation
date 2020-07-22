import re


def allowed_tags():
    """tuple of whitelisted tags"""
    return (
        '<p>', '</p>',
        '<italic>', '</italic>',
        '<bold>', '</bold>',
        '<underline>', '</underline>',
        '<sub>', '</sub>',
        '<sup>', '</sup>',
        '<sc>', '</sc>',
        '<inline-formula>', '</inline-formula>',
        '<mml:', '</mml:',
        '<ext-link', '</ext-link>',
        '<xref', '</xref>',
        '<sec', '</sec>',
        '<title', '</title>',
        '<related-object', '</related-object>',
    )


def clean_string(string):
    """remove unwanted characters when concatenating the batch_id"""
    if string:
        return re.sub(r'[^a-zA-Z0-9_\-]', '', str(string))
    return None


def remove_tag(tag_name, string):
    pattern = r'\s*</?%s.*?>\s*' % tag_name
    return re.sub(pattern, '', string)


def remove_tag_and_text(tag_name, string):
    pattern = r'\s*<%s.*?>.*?</%s>\s*' % (tag_name, tag_name)
    return re.sub(pattern, '', string)
