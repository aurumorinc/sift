import pytest
from unittest.mock import MagicMock, patch
from sift.modules.agents.schema import Agent
from sift.use_cases.agents.service import _deep_merge, main


def test_deep_merge():
    base = {
        "a": 1,
        "b": {"c": 2, "d": 3},
        "e": [1, 2],
    }
    update = {
        "b": {"d": 4, "f": 5},
        "e": [3, 4],  # Lists are overwritten
        "g": 6,
    }
    merged = _deep_merge(base, update)
    assert merged == {
        "a": 1,
        "b": {"c": 2, "d": 4, "f": 5},
        "e": [3, 4],
        "g": 6,
    }


@patch("sift.use_cases.agents.service.client")
@patch("sift.use_cases.agents.service.get_agent_safe")
def test_agents_new_agent(mock_get_agent_safe, mock_client):
    mock_get_agent_safe.return_value = None

    response = main(
        agent_card_params={"desc": "test"},
        litellm_params={"model": "gpt-4"},
        dspy_params={"state": {}},
    )

    assert response.success is True
    # agent_name should have been generated
    assert isinstance(response.agent_name, str)
    assert len(response.agent_name) > 0

    # Ensure empty signature was populated correctly before sending
    mock_client.compile_and_save_agent.assert_called_once()
    payload = mock_client.compile_and_save_agent.call_args[0][0]
    assert payload["agent_name"] == response.agent_name
    assert payload["agent_card_params"] == {"desc": "test"}


@patch("sift.use_cases.agents.service.client")
@patch("sift.use_cases.agents.service.get_agent_safe")
def test_agents_existing_agent_merge(mock_get_agent_safe, mock_client):
    # Setup the mock existing agent
    existing_agent = Agent(
        agent_name="existing-agent",
        agent_card_params={"old": "param"},
        litellm_params={"model": "gpt-3.5"},
        dspy_params={
            "optimizer": "old_opt",
            "state": {
                "predict": {
                    "signature": {"instructions": "old", "fields": []},
                    "train": [{"q": "old", "a": "old"}],
                    "traces": [],
                    "demos": []
                }
            }
        },
    )
    mock_get_agent_safe.return_value = existing_agent

    # Provide only litellm_params and optimizer to override
    response = main(
        agent_name="existing-agent",
        litellm_params={"model": "gpt-4"},
        dspy_params={"optimizer": "new_opt"},
    )

    assert response.success is True
    assert response.agent_name == "existing-agent"

    mock_client.compile_and_save_agent.assert_called_once()
    payload = mock_client.compile_and_save_agent.call_args[0][0]

    # Verify litellm_params and optimizer were updated
    assert payload["litellm_params"]["model"] == "gpt-4"
    assert payload["dspy_params"]["optimizer"] == "new_opt"

    # Verify other fields were retained
    assert payload["agent_card_params"] == {"old": "param"}
    # model_dump includes default optional fields like trace_id, score, feedback
    train_example = payload["dspy_params"]["state"]["predict"]["train"][0]
    assert train_example["q"] == "old"
    assert train_example["a"] == "old"
    assert payload["dspy_params"]["state"]["predict"]["signature"]["instructions"] == "old"


@patch("sift.use_cases.agents.service.client")
@patch("sift.use_cases.agents.service.get_agent_safe")
@patch("sift.utils.webhook.service.dispatch_webhook")
def test_agents_main_optional_args_populated(mock_dispatch_webhook, mock_get_agent_safe, mock_client):
    mock_get_agent_safe.return_value = None

    response = main(
        agent_name="test_opts",
        agent_card_params={},
        litellm_params={},
        dspy_params={"state": {}},
        object_permission={"read": True},
        labels=["test_label"],
        webhook={"url": "http://example.com/hook"}
    )

    assert response.success is True
    mock_client.compile_and_save_agent.assert_called_once()
    payload = mock_client.compile_and_save_agent.call_args[0][0]
    
    assert payload.get("object_permission") == {"read": True}
    assert payload.get("labels") == ["test_label"]
    # Webhook is excluded from the payload sent to compile_and_save_agent
    assert "webhook" not in payload
    assert not hasattr(response, "webhook")


@patch("sift.use_cases.agents.service.client")
@patch("sift.use_cases.agents.service.get_agent_safe")
@patch("sift.utils.webhook.service.dispatch_webhook")
def test_agents_main_catches_exception(mock_dispatch_webhook, mock_get_agent_safe, mock_client):
    mock_get_agent_safe.return_value = None
    mock_client.compile_and_save_agent.side_effect = RuntimeError("Mocked compilation error")

    response = main(
        agent_name="error_test",
        agent_card_params={},
        litellm_params={},
        dspy_params={"state": {}},
        webhook={"url": "http://example.com/hook"}
    )

    assert response.success is False
    assert response.error == "Mocked compilation error"
    assert not hasattr(response, "webhook")
