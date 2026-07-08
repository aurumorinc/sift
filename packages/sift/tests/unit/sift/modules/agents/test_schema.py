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
    assert len(example.messages) == 1
    assert example.messages[0]["role"] == "user"
    assert len(example.messages[0]["content"]) == 2
    assert example.messages[0]["content"][1]["type"] == "image_url"


def test_agent_name_auto_generation():
    agent = Agent(
        agent_card_params={},
        litellm_params={},
        dspy_params=DSPyParams(state={})
    )
    assert agent.agent_name is not None
    assert isinstance(agent.agent_name, str)
    assert len(agent.agent_name) == 32
