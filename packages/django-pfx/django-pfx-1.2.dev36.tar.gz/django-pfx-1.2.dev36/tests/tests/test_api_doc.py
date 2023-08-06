from django.test import TestCase, override_settings

from pfx.pfxcore.management.commands.makeapidoc import get_spec
from pfx.pfxcore.test import TestAssertMixin
from tests.views import AuthorRestView


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

    def test_view_get_urls(self):
        def get_methods(url, p):
            return next(filter(lambda u: u['path'] == p, urls))['methods']

        urls = AuthorRestView.get_urls()

        # Methods from RestView
        self.assertEqual(
            get_methods(urls, 'authors'),
            dict(get='get_list', post='post'))
        self.assertEqual(
            get_methods(urls, 'authors/<int:id>'),
            dict(delete='delete', get='get', put='put'))
        # A method from SlugDetailRestViewMixin
        self.assertEqual(
            get_methods(urls, 'authors/slug/<slug:slug>'),
            dict(get='get_by_slug'))
        # A method from AuthorRestView itself
        self.assertEqual(
            get_methods(urls, 'authors/cache/<int:id>'),
            dict(get='cache_get'))
