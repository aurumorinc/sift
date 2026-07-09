from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from pydantic import BaseModel, Field, HttpUrl

if TYPE_CHECKING:
    from sift.modules.agents.schema import AgentResponse
    from sift.modules.responses.schema import ResponseResponse


class WebhookEvent(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class Webhook(BaseModel):
    """A webhook configuration for receiving asynchronous task updates."""

    url: HttpUrl = Field(
        description="The destination URL where event payloads will be sent via POST request."
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="Key-value pairs to be included as HTTP headers (e.g., for authentication or custom identifiers).",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="User-defined key-value data that will be echoed back in every webhook payload.",
    )
    events: Optional[List[WebhookEvent]] = Field(
        default=[
            WebhookEvent.STARTED,
            WebhookEvent.COMPLETED,
            WebhookEvent.FAILED,
        ],
        description="A filter list of specific event types to receive. If omitted, all supported events are sent.",
    )
    data: Optional[Union['AgentResponse', 'ResponseResponse']] = Field(default=None)
