import pytest
from unittest.mock import call

from f.sift.agents import main
from sift.modules.agents.schema import AgentRequest, AgentResponse
from sift.utils.webhook.schema import Webhook, WebhookEvent


@pytest.fixture
def mock_client(mocker):
    return mocker.patch("f.sift.agents.client")


@pytest.fixture
def mock_dispatch(mocker):
    # Patch the underlying dispatch_webhook function
    return mocker.patch("sift.utils.webhook.service.dispatch_webhook")


@pytest.fixture
def valid_agent_request():
    return AgentRequest(
        agent_name="test_agent",
        agent_card_params={"key": "value"},
        litellm_params={"model": "gpt-4"},
        dspy_params={"state": {}},
        webhook=Webhook(
            url="https://example.com/webhook",
            events=[WebhookEvent.STARTED, WebhookEvent.COMPLETED, WebhookEvent.FAILED],
        ),
    )


def test_main_create_success(mock_client, mock_dispatch, valid_agent_request):
    result = main(valid_agent_request)

    mock_dispatch.assert_has_calls(
        [
            call(
                webhook=valid_agent_request.webhook,
                event=WebhookEvent.STARTED,
                payload=valid_agent_request.model_dump(),
            ),
            call(
                webhook=result.webhook,
                event=WebhookEvent.COMPLETED,
                payload=result.model_dump(),
            ),
        ]
    )

    mock_client.compile_and_save_agent.assert_called_once_with(
        valid_agent_request.model_dump(exclude={"webhook"})
    )

    assert isinstance(result, AgentResponse)
    assert result.success is True
    assert result.error is None
    assert result.agent_name == "test_agent"


def test_main_create_error(mock_client, mock_dispatch, valid_agent_request):
    mock_client.compile_and_save_agent.side_effect = Exception("Compile failed")

    result = main(valid_agent_request)

    mock_dispatch.assert_has_calls(
        [
            call(
                webhook=valid_agent_request.webhook,
                event=WebhookEvent.STARTED,
                payload=valid_agent_request.model_dump(),
            ),
            call(
                webhook=result.webhook,
                event=WebhookEvent.FAILED,
                payload=result.model_dump(),
            ),
        ]
    )

    mock_client.compile_and_save_agent.assert_called_once_with(
        valid_agent_request.model_dump(exclude={"webhook"})
    )

    assert isinstance(result, AgentResponse)
    assert result.success is False
    assert result.error == "Compile failed"
    assert result.agent_name == "test_agent"
