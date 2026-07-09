from unittest.mock import patch
import os
import pytest
from tests.conftest import filter_response, vcr_config, setup_environment  # type: ignore


def test_filter_response():
    response = {"body": "secret_data"}
    filtered = filter_response(response)
    assert filtered == {"body": "secret_data"}


def test_vcr_config():
    from tests.conftest import _get_vcr_config  # type: ignore
    config = _get_vcr_config()
    assert "filter_headers" in config
    assert ("authorization", "DUMMY_AUTHORIZATION") in config["filter_headers"]
    assert "filter_query_parameters" in config
    assert "before_record_response" in config


@patch("dotenv.load_dotenv", autospec=True)
@patch.dict(os.environ, clear=True)
def test_setup_environment_sets_dummies(mock_load_dotenv):
    from tests.conftest import _setup_environment  # type: ignore
    _setup_environment()
    assert os.environ["GEMINI_API_KEY"] == "DUMMY_GEMINI_API_KEY"
    assert os.environ["LANGFUSE_SECRET_KEY"] == "sk-lf-dummy"
    assert os.environ["LANGFUSE_PUBLIC_KEY"] == "pk-lf-dummy"
    assert os.environ["LANGFUSE_BASE_URL"] == "https://cloud.langfuse.com"


@patch("dotenv.load_dotenv", autospec=True)
@patch.dict(os.environ, {
    "GEMINI_API_KEY": "real_gemini",
    "LANGFUSE_SECRET_KEY": "real_sk",
    "LANGFUSE_PUBLIC_KEY": "real_pk",
    "LANGFUSE_BASE_URL": "http://real-langfuse"
}, clear=True)
def test_setup_environment_preserves_existing(mock_load_dotenv):
    from tests.conftest import _setup_environment  # type: ignore
    _setup_environment()
    assert os.environ["GEMINI_API_KEY"] == "real_gemini"
    assert os.environ["LANGFUSE_SECRET_KEY"] == "real_sk"
    assert os.environ["LANGFUSE_PUBLIC_KEY"] == "real_pk"
    assert os.environ["LANGFUSE_BASE_URL"] == "http://real-langfuse"
