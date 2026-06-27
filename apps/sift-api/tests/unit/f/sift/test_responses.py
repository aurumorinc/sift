import pytest
from unittest.mock import call

from f.sift.responses import main
from sift.modules.responses.schema import ResponseRequest, ResponseResponse
from sift.utils.webhook.schema import Webhook, WebhookEvent


@pytest.fixture
def mock_client(mocker):
    return mocker.patch("f.sift.responses.client")


@pytest.fixture
def mock_dispatch(mocker):
    return mocker.patch("sift.utils.webhook.service.dispatch_webhook")


@pytest.fixture
def valid_response_request():
    return ResponseRequest(
        model="a2a_agent/my-agent",
        input="Hello",
        background=False,
        webhook=Webhook(
            url="https://example.com/webhook",
            events=[WebhookEvent.STARTED, WebhookEvent.COMPLETED, WebhookEvent.FAILED],
        ),
    )


def test_responses_main_success(mock_client, mock_dispatch, valid_response_request):
    mock_response_data = {
        "id": "resp_123",
        "created_at": 1718000000,
        "model": "my-agent",
        "status": "completed",
        "output": [{"content": [{"type": "output_text", "text": "Result"}]}],
        "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
    }
    mock_client.predict_response.return_value = mock_response_data

    result = main(valid_response_request)

    mock_dispatch.assert_has_calls(
        [
            call(
                webhook=valid_response_request.webhook,
                event=WebhookEvent.STARTED,
                payload=valid_response_request.model_dump(),
            ),
            call(
                webhook=result.webhook,
                event=WebhookEvent.COMPLETED,
                payload=result.model_dump(),
            ),
        ]
    )

    mock_client.predict_response.assert_called_once_with("my-agent", "Hello", False)

    assert isinstance(result, ResponseResponse)
    assert result.success is True
    assert result.error is None
    # Just check the key fields to avoid Pydantic default value drift
    assert result.response is not None
    dumped_response = result.response.model_dump(exclude_unset=True)
    assert dumped_response["id"] == mock_response_data["id"]
    assert dumped_response["model"] == mock_response_data["model"]


def test_responses_main_no_prefix(mock_client):
    request = ResponseRequest(
        model="other-agent",
        input=[{"role": "user", "content": "Hi"}],
        background=True,
    )
    mock_response_data = {
        "id": "resp_123",
        "created_at": 1718000000,
        "model": "other-agent",
        "status": "completed",
        "output": [{"content": [{"type": "output_text", "text": "Result"}]}],
        "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
    }
    mock_client.predict_response.return_value = mock_response_data

    result = main(request)

    mock_client.predict_response.assert_called_once_with(
        "other-agent", [{"role": "user", "content": "Hi"}], True
    )

    assert isinstance(result, ResponseResponse)
    assert result.success is True


def test_responses_main_error(mock_client, mock_dispatch, valid_response_request):
    mock_client.predict_response.side_effect = Exception("Prediction failed")

    result = main(valid_response_request)

    mock_dispatch.assert_has_calls(
        [
            call(
                webhook=valid_response_request.webhook,
                event=WebhookEvent.STARTED,
                payload=valid_response_request.model_dump(),
            ),
            call(
                webhook=result.webhook,
                event=WebhookEvent.FAILED,
                payload=result.model_dump(),
            ),
        ]
    )

    mock_client.predict_response.assert_called_once_with("my-agent", "Hello", False)

    assert isinstance(result, ResponseResponse)
    assert result.success is False
    assert result.error == "Prediction failed"
    assert result.response is None
