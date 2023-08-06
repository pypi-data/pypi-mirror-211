import inspect
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from apispec import APISpec
from apispec.utils import deepupdate
from apispec.yaml_utils import load_operations_from_docstring

from pfx.pfxcore import __PFX_VIEWS__
from pfx.pfxcore.settings import PFXSettings
from pfx.pfxcore.views import ModelMixin

settings = PFXSettings()
DEFAULT_TEMPLATE = dict(
    title="PFX API",
    version="1.0.0",
    openapi_version="3.0.2")


def get_operations(view, url):
    for op, method_name in url['methods'].items():
        doc = inspect.getdoc(getattr(view, method_name))
        vars = {}
        if issubclass(view, ModelMixin) and view.model:
            vars.update(
                model=view.model._meta.verbose_name.lower(),
                models=view.model._meta.verbose_name_plural.lower())
        if doc:
            doc = doc.format(**vars)
        spec = deepupdate(
            load_operations_from_docstring(doc).get(op, {}),
            view.rest_doc.get(url['path'], {}))
        spec.setdefault('summary', url['path'])
        yield op, spec


def get_spec():
    spec = APISpec(**{**DEFAULT_TEMPLATE, **settings.PFX_OPENAPI_TEMPLATE})
    for view in __PFX_VIEWS__:
        for url in view.get_urls():
            spec.path(
                path=url['path'],
                operations=dict(get_operations(view, url)))
    return spec


class Command(BaseCommand):
    help = 'Generate OpenAPI documentation'

    def handle(self, *args, **options):
        spec = get_spec()

        path = Path(settings.PFX_OPENAPI_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as outfile:
            json.dump(spec.to_dict(), outfile, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"OpenAPI documentation generated: {path}"))
