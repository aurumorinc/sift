from typing import Dict, List, Optional, Union

from worldline import structlog

from sift.client import SiftClient
from sift.modules.responses.schema import ResponseRequest, ResponseResponse
from sift.utils.webhook.service import webhook_dispatch

logger = structlog.get_logger(__name__)

client = SiftClient()


@webhook_dispatch
def main(
    model: str,
    input: Union[str, List[Dict]],
    background: bool = False,
    webhook: Optional[Dict] = None,
) -> ResponseResponse:
    """Inference endpoint mapping standard Responses API payload."""
    request = ResponseRequest(
        model=model,
        input=input,
        background=background,
        webhook=webhook,
    )

    logger.info("processing_response_request", agent_id=request.model)

    try:
        # Extract agent_id from model
        agent_id = request.model
        if agent_id.startswith("a2a_agent/"):
            agent_id = agent_id[len("a2a_agent/") :]

        # Execute inference via SiftClient
        background_val = request.background if request.background is not None else False
        response_data = client.predict_response(agent_id, request.input, background_val)

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
