from xml.etree.ElementTree import SubElement
from elifecrossref import (
    abstract,
    access_indicators,
    citation,
    component,
    contributor,
    crossmark,
    dataset,
    dates,
    doi,
    funding,
    preprint,
    related,
    title,
)


def set_journal_article(parent, poa_article, pub_date, crossref_config):
    journal_article_tag = SubElement(parent, "journal_article")
    journal_article_tag.set("publication_type", "full_text")
    if (
        crossref_config.get("reference_distribution_opts")
        and crossref_config.get("reference_distribution_opts") != ""
    ):
        journal_article_tag.set(
            "reference_distribution_opts",
            crossref_config.get("reference_distribution_opts"),
        )

    # Set the title with italic tag support
    title.set_titles(journal_article_tag, poa_article.title, crossref_config)

    contributor.set_article_contributors(
        journal_article_tag, poa_article, crossref_config.get("contrib_types")
    )

    abstract.set_abstract(journal_article_tag, poa_article, crossref_config)
    abstract.set_digest(journal_article_tag, poa_article, crossref_config)

    # Journal publication date
    dates.set_publication_date(journal_article_tag, pub_date)

    # article accepted date
    dates.set_acceptance_date(journal_article_tag, poa_article.get_date("accepted"))

    publisher_item_tag = SubElement(journal_article_tag, "publisher_item")
    if crossref_config.get("elocation_id") and poa_article.elocation_id:
        item_number_tag = SubElement(publisher_item_tag, "item_number")
        item_number_tag.set("item_number_type", "article_number")
        item_number_tag.text = poa_article.elocation_id
    identifier_tag = SubElement(publisher_item_tag, "identifier")
    identifier_tag.set("id_type", "doi")
    identifier_tag.text = poa_article.doi

    # Crossmark data includes funding and access indicators, otherwise add them separately
    if crossmark.do_crossmark(poa_article, crossref_config):
        crossmark.set_crossmark(journal_article_tag, poa_article, crossref_config)
    else:
        funding.set_fundref(journal_article_tag, poa_article)
        access_indicators.set_access_indicators(
            journal_article_tag, poa_article, crossref_config
        )

    # this is the spot to add the relations program tag if it is required
    relations_program_tag = None
    if related.do_relations_program(poa_article) is True:
        relations_program_tag = related.set_relations_program(
            journal_article_tag, relations_program_tag
        )

    dataset.set_datasets(relations_program_tag, poa_article)

    set_archive_locations(journal_article_tag, crossref_config.get("archive_locations"))

    doi.set_article_doi_data(journal_article_tag, poa_article, crossref_config)

    citation.set_citation_list(
        journal_article_tag, poa_article, relations_program_tag, crossref_config
    )

    component.set_component_list(journal_article_tag, poa_article, crossref_config)

    if related.do_preprint_related_item(poa_article) is True:
        preprint.set_preprint(relations_program_tag, poa_article.preprint)


def set_archive_locations(parent, archive_locations):
    if archive_locations:
        archive_locations_tag = SubElement(parent, "archive_locations")
        for archive_location in archive_locations:
            archive_tag = SubElement(archive_locations_tag, "archive")
            archive_tag.set("name", archive_location)
