import functools
import inspect
from typing import Any, Callable, Dict, Optional

import httpx
from worldline import structlog

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
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        webhook_data = bound_args.arguments.get("webhook")
        webhook = None
        if isinstance(webhook_data, dict):
            webhook = Webhook(**webhook_data)
        elif isinstance(webhook_data, Webhook):
            webhook = webhook_data

        if webhook:
            dispatch_webhook(
                webhook=webhook,
                event=WebhookEvent.STARTED,
                payload=bound_args.arguments,
            )

        try:
            response = func(*args, **kwargs)
        except Exception as e:
            if webhook:
                payload = dict(bound_args.arguments)
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
