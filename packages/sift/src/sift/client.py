from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from sift.config import settings
from worldline import structlog

logger = structlog.get_logger(__name__)

if TYPE_CHECKING:
    from sift.modules.agents.schema import Agent
    from sift.modules.responses.schema import ResponsesAPIResponse


class SiftClient:
    """Lightweight client facade for Sift API."""

    def __init__(self, **settings_override: Any) -> None:
        """Initialize the client, optionally overriding settings."""
        for key, value in settings_override.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
            else:
                # If extra is allowed, we can still set it on the pydantic model but dynamically it's tricky.
                # Actually, pydantic settings v2 allows setting attributes if extra is allowed, but it's safer to just setattr.
                setattr(settings, key, value)

    def get_agent(self, agent_name: str, version: Optional[int] = None) -> "Agent":
        from sift.modules.agents.repository.langfuse import get_agent

        logger.debug("get_agent_called", agent_name=agent_name, version=version)
        return get_agent(agent_name, version)

    def save_agent(self, agent: "Agent") -> None:
        from sift.modules.agents.repository.langfuse import save_agent

        logger.debug("save_agent_called", agent_name=agent.agent_name)
        return save_agent(agent)

    def compile_and_save_agent(self, payload: Dict[str, Any]) -> None:
        from sift.modules.agents.service import compile_and_save_agent

        agent_name = payload.get("agent_name")
        logger.debug("compile_and_save_agent_called", agent_name=agent_name)
        return compile_and_save_agent(payload)

    def predict_response(
        self,
        agent_id: str,
        input: Union[str, List[Dict[str, Any]]],
        background: bool = False,
    ) -> "ResponsesAPIResponse":
        from sift.modules.responses.service import predict_response

        logger.debug(
            "predict_response_called", agent_id=agent_id, background=background
        )
        return predict_response(agent_id, input, background)
