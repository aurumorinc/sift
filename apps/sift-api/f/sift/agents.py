# /// script
# dependencies = [
#   "sift @ git+https://github.com/aurumorinc/sift.git@0.5.0#subdirectory=packages/sift",
# ]
# ///

from typing import Dict, List, Optional

from sift.modules.agents.schema import AgentResponse
from sift.use_cases.agents.service import main as agents_main


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
