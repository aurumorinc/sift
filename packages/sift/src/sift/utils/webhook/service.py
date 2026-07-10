import functools
import inspect
import os
import uuid
from typing import Any, Callable, Dict, Optional

import httpx
from worldline import structlog

from sift.utils.webhook.schema import WebhookRequest, WebhookEvent, WebhookResponse

logger = structlog.get_logger(__name__)


def dispatch_webhook(
    webhook: Optional[WebhookRequest], payload: WebhookResponse
) -> None:
    """Trigger an HTTP callback based on the webhook spec."""
    if not webhook:
        return

    headers = webhook.headers or {}

    try:
        response = httpx.post(
            str(webhook.url),
            json=payload.model_dump(exclude_none=True),
            headers=headers,
            timeout=10.0,
        )
        response.raise_for_status()
    except Exception as e:
        logger.warning("Failed to trigger webhook for event %s: %s", payload.type, e)


def webhook_dispatch(event_prefix: str = "") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            webhook_data = bound_args.arguments.get("webhook")
            webhook = None
            if isinstance(webhook_data, dict):
                webhook = WebhookRequest(**webhook_data)
            elif isinstance(webhook_data, WebhookRequest):
                webhook = webhook_data
                
            job_id = os.getenv("WM_JOB_ID", uuid.uuid4().hex)

            if webhook and (not webhook.events or WebhookEvent.STARTED in webhook.events):
                payload = WebhookResponse(
                    success=True,
                    type=f"{event_prefix}.{WebhookEvent.STARTED.value}",
                    id=job_id,
                    webhookId=uuid.uuid4().hex,
                    data=[],
                    metadata=webhook.metadata
                )
                dispatch_webhook(webhook=webhook, payload=payload)

            try:
                response = func(*args, **kwargs)
            except Exception as e:
                if webhook and (not webhook.events or WebhookEvent.FAILED in webhook.events):
                    payload = WebhookResponse(
                        success=False,
                        type=f"{event_prefix}.{WebhookEvent.FAILED.value}",
                        id=job_id,
                        webhookId=uuid.uuid4().hex,
                        data=[],
                        error=str(e),
                        metadata=webhook.metadata
                    )
                    dispatch_webhook(webhook=webhook, payload=payload)
                raise e

            success = getattr(response, "success", True)
            event = WebhookEvent.COMPLETED if success else WebhookEvent.FAILED
            
            if webhook and (not webhook.events or event in webhook.events):
                if hasattr(response, "output"):
                    data = response.output
                else:
                    data = response.model_dump()
                    data.pop("success", None)
                    data.pop("error", None)
                    data.pop("webhook", None)
                    data = [data]
                
                payload = WebhookResponse(
                    success=success,
                    type=f"{event_prefix}.{event.value}",
                    id=job_id,
                    webhookId=uuid.uuid4().hex,
                    data=data,
                    error=getattr(response, "error", None) if not success else None,
                    metadata=webhook.metadata
                )
                dispatch_webhook(webhook=webhook, payload=payload)
                
            return response
        return wrapper
    return decorator
