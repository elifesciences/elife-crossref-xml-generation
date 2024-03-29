import time
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, Comment
from xml.dom import minidom

from elifearticle import utils as eautils
from elifearticle import parse

from elifecrossref import body, elife, head, utils

from elifecrossref.conf import raw_config, parse_raw_config


TMP_DIR = "tmp"


class CrossrefXML:
    def __init__(
        self,
        poa_articles,
        crossref_config,
        pub_date=None,
        add_comment=True,
        submission_type="journal",
    ):
        """
        Set the root node
        set default values for dates and batch id
        then build out the XML using the article objects
        """
        # Create the root XML node
        self.root = Element("doi_batch")
        set_root(self.root, crossref_config.get("crossref_schema_version"))

        # Publication date
        if pub_date is None:
            self.pub_date = time.gmtime()
        else:
            self.pub_date = pub_date

        self.batch_id = get_batch_id(
            crossref_config.get("batch_file_prefix"),
            self.pub_date,
            poa_articles,
            submission_type,
        )

        # set comment
        if add_comment:
            self.generated = time.strftime("%Y-%m-%d %H:%M:%S")
            last_commit = eautils.get_last_commit_to_master()
            comment = Comment(
                "generated by "
                + str(crossref_config.get("generator"))
                + " at "
                + self.generated
                + " from version "
                + last_commit
            )
            self.root.append(comment)

        # Build out the Crossref XML
        self.build(poa_articles, crossref_config, submission_type)

    def build(self, poa_articles, crossref_config, submission_type):
        head.set_head(self.root, self.batch_id, self.pub_date, crossref_config)
        body.set_body(
            self.root, poa_articles, crossref_config, self.pub_date, submission_type
        )

    def output_xml(self, pretty=False, indent=""):
        encoding = "utf-8"

        rough_string = ElementTree.tostring(self.root, encoding)
        reparsed = minidom.parseString(rough_string)

        if pretty is True:
            return reparsed.toprettyxml(indent, encoding=encoding).decode(encoding)
        return reparsed.toxml(encoding=encoding).decode(encoding)


def set_root(root, schema_version):
    """Set the root tag namespaces and schema details

    :param root: ElementTree.Element tag
    :param schema_version: version of the Crossref schema as a string, e.g. 4.4.1
    """
    root.set("version", schema_version)
    root.set("xmlns", "http://www.crossref.org/schema/%s" % schema_version)
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:fr", "http://www.crossref.org/fundref.xsd")
    root.set("xmlns:ai", "http://www.crossref.org/AccessIndicators.xsd")
    if schema_version != "4.3.5":
        root.set("xmlns:ct", "http://www.crossref.org/clinicaltrials.xsd")
        root.set("xmlns:rel", "http://www.crossref.org/relations.xsd")
    schema_location_name = "http://www.crossref.org/schema/%s" % schema_version
    schema_location_uri = (
        "http://www.crossref.org/schemas/crossref%s.xsd" % schema_version
    )
    root.set(
        "xsi:schemaLocation", "%s %s" % (schema_location_name, schema_location_uri)
    )
    root.set("xmlns:mml", "http://www.w3.org/1998/Math/MathML")
    root.set("xmlns:jats", "http://www.ncbi.nlm.nih.gov/JATS1")


def get_batch_id(batch_file_prefix, pub_date, poa_articles, submission_type):
    """generate a doi_batch_id value for the Crossref deposit"""
    batch_id_parts = []
    # add detail about submission type
    if submission_type != "journal":
        batch_id_parts.append(submission_type)
    # add detail about articles
    if poa_articles:
        # If only one article is supplied, then add the doi to the batch file name
        batch_id_parts.append(str(utils.clean_string(poa_articles[0].manuscript)))
        if (
            submission_type == "posted_content"
            or poa_articles[0].article_type == "preprint"
        ):
            # add version
            version_string = elife.elife_style_article_url_version(poa_articles[0])
            if version_string:
                batch_id_parts.append(version_string)
    # add detail about the date
    batch_id_parts.append(time.strftime("%Y%m%d%H%M%S", pub_date))
    # concatenate and return the final batch id
    return str(batch_file_prefix) + "-".join([part for part in batch_id_parts if part])


def build_crossref_xml(
    poa_articles,
    crossref_config=None,
    pub_date=None,
    add_comment=True,
    submission_type="journal",
):
    """
    Given a list of article article objects
    generate crossref XML from them
    """
    if not crossref_config:
        crossref_config = parse_raw_config(raw_config(None))
    return CrossrefXML(
        poa_articles, crossref_config, pub_date, add_comment, submission_type
    )


def crossref_xml(
    poa_articles,
    crossref_config=None,
    pub_date=None,
    add_comment=True,
    submission_type="journal",
    pretty=False,
    indent="",
):
    """build crossref xml and return output as a string"""
    if not crossref_config:
        crossref_config = parse_raw_config(raw_config(None))
    c_xml = build_crossref_xml(
        poa_articles, crossref_config, pub_date, add_comment, submission_type
    )
    return c_xml.output_xml(pretty=pretty, indent=indent)


def crossref_xml_to_disk(
    poa_articles,
    crossref_config=None,
    pub_date=None,
    add_comment=True,
    submission_type="journal",
    pretty=False,
    indent="",
):
    """build crossref xml and write the output to disk"""
    if not crossref_config:
        crossref_config = parse_raw_config(raw_config(None))
    c_xml = build_crossref_xml(
        poa_articles, crossref_config, pub_date, add_comment, submission_type
    )
    xml_string = c_xml.output_xml(pretty=pretty, indent=indent)
    # Write to file
    filename = TMP_DIR + os.sep + c_xml.batch_id + ".xml"
    with open(filename, "wb") as open_file:
        open_file.write(xml_string.encode("utf-8"))


def build_articles_for_crossref(article_xmls, detail="full", build_parts=None):
    """specify some detail and build_parts specific to generating crossref output"""
    build_parts = [
        "abstract",
        "basic",
        "components",
        "contributors",
        "categories",
        "funding",
        "datasets",
        "license",
        "pub_dates",
        "references",
        "related_articles",
        "volume",
        "sub_articles",
        "history",
        "is_poa",
    ]
    return build_articles(article_xmls, detail, build_parts)


def build_articles(article_xmls, detail="full", build_parts=None):
    return parse.build_articles_from_article_xmls(article_xmls, detail, build_parts)
