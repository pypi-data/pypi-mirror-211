import json
from pathlib import Path

from django.core.management.base import BaseCommand

from apispec import APISpec

from pfx.pfxcore import __PFX_VIEWS__
from pfx.pfxcore.settings import PFXSettings

settings = PFXSettings()
DEFAULT_TEMPLATE = dict(
    title="PFX API",
    version="1.0.0",
    openapi_version="3.0.2")


def get_spec():
    spec = APISpec(**{**DEFAULT_TEMPLATE, **settings.PFX_OPENAPI_TEMPLATE})
    for view in __PFX_VIEWS__:
        for url in view.get_urls():
            spec.path(
                path=url['path'],
                operations={k: {} for k, v in url['methods'].items()})
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
