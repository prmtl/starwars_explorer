import os

import django


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starwars_explorer.settings")
    django.setup()
