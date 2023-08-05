import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_load_initial_conftests(early_config, parser, args):
    try:
        from django.db import models
    except ImportError:
        pass
    else:
        models.FileField.storage = property(
            lambda obj: obj._storage,
            lambda obj, value: setattr(obj, "_storage", value),
            lambda obj: delattr(obj, "_storage"),
        )

    yield
