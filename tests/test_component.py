import unittest
from elifearticle.article import Component
from elifecrossref import component


class TestComponent(unittest.TestCase):
    def test_do_set_component_permissions_none(self):
        comp = Component()
        self.assertIsNone(component.do_set_component_permissions(comp))

    def test_do_set_component_permissions_false(self):
        comp = Component()
        permission = {}
        comp.permissions = [permission]
        self.assertFalse(component.do_set_component_permissions(comp))
