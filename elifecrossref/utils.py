
def allowed_tags():
    "tuple of whitelisted tags"
    return (
        '<p>', '</p>',
        '<italic>', '</italic>',
        '<bold>', '</bold>',
        '<underline>', '</underline>',
        '<sub>', '</sub>',
        '<sup>', '</sup>',
        '<sc>', '</sc>',
    )
