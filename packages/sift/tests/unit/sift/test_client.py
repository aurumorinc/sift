from sift.client import SiftClient
from sift.config import settings


def test_sift_client_initialization_overrides_settings() -> None:
    _ = SiftClient(langfuse_public_key="test_public_key", langfuse_secret_key="test_secret")
    assert settings.langfuse_public_key == "test_public_key"
    assert settings.langfuse_secret_key == "test_secret"


def test_sift_client_routing_properties(mocker) -> None:
    client = SiftClient()
    assert hasattr(client, "get_agent")
    assert hasattr(client, "compile_and_save_agent")

    mock_get_agent = mocker.patch(
        "sift.modules.agents.repository.langfuse.get_agent", return_value="dummy_agent"
    )
    result = client.get_agent("test", 1)
    mock_get_agent.assert_called_once_with("test", 1)
    assert result == "dummy_agent"
