import os
import pytest


def filter_response(response):
    """Filter out sensitive data from the response."""
    return response


def _get_vcr_config():
    """Configure VCR to scrub sensitive headers."""
    return {
        "filter_headers": [
            ("authorization", "DUMMY_AUTHORIZATION"),
            ("x-api-key", "DUMMY_API_KEY"),
            ("x-langfuse-public-key", "pk-lf-dummy"),
            ("x-goog-api-key", "DUMMY_GEMINI_API_KEY"),
        ],
        "filter_query_parameters": [
            ("api_key", "DUMMY_API_KEY"),
            ("key", "DUMMY_API_KEY"),
        ],
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "before_record_response": filter_response,
        "record_mode": "once",
    }


@pytest.fixture(scope="module")
def vcr_config():
    """Configure VCR to scrub sensitive headers."""
    return _get_vcr_config()


def _setup_environment():
    """Ensure environment variables are set for dummy/playback if not running live."""
    from dotenv import load_dotenv

    load_dotenv(".env.local", override=True)

    # We require actual keys to record, but if they are missing, we set dummies
    # so that playback works seamlessly without real keys.
    if not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "DUMMY_GEMINI_API_KEY"
    if not os.environ.get("LANGFUSE_SECRET_KEY"):
        os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-dummy"
    if not os.environ.get("LANGFUSE_PUBLIC_KEY"):
        os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-dummy"
    if not os.environ.get("LANGFUSE_BASE_URL"):
        os.environ["LANGFUSE_BASE_URL"] = "https://cloud.langfuse.com"


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    _setup_environment()
