from sift.modules.agents.schema import DSPyTrainingExample, Agent, DSPyParams


def test_dspy_training_example_valid_schema():
    example = DSPyTrainingExample(score=0.9, feedback="Good", question="Hi")
    assert example.score == 0.9
    assert example.feedback == "Good"
    assert example.model_extra is not None
    assert example.model_extra["question"] == "Hi"
    assert getattr(example, "question") == "Hi"


def test_dspy_training_example_missing_extras():
    example = DSPyTrainingExample(score=0.5)
    assert example.score == 0.5
    assert example.feedback is None
    assert example.trace_id is None
    assert example.model_extra is None or len(example.model_extra) == 0


def test_dspy_training_example_messages():
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}}
            ]
        }
    ]
    example = DSPyTrainingExample(messages=messages, score=1.0)
    assert example.score == 1.0
    assert isinstance(example.messages, list)
    assert len(example.messages) == 1
    msg = example.messages[0]
    assert isinstance(msg, dict)
    assert msg["role"] == "user"
    content = msg.get("content", [])
    assert isinstance(content, list)
    assert len(content) == 2
    assert isinstance(content[1], dict)
    assert content[1]["type"] == "image_url"

def test_dspy_training_example_string_messages_and_structured_response():
    example = DSPyTrainingExample(
        messages="What is the capital of France?",
        response={"capital": "Paris", "country": "France"},
        output="Just Paris"
    )
    assert example.messages == "What is the capital of France?"
    assert isinstance(example.response, dict)
    assert example.response["capital"] == "Paris"
    assert example.output == "Just Paris"


def test_agent_name_auto_generation():
    agent = Agent(
        agent_card_params={},
        litellm_params={},
        dspy_params=DSPyParams(state={})
    )
    assert agent.agent_name is not None
    assert isinstance(agent.agent_name, str)
    assert len(agent.agent_name) == 32


def test_agent_sparse_parsing():
    """Assert that Agent.model_validate({}) succeeds and auto-creates defaults."""
    agent = Agent.model_validate({})
    assert isinstance(agent.agent_card_params, dict)
    assert len(agent.agent_card_params) == 0
    assert isinstance(agent.litellm_params, dict)
    assert len(agent.litellm_params) == 0
    assert isinstance(agent.dspy_params, DSPyParams)
    assert "predict" in agent.dspy_params.state
    assert agent.dspy_params.state["predict"].signature.instructions == ""
    assert isinstance(agent.dspy_params.state["predict"].signature.fields, list)
    assert len(agent.dspy_params.state["predict"].signature.fields) == 0


def test_dspy_predictor_state_sparse_parsing():
    """Assert parsing a predictor state with missing signature auto-injects defaults."""
    from sift.modules.agents.schema import DSPyPredictorState
    state = DSPyPredictorState.model_validate({"train": []})
    assert state.signature is not None
    assert state.signature.instructions == ""
    assert state.signature.fields == []
