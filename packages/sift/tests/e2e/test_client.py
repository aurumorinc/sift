import dspy
import pytest

from typing import cast

from sift.client import SiftClient


@pytest.mark.vcr
def test_workflow():
    client = SiftClient()

    agent_name = "e2e-test-gemini-agent"

    # 1. Compile and save agent
    payload = {
        "agent_name": agent_name,
        "agent_card_params": {},
        "litellm_params": {
            "model": "gemini/gemini-3.1-flash-lite",
            "temperature": 0.0,
        },
        "dspy_params": {
            "optimizer": None,
            "state": {"predict": dspy.Predict("messages -> answer").dump_state()},
        },
    }
    client.compile_and_save_agent(payload)

    # 2. Get agent to ensure it was saved correctly
    agent = client.get_agent(agent_name)
    assert agent is not None
    assert agent.agent_name == agent_name
    assert agent.litellm_params["model"] == "gemini/gemini-3.1-flash-lite"

    # 3. Predict response
    messages = [{"role": "user", "content": "Say 'hello world' literally."}]
    response = client.predict_response(agent_name, messages)

    assert response is not None
    assert response.model == agent_name

    # Verify the model returned output
    assert len(response.output) > 0
    output_item = cast(dict, response.output[0])
    text_content = output_item["content"][0]["text"].lower()
    assert "hello world" in text_content
