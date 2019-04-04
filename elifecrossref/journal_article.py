from xml.etree.ElementTree import Element, SubElement
from elifearticle import utils as eautils
from elifecrossref import (
    abstract, access_indicators, citation, collection, component, contributor,
    dataset, dates, funding, related, resource_url, title)


def set_journal_article(parent, poa_article, pub_date, crossref_config):
    journal_article_tag = SubElement(parent, 'journal_article')
    journal_article_tag.set("publication_type", "full_text")
    if (crossref_config.get("reference_distribution_opts")
            and crossref_config.get("reference_distribution_opts") != ''):
        journal_article_tag.set(
            "reference_distribution_opts",
            crossref_config.get("reference_distribution_opts"))

    # Set the title with italic tag support
    title.set_titles(journal_article_tag, poa_article, crossref_config)

    contributor.set_article_contributors(
        journal_article_tag, poa_article, crossref_config.get("contrib_types"))

    abstract.set_abstract(journal_article_tag, poa_article, crossref_config)
    abstract.set_digest(journal_article_tag, poa_article, crossref_config)

    # Journal publication date
    dates.set_publication_date(journal_article_tag, pub_date)

    publisher_item_tag = SubElement(journal_article_tag, 'publisher_item')
    if crossref_config.get("elocation_id") and poa_article.elocation_id:
        item_number_tag = SubElement(publisher_item_tag, 'item_number')
        item_number_tag.set("item_number_type", "article_number")
        item_number_tag.text = poa_article.elocation_id
    identifier_tag = SubElement(publisher_item_tag, 'identifier')
    identifier_tag.set("id_type", "doi")
    identifier_tag.text = poa_article.doi

    # Disable crossmark for now
    # self.set_crossmark(self.journal_article, poa_article)

    funding.set_fundref(journal_article_tag, poa_article)

    set_access_indicators(journal_article_tag, poa_article, crossref_config)

    # this is the spot to add the relations program tag if it is required
    relations_program_tag = None
    if related.do_relations_program(poa_article) is True:
        relations_program_tag = related.set_relations_program(
            journal_article_tag, relations_program_tag)

    dataset.set_datasets(relations_program_tag, poa_article)

    set_archive_locations(journal_article_tag,
                          crossref_config.get("archive_locations"))

    set_doi_data(journal_article_tag, poa_article, crossref_config)

    citation.set_citation_list(
        journal_article_tag, poa_article, relations_program_tag, crossref_config)

    component.set_component_list(journal_article_tag, poa_article, crossref_config)


def set_doi_data(parent, poa_article, crossref_config):
    doi_data_tag = SubElement(parent, 'doi_data')

    doi_tag = SubElement(doi_data_tag, 'doi')
    doi_tag.text = poa_article.doi

    resource_tag = SubElement(doi_data_tag, 'resource')

    resource = resource_url.generate_resource_url(
        poa_article, poa_article, crossref_config)
    resource_tag.text = resource

    collection.set_collection(doi_data_tag, poa_article, "text-mining", crossref_config)


def set_access_indicators(parent, poa_article, crossref_config):
    """
    Set the AccessIndicators
    """

    applies_to = crossref_config.get("access_indicators_applies_to")

    if applies_to and access_indicators.has_license(poa_article) is True:

        ai_program_tag = SubElement(parent, 'ai:program')
        ai_program_tag.set('name', 'AccessIndicators')

        for applies_to in applies_to:
            ai_program_ref_tag = SubElement(ai_program_tag, 'ai:license_ref')
            ai_program_ref_tag.set('applies_to', applies_to)
            ai_program_ref_tag.text = poa_article.license.href


def set_archive_locations(parent, archive_locations):
    if archive_locations:
        archive_locations_tag = SubElement(parent, 'archive_locations')
        for archive_location in archive_locations:
            archive_tag = SubElement(archive_locations_tag, 'archive')
            archive_tag.set('name', archive_location)
