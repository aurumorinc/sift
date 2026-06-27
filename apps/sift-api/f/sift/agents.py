# /// script
# dependencies = [
#   "sift @ git+https://github.com/aurumorinc/sift.git@0.2.0#subdirectory=packages/sift",
# ]
# ///

from sift import SiftClient, AgentRequest, AgentResponse, webhook_dispatch
from worldline import structlog

logger = structlog.get_logger(__name__)

client = SiftClient()


@webhook_dispatch
def main(request: AgentRequest) -> AgentResponse:
    """Create/compile agents and trigger webhooks."""
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
