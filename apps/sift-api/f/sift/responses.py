# /// script
# dependencies = [
#   "sift @ git+https://github.com/aurumorinc/sift.git@0.2.0#subdirectory=packages/sift",
# ]
# ///

from sift import SiftClient, ResponseRequest, ResponseResponse, webhook_dispatch
from worldline import structlog

logger = structlog.get_logger(__name__)

client = SiftClient()


@webhook_dispatch
def main(request: ResponseRequest) -> ResponseResponse:
    """Inference endpoint mapping standard Responses API payload."""
    logger.info("processing_response_request", agent_id=request.model)

    try:
        # Extract agent_id from model
        agent_id = request.model
        if agent_id.startswith("a2a_agent/"):
            agent_id = agent_id[len("a2a_agent/") :]

        # Execute inference via SiftClient
        background = request.background if request.background is not None else False
        response_data = client.predict_response(
            agent_id, request.input, background
        )

        response = ResponseResponse(
            success=True,
            error=None,
            response=response_data,
            webhook=request.webhook,
        )
        logger.info("response_processing_completed")
        return response
    except Exception as e:
        error_msg = str(e)
        logger.exception("response_processing_failed")
        response = ResponseResponse(
            success=False,
            error=error_msg,
            response=None,
            webhook=request.webhook,
        )
        return response
