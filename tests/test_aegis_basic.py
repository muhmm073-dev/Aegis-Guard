import importlib
import pytest

def test_import_aegis_guard():
    mod = importlib.import_module("aegis_guard")
    assert hasattr(mod, "main") or hasattr(mod, "__name__")
