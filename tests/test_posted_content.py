import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifearticle.article import Event
from elifecrossref import posted_content
from tests import create_crossref_config, helpers


class TestSetPostedContent(unittest.TestCase):
    "tests for set_posted_content()"

    def test_set_posted_content(self):
        "test generating posted content output from test fixture data"
        parent = Element("root")
        crossref_config = create_crossref_config("elife_preprint")
        article = helpers.build_preprint_article()
        # add a sent-for-review publication-history event, ignored due to no DOI or URI
        event_object = Event()
        event_object.event_type = "sent-for-review"
        article.publication_history.insert(0, event_object)

        expected = bytes(
            (
                "<root>"
                '<posted_content type="preprint">'
                "<group_title>eLife RP</group_title>"
                "<contributors>"
                '<person_name contributor_role="author" sequence="first">'
                "<given_name>Given names</given_name>"
                "<surname>First</surname>"
                "<affiliations>"
                "<institution>"
                "<institution_name>Department, Institution</institution_name>"
                "<institution_place>City, Country</institution_place>"
                "</institution>"
                "</affiliations>"
                '<ORCID authenticated="false">https://orcid.org/0000-0000-0000-0000</ORCID>'
                "</person_name>"
                '<person_name contributor_role="author" sequence="additional">'
                "<given_name>Given names</given_name>"
                "<surname>Second</surname>"
                "<affiliations>"
                "<institution>"
                "<institution_name>Department, Institution</institution_name>"
                "<institution_place>City, Country</institution_place>"
                "</institution>"
                "</affiliations>"
                "</person_name>"
                "</contributors>"
                "<titles>"
                "<title>"
                "Timely sleep coupling: spindle-slow wave synchrony is linked to early amyloid-β"
                " burden and predicts memory decline"
                "</title>"
                "</titles>"
                "<posted_date>"
                "<month>03</month>"
                "<day>03</day>"
                "<year>2022</year>"
                "</posted_date>"
                "<institution>"
                "<institution_name>eLife</institution_name>"
                '<institution_id type="ror">https://ror.org/04rjz5883</institution_id>'
                "</institution>"
                '<item_number item_number_type="article_number">RP202200001</item_number>'
                "<jats:abstract>"
                "<jats:p>An abstract x2.</jats:p>"
                "</jats:abstract>"
                '<fr:program name="fundref">'
                '<fr:assertion name="fundgroup">'
                '<fr:assertion name="funder_name">Example Funding Institution</fr:assertion>'
                '<fr:assertion name="ror">example_ror_id</fr:assertion>'
                '<fr:assertion name="grant_doi">example_award_id</fr:assertion>'
                "</fr:assertion>"
                "</fr:program>"
                '<ai:program name="AccessIndicators">'
                "<ai:license_ref>http://creativecommons.org/licenses/by/4.0/</ai:license_ref>"
                "</ai:program>"
                "<rel:program>"
                "<rel:related_item>"
                '<rel:intra_work_relation identifier-type="doi" relationship-type="isVersionOf">'
                "10.7554/article_version_with_doi"
                "</rel:intra_work_relation>"
                "</rel:related_item>"
                "<rel:related_item>"
                '<rel:intra_work_relation identifier-type="uri" relationship-type="isVersionOf">'
                "10.7554/article_version_with_uri"
                "</rel:intra_work_relation>"
                "</rel:related_item>"
                "<rel:related_item>"
                '<rel:inter_work_relation identifier-type="doi" relationship-type="isFinancedBy">'
                "example_award_id"
                "</rel:inter_work_relation>"
                "</rel:related_item>"
                "</rel:program>"
                "<version_info>"
                '<version xml:lang="en">2</version>'
                "</version_info>"
                "<doi_data>"
                "<doi>10.7554/eLife.202200001</doi>"
                "<resource>https://example.org/articles/202200001</resource>"
                '<collection property="text-mining">'
                "<item>"
                '<resource mime_type="application/xml">'
                "https://cdn.elifesciences.org/preprints/202200001/elife-preprint-202200001-v2.xml"
                "</resource>"
                "</item>"
                "</collection>"
                '<collection property="crawler-based">'
                '<item crawler="iParadigms">'
                "<resource>https://elifesciences.org/reviewed-preprints/202200001v2/pdf</resource>"
                "</item>"
                "</collection>"
                "</doi_data>"
                "<citation_list>"
                '<citation key="1">'
                "<article_title>An article title</article_title>"
                "</citation>"
                "</citation_list>"
                "</posted_content>"
                "</root>"
            ),
            encoding="utf-8",
        )
        posted_content.set_posted_content(parent, article, crossref_config)
        parent_string = ElementTree.tostring(parent, "utf-8")
        self.assertEqual(parent_string, expected)
