import pytest
import httpx
from unittest.mock import patch, MagicMock, ANY
from typing import Optional
import uuid

from sift.utils.webhook.schema import WebhookRequest, WebhookEvent, WebhookResponse
from sift.utils.webhook.service import dispatch_webhook, webhook_dispatch


@pytest.fixture
def webhook():
    return WebhookRequest(
        url="https://example.com/webhook",
        headers={"Authorization": "Bearer token"},
        metadata={"user_id": "123"},
        events=[WebhookEvent.STARTED, WebhookEvent.COMPLETED],
    )


def test_dispatch_webhook_success(webhook):
    with patch("httpx.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = WebhookResponse(
            success=True,
            type="agent.started",
            id="12345",
            webhookId="uuid-1234",
            data=[],
            metadata=webhook.metadata
        )
        dispatch_webhook(webhook, payload)

        mock_post.assert_called_once_with(
            "https://example.com/webhook",
            json={
                "success": True,
                "type": "agent.started",
                "id": "12345",
                "webhookId": "uuid-1234",
                "data": [],
                "metadata": {"user_id": "123"},
            },
            headers={"Authorization": "Bearer token"},
            timeout=10.0,
        )
        mock_response.raise_for_status.assert_called_once()


def test_dispatch_webhook_no_webhook():
    with patch("httpx.post") as mock_post:
        payload = WebhookResponse(
            success=True,
            type="agent.started",
            id="12345",
            webhookId="uuid-1234",
            data=[]
        )
        dispatch_webhook(None, payload)
        mock_post.assert_not_called()


def test_dispatch_webhook_http_error(webhook, caplog):
    with patch("httpx.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock()
        )
        mock_post.return_value = mock_response
        payload = WebhookResponse(
            success=True,
            type="agent.started",
            id="12345",
            webhookId="uuid-1234",
            data=[]
        )
        dispatch_webhook(webhook, payload)

        assert "Failed to trigger webhook for event" in caplog.text
        assert "agent.started" in caplog.text


# tests for webhook_dispatch decorator


class MockResponse:
    def __init__(self, success=True, data="resp_data"):
        self.success = success
        self.data = data

    def model_dump(self):
        return {"data": self.data, "success": self.success}


@webhook_dispatch(event_prefix="test")
def dummy_success_func(data: str, webhook: Optional[dict] = None):
    return MockResponse(success=True)


@webhook_dispatch(event_prefix="test")
def dummy_failure_func(data: str, webhook: Optional[dict] = None):
    return MockResponse(success=False)


@webhook_dispatch(event_prefix="test")
def dummy_exception_func(data: str, webhook: Optional[dict] = None):
    raise ValueError("dummy error")


@patch("uuid.uuid4")
@patch("os.getenv")
def test_webhook_dispatch_success(mock_getenv, mock_uuid4, webhook):
    mock_getenv.return_value = "job-123"
    mock_uuid4.return_value.hex = "webhook-uuid"
    webhook_dict = webhook.model_dump()
    
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_success_func(data="req_data", webhook=webhook_dict)

        assert response.success is True
        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url
        payload = started_call.kwargs["payload"]
        assert payload.type == "test.started"
        assert payload.success is True
        assert payload.id == "job-123"
        assert payload.webhookId == "webhook-uuid"
        assert payload.data == []
        assert payload.metadata == webhook.metadata

        completed_call = mock_dispatch.call_args_list[1]
        assert completed_call.kwargs["webhook"].url == webhook.url
        payload = completed_call.kwargs["payload"]
        assert payload.type == "test.completed"
        assert payload.success is True
        assert payload.id == "job-123"
        assert payload.webhookId == "webhook-uuid"
        assert payload.data == [{"data": "resp_data"}]
        assert payload.metadata == webhook.metadata


@patch("uuid.uuid4")
@patch("os.getenv")
def test_webhook_dispatch_handled_failure(mock_getenv, mock_uuid4, webhook):
    mock_getenv.return_value = "job-123"
    mock_uuid4.return_value.hex = "webhook-uuid"
    webhook.events = [WebhookEvent.STARTED, WebhookEvent.FAILED]
    webhook_dict = webhook.model_dump()
    
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_failure_func(data="req_data", webhook=webhook_dict)

        assert response.success is False
        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url
        payload = started_call.kwargs["payload"]
        assert payload.type == "test.started"
        assert payload.success is True
        assert payload.id == "job-123"

        failed_call = mock_dispatch.call_args_list[1]
        assert failed_call.kwargs["webhook"].url == webhook.url
        payload = failed_call.kwargs["payload"]
        assert payload.type == "test.failed"
        assert payload.success is False
        assert payload.data == [{"data": "resp_data"}]


@patch("uuid.uuid4")
@patch("os.getenv")
def test_webhook_dispatch_unhandled_exception(mock_getenv, mock_uuid4, webhook):
    mock_getenv.return_value = "job-123"
    mock_uuid4.return_value.hex = "webhook-uuid"
    webhook.events = [WebhookEvent.STARTED, WebhookEvent.FAILED]
    webhook_dict = webhook.model_dump()
    
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        with pytest.raises(ValueError, match="dummy error"):
            dummy_exception_func(data="req_data", webhook=webhook_dict)

        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url
        payload = started_call.kwargs["payload"]
        assert payload.type == "test.started"

        failed_call = mock_dispatch.call_args_list[1]
        assert failed_call.kwargs["webhook"].url == webhook.url
        payload = failed_call.kwargs["payload"]
        assert payload.type == "test.failed"
        assert payload.success is False
        assert payload.data == []
        assert payload.error == "dummy error"


def test_webhook_dispatch_no_webhook():
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_success_func(data="req_data", webhook=None)

        assert response.success is True
        mock_dispatch.assert_not_called()

def test_webhook_dispatch_webhook_object(webhook):
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_success_func(data="req_data", webhook=webhook)

        assert response.success is True
        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url

class MockResponseWithOutput:
    def __init__(self, success=True, output=[{"result": "ok"}]):
        self.success = success
        self.output = output

@webhook_dispatch(event_prefix="test")
def dummy_output_func(data: str, webhook: Optional[dict] = None):
    return MockResponseWithOutput()

def test_webhook_dispatch_with_output(webhook):
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_output_func(data="req_data", webhook=webhook)

        assert response.success is True
        assert mock_dispatch.call_count == 2
        
        completed_call = mock_dispatch.call_args_list[1]
        payload = completed_call.kwargs["payload"]
        assert payload.data == [{"result": "ok"}]
