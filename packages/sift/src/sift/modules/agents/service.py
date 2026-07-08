import dspy
from typing import Any, Dict, List
from worldline import structlog

logger = structlog.get_logger(__name__)


def _hydrate_multimodal_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Recursively parses multimodal messages and hydrates image_url dicts into native dspy.Image instances."""
    hydrated = []
    for msg in messages:
        if isinstance(msg.get("content"), list):
            new_content = []
            for part in msg["content"]:
                if isinstance(part, dict) and part.get("type") == "image_url" and isinstance(part.get("image_url"), dict):
                    url = part["image_url"].get("url")
                    if url:
                        new_content.append(dspy.Image(url=url))
                    else:
                        new_content.append(part)
                else:
                    new_content.append(part)
            # Create a shallow copy and update content
            new_msg = dict(msg)
            new_msg["content"] = new_content
            hydrated.append(new_msg)
        else:
            hydrated.append(msg)
    return hydrated


class AgentModule(dspy.Module):
    def __init__(self, state_dict: Dict[str, Any]):
        super().__init__()
        for key, pred_state in state_dict.items():
            if not isinstance(pred_state, dict):
                continue

            sig_state = pred_state.get("signature", {})
            instructions = sig_state.get("instructions", "")
            fields = sig_state.get("fields", [])

            # Reconstruct a generic signature string based on the fields.
            inputs = []
            outputs = []

            # fields can be a dict (name -> info) or list (if serialized differently)
            if isinstance(fields, dict):
                field_items = fields.items()
            else:
                field_items = [(f.get("name", ""), f) for f in fields]

            for f_name, f_info in field_items:
                if not f_name:
                    continue
                extra = f_info.get("json_schema_extra", {})
                field_type = extra.get("__dspy_field_type")
                if field_type == "input":
                    inputs.append(f_name)
                elif field_type == "output":
                    outputs.append(f_name)
                else:
                    # Fallback logic
                    if (
                        "response" in f_name.lower()
                        or "output" in f_name.lower()
                        or "answer" in f_name.lower()
                    ):
                        outputs.append(f_name)
                    else:
                        inputs.append(f_name)

            # If we couldn't parse inputs/outputs, default to something sensible
            if not inputs:
                inputs = ["messages"]
            if not outputs:
                outputs = ["response"]

            sig_string = f"{', '.join(inputs)} -> {', '.join(outputs)}"

            # Create the predictor
            predictor = dspy.Predict(sig_string)

            # Attempt to set the exact instructions
            if instructions:
                predictor.signature.__doc__ = instructions

            setattr(self, key, predictor)

    def load_state(self, state_dict: Dict[str, Any]):
        # Hydrate messages arrays in demos
        for key, pred_state in state_dict.items():
            if isinstance(pred_state, dict) and "demos" in pred_state:
                for demo in pred_state["demos"]:
                    if "messages" in demo and isinstance(demo["messages"], list):
                        demo["messages"] = _hydrate_multimodal_messages(demo["messages"])
        super().load_state(state_dict)

    def forward(self, **kwargs):
        # We assume the first predictor is the main entry point
        # For a generic agent, we just pass the kwargs to the first predictor.
        predictors = [
            v for k, v in self.__dict__.items() if isinstance(v, dspy.Predict)
        ]
        if not predictors:
            raise ValueError("No predictors found in agent state.")

        main_predictor = predictors[0]
        return main_predictor(**kwargs)


def compile_and_save_agent(payload: Dict[str, Any]) -> None:
    from sift.modules.agents.schema import Agent, DSPyPredictorState, DSPySignatureState
    import dspy.teleprompt
    from sift.modules.agents.metric import dynamic_api_metric
    from sift.modules.agents.repository.langfuse import save_agent

    # 1. Instantiate Agent from updated schema
    agent = Agent(**payload)

    # 1.5 Infer fields for new agents missing signature configuration
    for key, pred_state in agent.dspy_params.state.items():
        if not pred_state.signature.fields and pred_state.train:
            first_example = pred_state.train[0]
            # Convert DSPyTrainingExample to dict, omitting unset optional fields
            example_dict = first_example.model_dump(exclude_unset=True)
            inferred_fields = []
            for k, v in example_dict.items():
                if k in ["trace_id", "score", "feedback"]:
                    continue
                if k == "messages" and not v:
                    continue
                # Categorize inputs/outputs based on common naming
                if (
                    "response" in k.lower()
                    or "output" in k.lower()
                    or "answer" in k.lower()
                ):
                    field_type = "output"
                else:
                    field_type = "input"
                inferred_fields.append(
                    {
                        "name": k,
                        "json_schema_extra": {
                            "__dspy_field_type": field_type,
                            "prefix": f"{k.capitalize()}:",
                            "desc": f"${{{k}}}",
                        },
                    }
                )
            pred_state.signature.fields = inferred_fields

    # 2. Extract litellm_params and initialize LM
    litellm_params = agent.litellm_params.copy()
    lm = dspy.LM(**litellm_params)
    dspy.settings.configure(lm=lm)

    # 3. Hydrate module
    raw_state = {k: v.model_dump() for k, v in agent.dspy_params.state.items()}
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

    # Convert trainset dictionaries into dspy.Examples
    trainset = []
    for key, pred_state in raw_state.items():
        for example_dict in pred_state.get("train", []):
            filtered_dict = {k: v for k, v in example_dict.items() if k != "trace_id"}
            
            if "messages" in filtered_dict and not filtered_dict["messages"]:
                del filtered_dict["messages"]
            elif "messages" in filtered_dict and isinstance(filtered_dict["messages"], list):
                filtered_dict["messages"] = _hydrate_multimodal_messages(filtered_dict["messages"])

            # Determine inputs vs labels
            sig_fields = pred_state.get("signature", {}).get("fields", [])
            inputs = []

            if isinstance(sig_fields, dict):
                field_items = sig_fields.items()
            else:
                field_items = [(f.get("name", ""), f) for f in sig_fields]

            for f_name, f_info in field_items:
                if not f_name:
                    continue
                extra = f_info.get("json_schema_extra", {})
                if extra.get("__dspy_field_type") == "input":
                    inputs.append(f_name)
                elif (
                    "response" not in f_name.lower()
                    and "output" not in f_name.lower()
                    and "answer" not in f_name.lower()
                ):
                    inputs.append(f_name)

            if not inputs:
                inputs = ["messages"]

            trainset.append(dspy.Example(**filtered_dict).with_inputs(*inputs))

    # Recompile module using a basic optimizer if we have a trainset
    if trainset:
        logger.info("compiling_agent_started", trainset_size=len(trainset))

        optimizer_name = agent.dspy_params.optimizer or "BootstrapFewShot"
        optimizer_params = agent.dspy_params.optimizer_params or {}
        optimizer_params_dict = dict(optimizer_params)
        
        optimizer_class = getattr(dspy.teleprompt, optimizer_name, None)
        if not optimizer_class:
            raise ValueError(f"Optimizer {optimizer_name} not found in dspy.teleprompt")
            
        optimizer_params_dict["metric"] = dynamic_api_metric
        optimizer = optimizer_class(**optimizer_params_dict)

        compiled_module = optimizer.compile(module, trainset=trainset)
        logger.info("compiling_agent_finished")
    else:
        logger.info("compiling_agent_skipped_no_trainset")
        compiled_module = module

    # 4. Versioned Persistence
    new_state = compiled_module.dump_state()
    for key, pred_state in new_state.items():
        if key in agent.dspy_params.state:
            original_fields = agent.dspy_params.state[key].signature.fields
            optimized_instructions = pred_state.get("signature", {}).get(
                "instructions", ""
            )

            merged_signature = DSPySignatureState(
                instructions=optimized_instructions,
                fields=original_fields,
            )

            agent.dspy_params.state[key] = DSPyPredictorState(**pred_state)
            agent.dspy_params.state[key].signature = merged_signature

    save_agent(agent)
