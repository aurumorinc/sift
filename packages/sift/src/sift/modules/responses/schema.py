from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict
from litellm.types.llms.openai import (
    ResponseOutputItem,
    ResponsesAPIResponse,
    ResponseAPIUsage,
    ResponsesAPIOptionalRequestParams,
    ResponsesAPIRequestParams,
)

from oort.webhook.schema import WebhookRequest

__all__ = [
    "ResponseRequest",
    "ResponseResponse",
    "ResponsesAPIResponse",
    "ResponseAPIUsage",
    "ResponseOutputItem",
    "ResponsesAPIOptionalRequestParams",
    "ResponsesAPIRequestParams",
]


class ResponseRequest(BaseModel):
    model: str
    input: Union[str, List[Dict[str, Any]]]
    background: Optional[bool] = False
    webhook: Optional[WebhookRequest] = None

    # LiteLLM ResponsesAPIOptionalRequestParams
    text: Optional[Dict[str, Any]] = None
    instructions: Optional[str] = None
    max_output_tokens: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    parallel_tool_calls: Optional[bool] = None
    previous_response_id: Optional[str] = None
    reasoning: Optional[Dict[str, Any]] = None
    store: Optional[bool] = None
    stream: Optional[bool] = None
    temperature: Optional[float] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    top_p: Optional[float] = None
    truncation: Optional[Dict[str, Any]] = None
    user: Optional[str] = None
    service_tier: Optional[str] = None
    safety_identifier: Optional[str] = None
    prompt: Optional[str] = None
    max_tool_calls: Optional[int] = None
    prompt_cache_key: Optional[str] = None
    prompt_cache_retention: Optional[int] = None
    stream_options: Optional[Dict[str, Any]] = None
    top_logprobs: Optional[int] = None
    partial_images: Optional[bool] = None
    context_management: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(extra="allow")


class ResponseResponse(ResponsesAPIResponse):
    success: bool
    error: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
