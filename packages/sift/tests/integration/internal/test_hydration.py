import dspy

from typing import cast

from sift.modules.responses.service import predict_response
from sift.modules.agents.schema import AgentpredictRequest


def test_end_to_end_hydration(mocker):
    # Mock Langfuse API call to fetch a prompt
    mock_get = mocker.patch(
        "sift.modules.agents.repository.langfuse.get_langfuse_client"
    )
    mock_client = mocker.Mock()

    mock_prompt = mocker.Mock()
    mock_prompt.prompt = None
    mock_prompt.config = {
        "agent_name": "test-agent-model",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o", "temperature": 0.0},
        "dspy_params": {
            "optimizer": None,
            "state": {"predict": dspy.Predict("messages -> answer").dump_state()},
        },
    }
    mock_client.get_prompt.return_value = mock_prompt
    mock_get.return_value = mock_client

    # We want to mock dspy.LM since we don't actually want to call OpenAI in our integration tests
    mock_lm_cls = mocker.patch("dspy.LM")
    mock_lm_instance = mocker.Mock()
    mock_lm_instance.history = [
        {"usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}
    ]
    mock_lm_cls.return_value = mock_lm_instance

    # To ensure module(...) execution returns something predictable, we can mock AgentModule's forward method
    mock_generic_agent_forward = mocker.patch(
        "sift.modules.agents.service.AgentModule.forward"
    )
    mock_generic_agent_forward.return_value = dspy.Prediction(answer="Mocked Answer")

    # Prepare request
    req = AgentpredictRequest(
        messages=[{"role": "user", "content": "What is the answer?"}]
    )

    # Execute
    res = predict_response("test-agent-model", req.messages, False)

    # Verify Langfuse was called
    mock_client.get_prompt.assert_called_once_with(
        name="test-agent-model", version=None
    )

    # Verify LM was initialized correctly
    mock_lm_cls.assert_called_once_with(model="openai/gpt-4o", temperature=0.0)

    # Verify module was executed with the mapped inputs
    mock_generic_agent_forward.assert_called_once_with(
        messages=[{"role": "user", "content": "What is the answer?"}]
    )

    # Verify Response mapping
    assert res.model == "test-agent-model"
    assert len(res.output) == 1
    
    output_item = cast(dict, res.output[0])
    assert output_item["content"][0]["text"] == "Mocked Answer"
    assert res["usage"]["total_tokens"] == 0
