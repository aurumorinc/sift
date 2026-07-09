import copy
import uuid
from typing import Dict, List, Optional

from worldline import structlog

from sift.client import SiftClient
from sift.modules.agents.repository.langfuse import get_agent_safe
from sift.modules.agents.schema import AgentRequest, AgentResponse
from sift.utils.webhook.service import webhook_dispatch

logger = structlog.get_logger(__name__)

client = SiftClient()


def _deep_merge(base: Dict, update: Dict) -> Dict:
    """Deep merge `update` into `base` dict."""
    for k, v in update.items():
        if isinstance(v, dict) and k in base and isinstance(base[k], dict):
            base[k] = _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


@webhook_dispatch
def main(
    agent_name: Optional[str] = None,
    agent_card_params: Optional[Dict] = None,
    litellm_params: Optional[Dict] = None,
    dspy_params: Optional[Dict] = None,
    object_permission: Optional[Dict] = None,
    labels: Optional[List] = None,
    webhook: Optional[Dict] = None,
) -> AgentResponse:
    """Create/compile agents and trigger webhooks."""
    if not agent_name:
        agent_name = uuid.uuid4().hex

    existing_agent = get_agent_safe(agent_name)
    existing_agent_dict = existing_agent.model_dump() if existing_agent else {
        "signature": {"instructions": "", "fields": []}
    }

    from typing import Any
    overrides: Dict[str, Any] = {"agent_name": agent_name}
    if agent_card_params is not None:
        overrides["agent_card_params"] = agent_card_params
    if litellm_params is not None:
        overrides["litellm_params"] = litellm_params
    if dspy_params is not None:
        overrides["dspy_params"] = dspy_params
    if object_permission is not None:
        overrides["object_permission"] = object_permission
    if labels is not None:
        overrides["labels"] = labels
    if webhook is not None:
        overrides["webhook"] = webhook

    merged_payload = _deep_merge(copy.deepcopy(existing_agent_dict), overrides)

    request = AgentRequest(**merged_payload)

    webhook_url = str(request.webhook.url) if request.webhook else None
    logger.info("processing_agent_request", webhook_url=webhook_url)

    try:
        client.compile_and_save_agent(request.model_dump(exclude={"webhook"}))
        response = AgentResponse(
            **request.model_dump(exclude={"webhook"}),
            webhook=request.webhook,
            success=True,
            error=None,
        )
        logger.info("agent_processing_completed")
        return response
    except Exception as e:
        error_msg = str(e)
        logger.exception("agent_processing_failed")
        response = AgentResponse(
            **request.model_dump(exclude={"webhook"}),
            webhook=request.webhook,
            success=False,
            error=error_msg,
        )
        return response

