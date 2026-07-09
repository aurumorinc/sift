# /// script
# dependencies = [
#   "sift @ git+https://github.com/aurumorinc/sift.git@0.10.0#subdirectory=packages/sift",
#   "wmill",
# ]
# ///
import os
import wmill
from typing import Dict, List, Optional

from sift.modules.agents.schema import AgentResponse
from sift.use_cases.agents.service import main as agents_main

os.environ["GEMINI_API_KEY"] = wmill.get_variable("f/sift/gemini_api_key")
os.environ["LANGFUSE_SECRET_KEY"] = wmill.get_variable("f/sift/langfuse_secret_key")
os.environ["LANGFUSE_PUBLIC_KEY"] = wmill.get_variable("f/sift/langfuse_public_key")
os.environ["LANGFUSE_BASE_URL"] = wmill.get_variable("f/sift/langfuse_base_url")
os.environ["LANGFUSE_HOST"] = wmill.get_variable("f/sift/langfuse_host")


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
    return agents_main(
        agent_name=agent_name,
        agent_card_params=agent_card_params,
        litellm_params=litellm_params,
        dspy_params=dspy_params,
        object_permission=object_permission,
        labels=labels,
        webhook=webhook,
    )
