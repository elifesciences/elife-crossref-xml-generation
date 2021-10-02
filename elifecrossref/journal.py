from xml.etree.ElementTree import SubElement
from elifearticle import utils as eautils
from elifecrossref import dates, journal_article


def set_journal(parent, poa_article, crossref_config, default_pub_date):
    # Add journal for each article
    journal_tag = SubElement(parent, "journal")
    set_journal_metadata(journal_tag, poa_article)

    journal_issue_tag = SubElement(journal_tag, "journal_issue")

    pub_date = dates.get_pub_date(poa_article, crossref_config, default_pub_date)
    dates.set_publication_date(journal_issue_tag, pub_date)

    journal_volume_tag = SubElement(journal_issue_tag, "journal_volume")
    volume_tag = SubElement(journal_volume_tag, "volume")
    # Use volume from the article unless not present then use the default
    if poa_article.volume:
        volume_tag.text = poa_article.volume
    else:
        if crossref_config.get("year_of_first_volume"):
            volume_tag.text = eautils.calculate_journal_volume(
                pub_date, crossref_config.get("year_of_first_volume")
            )

    # Add journal article
    journal_article.set_journal_article(
        journal_tag, poa_article, pub_date, crossref_config
    )


def set_journal_metadata(parent, poa_article):
    # journal_metadata
    journal_metadata_tag = SubElement(parent, "journal_metadata")
    journal_metadata_tag.set("language", "en")
    full_title_tag = SubElement(journal_metadata_tag, "full_title")
    full_title_tag.text = poa_article.journal_title
    set_issn_tag(journal_metadata_tag, poa_article)


def set_issn_tag(parent, poa_article):
    issn_tag = SubElement(parent, "issn")
    issn_tag.set("media_type", "electronic")
    issn_tag.text = poa_article.journal_issn
