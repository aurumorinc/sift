from typing import Any, Dict, List, Optional, Union

import structlog

from sift.client import SiftClient
from sift.modules.responses.schema import ResponseRequest, ResponseResponse
from sift.utils.webhook.service import webhook_dispatch

logger = structlog.get_logger(__name__)

client = SiftClient()


@webhook_dispatch(event_prefix="response")
def main(
    model: str,
    input: Union[str, List[Dict]],
    background: bool = False,
    webhook: Optional[Dict] = None,
    **kwargs: Any
) -> ResponseResponse:
    """Inference endpoint mapping standard Responses API payload."""
    request = ResponseRequest(
        model=model,
        input=input,
        background=background,
        webhook=webhook,
        **kwargs
    )

    logger.info("processing_response_request", agent_id=request.model)

    try:
        # Extract agent_id from model
        agent_id = request.model
        if agent_id.startswith("a2a_agent/"):
            agent_id = agent_id[len("a2a_agent/") :]

        # Execute inference via SiftClient
        background_val = request.background if request.background is not None else False
        
        # Extract kwargs to pass through
        passthrough_kwargs = request.model_dump(exclude={"model", "input", "background", "webhook"}, exclude_unset=True)
        response_data = client.predict_response(agent_id, request.input, background_val, **passthrough_kwargs)

        response_dict = response_data.model_dump()
        response_dict.pop("error", None)
        response = ResponseResponse(
            **response_dict,
            success=True,
            error=None,
        )
        logger.info("response_processing_completed")
        return response
    except Exception as e:
        error_msg = str(e)
        logger.exception("response_processing_failed")
        import time
        response = ResponseResponse(
            id="error",
            created_at=int(time.time()),
            model=request.model,
            object="error",
            output=[],
            success=False,
            error=error_msg,
        )
        return response
