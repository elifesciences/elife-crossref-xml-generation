from xml.etree.ElementTree import SubElement
from elifecrossref import tags


def set_citation(parent, ref, ref_index, face_markup,
                 crossref_schema_version):
    # continue with creating a citation tag
    citation_tag = SubElement(parent, 'citation')

    if ref.id:
        citation_tag.set("key", ref.id)
    else:
        citation_tag.set("key", str(ref_index))

    if ref.source:
        if ref.publication_type == "journal":
            journal_title_tag = SubElement(citation_tag, 'journal_title')
            journal_title_tag.text = ref.source
        else:
            volume_title_tag = SubElement(citation_tag, 'volume_title')
            volume_title_tag.text = ref.source

    authors = filter_citation_authors(ref)
    if authors:
        # Only set the first author surname
        first_author = authors[0]
        if first_author.get("surname"):
            author_tag = SubElement(citation_tag, 'author')
            author_tag.text = first_author.get("surname")
        elif first_author.get("collab"):
            tags.add_clean_tag(citation_tag, 'author', first_author.get("collab"))

    if ref.volume:
        volume_tag = SubElement(citation_tag, 'volume')
        volume_tag.text = ref.volume[0:31]

    if ref.issue:
        issue_tag = SubElement(citation_tag, 'issue')
        issue_tag.text = ref.issue

    if ref.fpage:
        first_page_tag = SubElement(citation_tag, 'first_page')
        first_page_tag.text = ref.fpage

    if ref.year or ref.year_numeric:
        cyear_tag = SubElement(citation_tag, 'cYear')
        # Prefer the numeric year value if available
        if ref.year_numeric:
            cyear_tag.text = str(ref.year_numeric)
        else:
            cyear_tag.text = ref.year

    if ref.article_title or ref.data_title:
        if ref.article_title:
            tags.add_clean_tag(citation_tag, 'article_title', ref.article_title)
        elif ref.data_title:
            tags.add_clean_tag(citation_tag, 'article_title', ref.data_title)

    if ref.doi:
        doi_tag = SubElement(citation_tag, 'doi')
        doi_tag.text = ref.doi

    if ref.isbn:
        isbn_tag = SubElement(citation_tag, 'isbn')
        isbn_tag.text = ref.isbn

    if ref.elocation_id:
        if crossref_schema_version in ['4.3.5', '4.3.7', '4.4.0']:
            # Until alternate tag is available, elocation-id goes into first_page tag
            first_page_tag = SubElement(citation_tag, 'first_page')
            first_page_tag.text = ref.elocation_id
        else:
            # schema greater than 4.4.0 supports elocation_id
            elocation_id_tag = SubElement(citation_tag, 'elocation_id')
            elocation_id_tag.text = ref.elocation_id

    # unstructured-citation
    if do_unstructured_citation(ref) is True:
        set_unstructured_citation(citation_tag, ref, face_markup)


def set_unstructured_citation(parent, ref, face_markup):
    # tag_content
    tag_content = ''
    author_line = citation_author_line(ref)

    if ref.publication_type and ref.publication_type in [
            'confproc', 'patent', 'preprint', 'report', 'software', 'thesis', 'web', 'webpage']:
        tag_content = '. '.join([item.rstrip('.') for item in [
            author_line, ref.year, ref.article_title, ref.data_title,
            citation_publisher(ref), ref.source, ref.version,
            ref.patent, ref.conf_name, citation_uri(ref)] if item is not None])
        tag_content += '.'
    # add the tag if there is tag_content
    if tag_content != '':
        # handle inline tagging
        if face_markup is True:
            tags.add_inline_tag(parent, 'unstructured_citation', tag_content)
        else:
            tags.add_clean_tag(parent, 'unstructured_citation', tag_content)
    return parent


def citation_author_line(ref):
    author_line = None
    author_names = []
    # extract all authors regardless of their group-type
    for author in ref.authors:
        author_name = ''
        if author.get('surname'):
            author_name = author.get('surname')
            if author.get('given-names'):
                author_name += ' ' + author.get('given-names')
        elif author.get('collab'):
            author_name = author.get('collab')
        if author_name != '':
            author_names.append(author_name)
    if author_names:
        author_line = ', '.join(author_names)
    return author_line


def citation_publisher(ref):
    if ref.publisher_loc or ref.publisher_name:
        return ': '.join([item for item in [
            ref.publisher_loc, ref.publisher_name] if item is not None])
    return None


def citation_uri(ref):
    uri_content = ''
    if ref.uri:
        uri_content = ref.uri
    if ref.date_in_citation:
        uri_content += ' [Accessed ' + ref.date_in_citation + ']'
    return uri_content if uri_content != '' else None


def do_unstructured_citation(ref):
    """decide if a citation should have an unstructured_citation tag added"""
    if ref.publication_type and ref.publication_type in [
            'confproc', 'patent', 'software', 'thesis', 'web', 'webpage']:
        return True
    if ref.publication_type and ref.publication_type in ['preprint'] and ref.doi is None:
        return True
    if ref.publication_type and ref.publication_type in ['report'] and ref.isbn is None:
        return True
    return False


def filter_citation_authors(ref):
    """logic for which authors to select for citation records"""
    # First consider authors with group-type author
    authors = [c for c in ref.authors if c.get('group-type') == 'author']
    if not authors:
        # Take editors if there are no authors
        authors = [c for c in ref.authors if c.get('group-type') == 'editor']
    return authors
