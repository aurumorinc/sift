import time
import uuid
import dspy
from typing import Any, Dict, List, Union
import structlog

from sift.modules.agents.repository.langfuse import get_agent
from sift.modules.agents.service import AgentModule, _hydrate_multimodal_messages
from sift.modules.responses.schema import (
    ResponseRequest,
    ResponsesAPIResponse,
    ResponseAPIUsage,
)

logger = structlog.get_logger(__name__)


def predict_response(request: ResponseRequest) -> ResponsesAPIResponse:
    agent_id = request.model
    input = request.input
    
    # 1. Fetch Agent schema from repository
    agent = get_agent(agent_id)
    logger.info("fetched_agent", agent_id=agent_id)

    # 2. Extract litellm_params and initialize LM
    litellm_params = agent.litellm_params.copy()
    
    # Merge optional Litellm fields into litellm_params
    litellm_kwargs = request.model_dump(exclude={"model", "input", "background", "webhook"}, exclude_unset=True)
    
    # Map text.format to response_format for DSPy mapping
    if "text" in litellm_kwargs and isinstance(litellm_kwargs["text"], dict):
        if "format" in litellm_kwargs["text"]:
            litellm_params["response_format"] = litellm_kwargs["text"]["format"]
        
        # Remove text so it isn't passed down as an invalid kwarg to dspy.LM
        del litellm_kwargs["text"]
            
    litellm_params.update(litellm_kwargs)
    
    lm = dspy.LM(**litellm_params)
    dspy.settings.configure(lm=lm)

    # 3. Hydrate module
    state_dict = agent.dspy_params.state
    raw_state = {k: v.model_dump() for k, v in state_dict.items()}
    module = AgentModule(raw_state)

    import copy

    loadable_state = copy.deepcopy(raw_state)
    for key, pred_state in loadable_state.items():
        if "signature" in pred_state and "fields" in pred_state["signature"]:
            dspy_fields = []
            sig_fields = pred_state["signature"]["fields"]

            if isinstance(sig_fields, dict):
                field_items = sig_fields.items()
            else:
                field_items = [(f.get("name", ""), f) for f in sig_fields]

            for f_name, f_info in field_items:
                extra = f_info.get("json_schema_extra", {})
                dspy_fields.append(
                    {
                        "prefix": extra.get("prefix", f"{f_name}:"),
                        "description": extra.get("desc", f"${{{f_name}}}"),
                    }
                )
            pred_state["signature"]["fields"] = dspy_fields

    module.load_state(loadable_state)

    # 4. Parse request and execute
    # Convert input to appropriate format for AgentModule
    # If it's a string, we might just pass it as "messages" or the first input field
    inputs = {}

    # AgentModule expects keyword arguments based on its predictor signature.
    # We will try to map the provided input to the first input field of the first predictor.
    predictors = [v for k, v in module.__dict__.items() if isinstance(v, dspy.Predict)]
    if not predictors:
        raise ValueError("No predictors found in agent state.")

    main_predictor = predictors[0]

    # Get the input fields from the predictor's signature
    assert main_predictor.signature is not None, "Predictor must have a signature"
    input_fields = main_predictor.signature.input_fields
    
    # Hydrate if input is multimodal
    hydrated_input = input
    if isinstance(input, list):
        hydrated_input = _hydrate_multimodal_messages(input)
        
    if input_fields:
        first_input_field = list(input_fields.keys())[0]
        inputs[first_input_field] = hydrated_input
    else:
        # Fallback if no input fields
        inputs["messages"] = hydrated_input

    logger.debug("mapped_inputs", inputs_keys=list(inputs.keys()))

    # 5. Execute
    result = module(**inputs)
    logger.info("dspy_execution_completed")

    # 6. Return result mapped to ResponsesAPIResponse
    pred_dict = result.toDict()
    content = pred_dict.get("response") or pred_dict.get("answer") or str(pred_dict)

    # Construct output item
    output_item = {"content": [{"type": "output_text", "text": str(content)}]}

    response = ResponsesAPIResponse(
        id=f"resp_{uuid.uuid4().hex}",
        object="response",
        created_at=int(time.time()),
        model=agent_id,
        status="completed",
        output=[output_item],
        usage=ResponseAPIUsage(input_tokens=0, output_tokens=0, total_tokens=0),
    )

    return response
