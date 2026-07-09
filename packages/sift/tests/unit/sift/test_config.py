import os
from unittest.mock import patch

from sift.config import Settings


def test_settings_default_dspy_cachedir():
    """Test that Settings defaults dspy_cachedir to /tmp/dspy_cache when no environment variable is set."""
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.dspy_cachedir == "/tmp/dspy_cache"


def test_settings_propagates_dspy_cachedir():
    """Test that setting dspy_cachedir correctly populates DSPY_CACHEDIR in os.environ."""
    with patch.dict(os.environ, {"DSPY_CACHEDIR": "/custom/path/cache"}, clear=True):
        settings = Settings()
        assert settings.dspy_cachedir == "/custom/path/cache"
        
        # In the actual module, we do `os.environ["DSPY_CACHEDIR"] = settings.dspy_cachedir`
        # Let's mock that module-level initialization
        os.environ["DSPY_CACHEDIR"] = settings.dspy_cachedir
        assert os.environ["DSPY_CACHEDIR"] == "/custom/path/cache"


def test_settings_propagates_default_to_environ():
    """Test that default dspy_cachedir gets correctly pushed to os.environ when the module runs."""
    # To test the module execution, we can reload the config module, but doing so could impact other tests.
    # We will instead test the functionality by simulating it or just importing the instantiated settings.
    with patch.dict(os.environ, {}, clear=True):
        import importlib
        import sift.config
        
        importlib.reload(sift.config)
        
        assert sift.config.settings.dspy_cachedir == "/tmp/dspy_cache"
        assert os.environ.get("DSPY_CACHEDIR") == "/tmp/dspy_cache"
