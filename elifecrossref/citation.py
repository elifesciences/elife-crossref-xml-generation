from xml.etree.ElementTree import SubElement
from elifecrossref import related, tags


def set_citation_list(parent, poa_article, relations_program_tag, crossref_config):
    """
    Set the citation_list from the article object ref_list objects
    """
    ref_index = 0
    if poa_article.ref_list:
        citation_list_tag = SubElement(parent, "citation_list")
    for ref in poa_article.ref_list:
        # Increment
        ref_index = ref_index + 1
        # decide whether to create a related_item for the citation
        if related.do_citation_related_item(ref):
            set_citation_related_item(relations_program_tag, ref)

        # continue with creating a citation tag
        set_citation(
            citation_list_tag,
            ref,
            ref_index,
            crossref_config.get("face_markup"),
            crossref_config.get("crossref_schema_version"),
        )


def set_citation(parent, ref, ref_index, face_markup, crossref_schema_version):
    # continue with creating a citation tag
    citation_tag = SubElement(parent, "citation")
    set_citation_key(citation_tag, ref, ref_index)
    set_citation_title(citation_tag, ref)
    set_citation_authors(citation_tag, ref)
    set_citation_volume(citation_tag, ref)
    set_citation_issue(citation_tag, ref)
    set_citation_first_page(citation_tag, ref)
    set_citation_year(citation_tag, ref)
    set_citation_article_title(citation_tag, ref)
    set_citation_doi(citation_tag, ref)
    set_citation_isbn(citation_tag, ref)
    set_elocation_id(citation_tag, ref, crossref_schema_version)
    # unstructured-citation
    if do_unstructured_citation(ref) is True:
        set_unstructured_citation(citation_tag, ref, face_markup)


def set_citation_key(citation_tag, ref, ref_index):
    if ref.id:
        citation_tag.set("key", ref.id)
    else:
        citation_tag.set("key", str(ref_index))


def set_citation_title(parent, ref):
    if ref.source:
        if ref.publication_type == "journal":
            journal_title_tag = SubElement(parent, "journal_title")
            journal_title_tag.text = ref.source
        else:
            volume_title_tag = SubElement(parent, "volume_title")
            volume_title_tag.text = ref.source


def set_citation_authors(parent, ref):
    authors = filter_citation_authors(ref)
    if authors:
        # Only set the first author surname
        first_author = authors[0]
        if first_author.get("surname"):
            author_tag = SubElement(parent, "author")
            author_tag.text = first_author.get("surname")
        elif first_author.get("collab"):
            tags.add_clean_tag(parent, "author", first_author.get("collab"))


def set_citation_volume(parent, ref):
    if ref.volume:
        volume_tag = SubElement(parent, "volume")
        volume_tag.text = ref.volume[0:31]


def set_citation_issue(parent, ref):
    if ref.issue:
        issue_tag = SubElement(parent, "issue")
        issue_tag.text = ref.issue


def set_citation_first_page(parent, ref):
    if ref.fpage:
        first_page_tag = SubElement(parent, "first_page")
        first_page_tag.text = ref.fpage


def set_citation_year(parent, ref):
    if ref.year or ref.year_numeric:
        cyear_tag = SubElement(parent, "cYear")
        # Prefer the numeric year value if available
        if ref.year_numeric:
            cyear_tag.text = str(ref.year_numeric)
        else:
            cyear_tag.text = ref.year


def set_citation_article_title(parent, ref):
    if ref.article_title or ref.data_title:
        if ref.article_title:
            tags.add_clean_tag(parent, "article_title", ref.article_title)
        elif ref.data_title:
            tags.add_clean_tag(parent, "article_title", ref.data_title)


def set_citation_doi(parent, ref):
    if ref.doi:
        doi_tag = SubElement(parent, "doi")
        doi_tag.text = ref.doi


def set_citation_isbn(parent, ref):
    if ref.isbn:
        isbn_tag = SubElement(parent, "isbn")
        isbn_tag.text = ref.isbn


