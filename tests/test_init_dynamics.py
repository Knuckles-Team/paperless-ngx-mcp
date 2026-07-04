import importlib

import pytest


@pytest.mark.concept("PL-OS.identity.pngx")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:PL-OS.identity.pngx"""
    module = importlib.import_module("paperless_ngx_mcp")
    assert hasattr(module, "__all__")
