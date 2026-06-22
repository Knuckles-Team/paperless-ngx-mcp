import importlib

import pytest


@pytest.mark.concept("PNGX-001")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:PNGX-001"""
    module = importlib.import_module("paperless_ngx_mcp")
    assert hasattr(module, "__all__")
