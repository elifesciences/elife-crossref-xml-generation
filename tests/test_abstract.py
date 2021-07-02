import unittest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from elifecrossref import abstract


class TestConvertSecTags(unittest.TestCase):
    def test_convert_sec_tags(self):
        string = (
            '<sec id="s1"><title content-type="sub">Section title:</title>'
            "<p>Paragraph.</p></sec>"
        )
        expected = '<jats:p content-type="sub">Section title:</jats:p><p>Paragraph.</p>'
        self.assertEqual(abstract.convert_sec_tags(string), expected)


class TestGetJatsAbstract(unittest.TestCase):
    def test_get_jats_abstract(self):
        string = (
            "<abstract>"
            '<sec id="s1"><title content-type="sub">Section title:</title>'
            "<p>Paragraph.</p></sec>"
            "</abstract>"
        )
        expected = (
            '<jats:sec id="s1"><jats:title content-type="sub">Section title:</jats:title>'
            "<jats:p>Paragraph.</jats:p></jats:sec>"
        )
        self.assertEqual(abstract.get_jats_abstract(string), expected)

    def test_get_jats_abstract_namespace(self):
        string = (
            "<abstract>"
            "<p>Paragraph</p>"
            "<p><bold>DOI:</bold>"
            '<ext-link ext-link-type="doi" xlink:href="10.7554/eLife.15272.001">'
            "https://doi.org/10.7554/eLife.15272.001</ext-link></p>"
            "</abstract>"
        )
        expected = (
            "<jats:p>Paragraph</jats:p><jats:p><jats:bold>DOI:</jats:bold>"
            '<jats:ext-link ext-link-type="doi" xlink:href="10.7554/eLife.15272.001">'
            "https://doi.org/10.7554/eLife.15272.001</jats:ext-link></jats:p>"
        )
        self.assertEqual(abstract.get_jats_abstract(string), expected)


class TestSetAbstractTag(unittest.TestCase):
    def test_set_abstract_tag(self):
        parent = Element("root")
        string = (
            "<abstract>"
            '<sec id="s1"><title content-type="sub">Section title:</title>'
            "<p>Paragraph.</p></sec>"
            "</abstract>"
        )
        jats_abstract = False
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b"<jats:abstract>"
            b'<jats:p content-type="sub">Section title:</jats:p>'
            b"<jats:p>Paragraph.</jats:p>"
            b"</jats:abstract>"
            b"</root>"
        )
        abstract.set_abstract_tag(parent, string, jats_abstract=jats_abstract)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_set_abstract_tag_jats(self):
        parent = Element("root")
        string = (
            "<abstract>"
            '<sec id="s1"><title content-type="sub">Section title:</title>'
            "<p>Paragraph.</p></sec>"
            "</abstract>"
        )
        jats_abstract = True
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b"<jats:abstract>"
            b'<jats:sec id="s1">'
            b'<jats:title content-type="sub">Section title:</jats:title>'
            b"<jats:p>Paragraph.</jats:p>"
            b"</jats:sec>"
            b"</jats:abstract>"
            b"</root>"
        )
        abstract.set_abstract_tag(parent, string, jats_abstract=jats_abstract)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_set_abstract_tag_mathml(self):
        parent = Element("root")
        string = (
            "<abstract>"
            "<p>This is the abstract."
            "<inline-formula><mml:math><mml:mn>0</mml:mn></mml:math></inline-formula>"
            "</p></abstract>"
        )
        jats_abstract = False
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<jats:abstract xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            b'<jats:p xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            b"This is the abstract."
            b"<mml:math><mml:mn>0</mml:mn></mml:math>"
            b"</jats:p>"
            b"</jats:abstract>"
            b"</root>"
        )
        abstract.set_abstract_tag(parent, string, jats_abstract=jats_abstract)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)

    def test_set_abstract_tag_nested_ext_link(self):
        parent = Element("root")
        string = (
            "<abstract>"
            "<p>Paragraph</p>"
            "<p><bold>"
            '<ext-link ext-link-type="doi" xlink:href="10.7554/eLife.15272.001">'
            "https://doi.org/10.7554/eLife.15272.001</ext-link></bold></p>"
            "</abstract>"
        )
        jats_abstract = True
        expected = (
            b"<?xml version='1.0' encoding='utf8'?>\n"
            b"<root>"
            b'<jats:abstract xmlns:xlink="http://www.w3.org/1999/xlink">'
            b"<jats:p>Paragraph</jats:p>"
            b'<jats:p xmlns:xlink="http://www.w3.org/1999/xlink"><jats:bold>'
            b'<jats:ext-link ext-link-type="doi" xlink:href="10.7554/eLife.15272.001">'
            b"https://doi.org/10.7554/eLife.15272.001</jats:ext-link>"
            b"</jats:bold></jats:p>"
            b"</jats:abstract>"
            b"</root>"
        )
        abstract.set_abstract_tag(parent, string, jats_abstract=jats_abstract)
        parent_string = ElementTree.tostring(parent, "utf8")
        self.assertEqual(parent_string, expected)
