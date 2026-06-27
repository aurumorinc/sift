from typing import Optional
from worldline import structlog

from sift.integrations.langfuse.service import get_langfuse_client
from sift.modules.agents.schema import Agent

logger = structlog.get_logger(__name__)


def get_agent(agent_name: str, version: Optional[int] = None) -> Agent:
    """Fetch an agent configuration from Langfuse Prompt Management."""
    logger.info("fetching_agent", agent_name=agent_name, version=version)
    client = get_langfuse_client()
    prompt = client.get_prompt(name=agent_name, version=version)

    payload = prompt.config if isinstance(prompt.config, dict) else {}

    if "agent_name" not in payload:
        payload["agent_name"] = agent_name

    return Agent(**payload)


def save_agent(agent: Agent) -> None:
    """Save an agent configuration to Langfuse Prompt Management."""
    logger.info("saving_agent", agent_name=agent.agent_name)
    client = get_langfuse_client()
    labels = agent.labels or ["production"]

    instructions = (
        "\n\n".join(
            state.signature.instructions for state in agent.dspy_params.state.values()
        )
        if agent.dspy_params.state
        else ""
    )

    client.create_prompt(
        name=agent.agent_name,
        prompt=instructions,
        config=agent.model_dump(mode="json"),
        type="text",
        labels=labels,
    )