def set_elocation_id(parent, ref, crossref_schema_version):
    if ref.elocation_id:
        if crossref_schema_version in ["4.3.5", "4.3.7", "4.4.0"]:
            # Until alternate tag is available, elocation-id goes into first_page tag
            first_page_tag = SubElement(parent, "first_page")
            first_page_tag.text = ref.elocation_id
        else:
            # schema greater than 4.4.0 supports elocation_id
            elocation_id_tag = SubElement(parent, "elocation_id")
            elocation_id_tag.text = ref.elocation_id


def set_citation_related_item(parent, ref):
    related_item_tag = SubElement(parent, "rel:related_item")
    if ref.data_title:
        related.set_related_item_description(related_item_tag, ref.data_title)
    identifier_type = None
    related_item_text = None
    related_item_type = "inter_work_relation"
    relationship_type = "references"
    if ref.doi:
        identifier_type = "doi"
        related_item_text = ref.doi
    elif ref.accession:
        identifier_type = "accession"
        related_item_text = ref.accession
    elif ref.pmid:
        identifier_type = "pmid"
        related_item_text = ref.pmid
    elif ref.uri:
        identifier_type = "uri"
        related_item_text = ref.uri
    if identifier_type and related_item_text:
        related.set_related_item_work_relation(
            related_item_tag,
            related_item_type,
            relationship_type,
            identifier_type,
            related_item_text,
        )


def set_unstructured_citation(parent, ref, face_markup):
    # tag_content
    tag_content = ""
    author_line = citation_author_line(ref)

    if ref.publication_type and ref.publication_type in [
        "confproc",
        "patent",
        "preprint",
        "report",
        "software",
        "thesis",
        "web",
        "webpage",
    ]:
        tag_content = ". ".join(
            [
                item.rstrip(".")
                for item in [
                    author_line,
                    ref.year,
                    ref.article_title,
                    ref.data_title,
                    citation_publisher(ref),
                    ref.source,
                    ref.version,
                    ref.patent,
                    ref.conf_name,
                    citation_uri(ref),
                ]
                if item is not None
            ]
        )
        tag_content += "."
    # add the tag if there is tag_content
    if tag_content != "":
        # handle inline tagging
        if face_markup is True:
            tags.add_inline_tag(parent, "unstructured_citation", tag_content)
        else:
            tags.add_clean_tag(parent, "unstructured_citation", tag_content)
    return parent


def citation_author_line(ref):
    author_line = None
    author_names = []
    # extract all authors regardless of their group-type
    for author in ref.authors:
        author_name = ""
        if author.get("surname"):
            author_name = author.get("surname")
            if author.get("given-names"):
                author_name += " " + author.get("given-names")
        elif author.get("collab"):
            author_name = author.get("collab")
        if author_name != "":
            author_names.append(author_name)
    if author_names:
        author_line = ", ".join(author_names)
    return author_line


def citation_publisher(ref):
    if ref.publisher_loc or ref.publisher_name:
        return ": ".join(
            [
                item
                for item in [ref.publisher_loc, ref.publisher_name]
                if item is not None
            ]
        )
    return None


def citation_uri(ref):
    uri_content = ""
    if ref.uri:
        uri_content = ref.uri
    if ref.date_in_citation:
        uri_content += " [Accessed " + ref.date_in_citation + "]"
    return uri_content if uri_content != "" else None


def do_unstructured_citation(ref):
    """decide if a citation should have an unstructured_citation tag added"""
    if ref.publication_type and ref.publication_type in [
        "confproc",
        "patent",
        "software",
        "thesis",
        "web",
        "webpage",
    ]:
        return True
    if (
        ref.publication_type
        and ref.publication_type in ["preprint"]
        and ref.doi is None
    ):
        return True
    if ref.publication_type and ref.publication_type in ["report"] and ref.isbn is None:
        return True
    return False


def filter_citation_authors(ref):
    """logic for which authors to select for citation records"""
    # First consider authors with group-type author
    authors = [c for c in ref.authors if c.get("group-type") == "author"]
    if not authors:
        # Take editors if there are no authors
        authors = [c for c in ref.authors if c.get("group-type") == "editor"]
    return authors
