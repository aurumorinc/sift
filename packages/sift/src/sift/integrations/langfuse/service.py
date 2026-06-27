from langfuse import Langfuse
from sift.config import settings

_client = None


def get_langfuse_client() -> Langfuse:
    """Returns a configured Langfuse client instance."""
    global _client
    if _client is None:
        _client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )
    return _client
