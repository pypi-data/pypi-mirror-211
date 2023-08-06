from django.test import TestCase, override_settings

from pfx.pfxcore.management.commands.makeapidoc import get_spec
from pfx.pfxcore.test import TestAssertMixin


class ApiDocTest(TestAssertMixin, TestCase):
    def test_default_generation(self):
        spec = get_spec().to_dict()
        self.assertEqual(spec['openapi'], "3.0.2")
        info = spec['info']
        self.assertEqual(info['title'], "PFX API")
        self.assertEqual(info['version'], "1.0.0")

    @override_settings(PFX_OPENAPI_TEMPLATE=dict(
        title="MyAPI",
        info=dict(description="A test API")))
    def test_default_customized_generation(self):
        spec = get_spec().to_dict()
        self.assertEqual(spec['openapi'], "3.0.2")
        info = spec['info']
        self.assertEqual(info['title'], "MyAPI")
        self.assertEqual(info['version'], "1.0.0")
        self.assertEqual(info['description'], "A test API")
