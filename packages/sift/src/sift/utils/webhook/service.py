from worldline import structlog
from typing import Any, Callable, Dict, Optional
import functools

import httpx

from sift.utils.webhook.schema import Webhook, WebhookEvent

logger = structlog.get_logger(__name__)


def dispatch_webhook(
    webhook: Optional[Webhook], event: WebhookEvent, payload: Dict[str, Any]
) -> None:
    """Trigger an HTTP callback based on the webhook spec."""
    if not webhook:
        return

    if webhook.events and event not in webhook.events:
        return

    request_payload = {"event": event.value, "payload": payload}
    if webhook.metadata:
        request_payload["metadata"] = webhook.metadata

    headers = webhook.headers or {}

    try:
        response = httpx.post(
            str(webhook.url),
            json=request_payload,
            headers=headers,
            timeout=10.0,
        )
        response.raise_for_status()
    except Exception as e:
        logger.warning("Failed to trigger webhook for event %s: %s", event.value, e)


def webhook_dispatch(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""

    @functools.wraps(func)
    def wrapper(request: Any, *args: Any, **kwargs: Any) -> Any:
        webhook = getattr(request, "webhook", None)

        if webhook:
            dispatch_webhook(
                webhook=webhook,
                event=WebhookEvent.STARTED,
                payload=request.model_dump(),
            )

        try:
            response = func(request, *args, **kwargs)
        except Exception as e:
            if webhook:
                payload = request.model_dump()
                payload["error"] = str(e)
                dispatch_webhook(
                    webhook=webhook, event=WebhookEvent.FAILED, payload=payload
                )
            raise e

        success = getattr(response, "success", True)
        event = WebhookEvent.COMPLETED if success else WebhookEvent.FAILED
        if webhook:
            dispatch_webhook(
                webhook=webhook, event=event, payload=response.model_dump()
            )
        return response

    return wrapper
