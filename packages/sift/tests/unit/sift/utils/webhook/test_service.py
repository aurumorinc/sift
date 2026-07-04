import pytest
import httpx
from unittest.mock import patch, MagicMock
from typing import Optional

from sift.utils.webhook.schema import Webhook, WebhookEvent
from sift.utils.webhook.service import dispatch_webhook, webhook_dispatch


@pytest.fixture
def webhook():
    return Webhook(
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

        payload = {"data": "test"}
        dispatch_webhook(webhook, WebhookEvent.STARTED, payload)

        mock_post.assert_called_once_with(
            "https://example.com/webhook",
            json={
                "event": "started",
                "payload": payload,
                "metadata": {"user_id": "123"},
            },
            headers={"Authorization": "Bearer token"},
            timeout=10.0,
        )
        mock_response.raise_for_status.assert_called_once()


def test_dispatch_webhook_no_webhook():
    with patch("httpx.post") as mock_post:
        dispatch_webhook(None, WebhookEvent.STARTED, {"data": "test"})
        mock_post.assert_not_called()


def test_dispatch_webhook_event_not_in_list(webhook):
    with patch("httpx.post") as mock_post:
        dispatch_webhook(webhook, WebhookEvent.FAILED, {"data": "test"})
        mock_post.assert_not_called()


def test_dispatch_webhook_http_error(webhook, caplog):
    with patch("httpx.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock()
        )
        mock_post.return_value = mock_response

        dispatch_webhook(webhook, WebhookEvent.STARTED, {"data": "test"})

        assert "Failed to trigger webhook for event %s: %s" in caplog.text


# tests for webhook_dispatch decorator


class MockResponse:
    def __init__(self, success=True, data="resp_data"):
        self.success = success
        self.data = data

    def model_dump(self):
        return {"data": self.data, "success": self.success}


@webhook_dispatch
def dummy_success_func(data: str, webhook: Optional[dict] = None):
    return MockResponse(success=True)


@webhook_dispatch
def dummy_failure_func(data: str, webhook: Optional[dict] = None):
    return MockResponse(success=False)


@webhook_dispatch
def dummy_exception_func(data: str, webhook: Optional[dict] = None):
    raise ValueError("dummy error")


def test_webhook_dispatch_success(webhook):
    webhook_dict = webhook.model_dump()
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_success_func(data="req_data", webhook=webhook_dict)

        assert response.success is True
        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url
        assert started_call.kwargs["event"] == WebhookEvent.STARTED
        assert started_call.kwargs["payload"] == {"data": "req_data", "webhook": webhook_dict}

        completed_call = mock_dispatch.call_args_list[1]
        assert completed_call.kwargs["webhook"].url == webhook.url
        assert completed_call.kwargs["event"] == WebhookEvent.COMPLETED
        assert completed_call.kwargs["payload"] == {"data": "resp_data", "success": True}


def test_webhook_dispatch_handled_failure(webhook):
    webhook_dict = webhook.model_dump()
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_failure_func(data="req_data", webhook=webhook_dict)

        assert response.success is False
        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url
        assert started_call.kwargs["event"] == WebhookEvent.STARTED
        assert started_call.kwargs["payload"] == {"data": "req_data", "webhook": webhook_dict}

        failed_call = mock_dispatch.call_args_list[1]
        assert failed_call.kwargs["webhook"].url == webhook.url
        assert failed_call.kwargs["event"] == WebhookEvent.FAILED
        assert failed_call.kwargs["payload"] == {"data": "resp_data", "success": False}


def test_webhook_dispatch_unhandled_exception(webhook):
    webhook_dict = webhook.model_dump()
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        with pytest.raises(ValueError, match="dummy error"):
            dummy_exception_func(data="req_data", webhook=webhook_dict)

        assert mock_dispatch.call_count == 2
        
        started_call = mock_dispatch.call_args_list[0]
        assert started_call.kwargs["webhook"].url == webhook.url
        assert started_call.kwargs["event"] == WebhookEvent.STARTED
        assert started_call.kwargs["payload"] == {"data": "req_data", "webhook": webhook_dict}

        failed_call = mock_dispatch.call_args_list[1]
        assert failed_call.kwargs["webhook"].url == webhook.url
        assert failed_call.kwargs["event"] == WebhookEvent.FAILED
        assert failed_call.kwargs["payload"] == {"data": "req_data", "webhook": webhook_dict, "error": "dummy error"}


def test_webhook_dispatch_no_webhook():
    with patch("sift.utils.webhook.service.dispatch_webhook") as mock_dispatch:
        response = dummy_success_func(data="req_data", webhook=None)

        assert response.success is True
        mock_dispatch.assert_not_called()
