from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict
from litellm.types.llms.openai import (
    ResponseOutputItem,
    ResponsesAPIResponse,
    ResponseAPIUsage,
)

from sift.utils.webhook.schema import Webhook

__all__ = [
    "ResponseRequest",
    "ResponseResponse",
    "ResponsesAPIResponse",
    "ResponseAPIUsage",
    "ResponseOutputItem",
]


class ResponseRequest(BaseModel):
    model: str
    input: Union[str, List[Dict[str, Any]]]
    background: Optional[bool] = False
    webhook: Optional[Webhook] = None


class ResponseResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    response: Optional[ResponsesAPIResponse] = None
    webhook: Optional[Webhook] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
