import dspy
import pytest

from typing import cast
from unittest.mock import patch, MagicMock

from sift.client import SiftClient


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("sift.modules.agents.repository.langfuse.get_agent")
@patch("sift.modules.responses.service.get_agent")
@patch("dspy.LM")
def test_workflow(mock_lm, mock_resp_get_agent, mock_get_agent, mock_save_agent):
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
            "state": {
                "predict": {
                    "signature": {
                        "instructions": "Given messages, produce answer.",
                        "fields": [
                            {"name": "messages", "json_schema_extra": {"__dspy_field_type": "input"}},
                            {"name": "answer", "json_schema_extra": {"__dspy_field_type": "output"}},
                        ]
                    }
                }
            },
        },
    }
    client.compile_and_save_agent(payload)

    # Capture saved agent to mock get_agent
    saved_agent = mock_save_agent.call_args[0][0]
    mock_get_agent.return_value = saved_agent
    mock_resp_get_agent.return_value = saved_agent

    # 2. Get agent to ensure it was saved correctly
    agent = client.get_agent(agent_name)
    assert agent is not None
    assert agent.agent_name == agent_name
    assert agent.litellm_params["model"] == "gemini/gemini-3.1-flash-lite"

    # 3. Predict response
    mock_lm_instance = MagicMock()
    mock_lm_instance.return_value = ["hello world"]
    mock_lm.return_value = mock_lm_instance

    with patch("sift.modules.agents.service.AgentModule.forward") as mock_forward:
        mock_forward.return_value = dspy.Prediction(answer="hello world")
        messages = [{"role": "user", "content": "Say 'hello world' literally."}]
        response = client.predict_response(agent_name, messages)

    assert response is not None
    assert response.model == agent_name

    # Verify the model returned output
    assert len(response.output) > 0
    
    out_dict = response.output[0]
    if hasattr(out_dict, "model_dump"):
        out_dict = out_dict.model_dump()
    elif hasattr(out_dict, "dict"):
        out_dict = out_dict.dict()
    assert isinstance(out_dict, dict)
    text_content = ""
    if "content" in out_dict and isinstance(out_dict["content"], list):
        text_content = out_dict["content"][0].get("text", "")
    elif "message" in out_dict and isinstance(out_dict["message"], dict):
        text_content = out_dict["message"].get("content", "")
    else:
        text_content = out_dict.get("text", "")
        
    assert "hello world" in text_content.lower()


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("sift.modules.agents.repository.langfuse.get_agent")
@patch("sift.modules.responses.service.get_agent")
@patch("dspy.LM")
def test_workflow_multimodal(mock_lm, mock_resp_get_agent, mock_get_agent, mock_save_agent):
    client = SiftClient()

    agent_name = "e2e-test-multimodal-agent"

    # 1. Compile and save agent
    payload = {
        "agent_name": agent_name,
        "agent_card_params": {},
        "litellm_params": {
            "model": "gemini/gemini-2.5-flash",
            "temperature": 0.0,
        },
        "dspy_params": {
            "optimizer": None,
            "state": {
                "predict": {
                    "signature": {
                        "instructions": "Given messages, produce answer.",
                        "fields": [
                            {"name": "messages", "json_schema_extra": {"__dspy_field_type": "input"}},
                            {"name": "answer", "json_schema_extra": {"__dspy_field_type": "output"}},
                        ]
                    }
                }
            },
        },
    }
    client.compile_and_save_agent(payload)

    # Capture saved agent to mock get_agent
    saved_agent = mock_save_agent.call_args[0][0]
    mock_get_agent.return_value = saved_agent
    mock_resp_get_agent.return_value = saved_agent

    # 2. Get agent to ensure it was saved correctly
    agent = client.get_agent(agent_name)
    assert agent is not None
    assert agent.agent_name == agent_name

    # 3. Predict response with multimodal input
    mock_lm_instance = MagicMock()
    mock_lm_instance.return_value = ["red"]
    mock_lm.return_value = mock_lm_instance

    with patch("sift.modules.agents.service.AgentModule.forward") as mock_forward:
        mock_forward.return_value = dspy.Prediction(answer="red")
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is the primary color in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Synthese%2B.svg/200px-Synthese%2B.svg.png"}
                    }
                ]
            }
        ]
        response = client.predict_response(agent_name, messages)

    assert response is not None
    assert response.model == agent_name

    # Verify the model returned output
    assert len(response.output) > 0
    out_dict = response.output[0]
    if hasattr(out_dict, "model_dump"):
        out_dict = out_dict.model_dump()
    elif hasattr(out_dict, "dict"):
        out_dict = out_dict.dict()
    assert isinstance(out_dict, dict)
    text_content = ""
    if "content" in out_dict and isinstance(out_dict["content"], list):
        text_content = out_dict["content"][0].get("text", "")
    elif "message" in out_dict and isinstance(out_dict["message"], dict):
        text_content = out_dict["message"].get("content", "")
    else:
        text_content = out_dict.get("text", "")
        
    assert len(text_content) > 0


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("sift.modules.agents.repository.langfuse.get_agent")
@patch("sift.modules.responses.service.get_agent")
@patch("dspy.LM")
def test_workflow_structured_responses(mock_lm, mock_resp_get_agent, mock_get_agent, mock_save_agent):
    import json
    client = SiftClient()

    agent_name = "e2e-test-structured-agent"

    # 1. Compile and save agent
    payload = {
        "agent_name": agent_name,
        "agent_card_params": {},
        "litellm_params": {
            "model": "openai/gpt-4o-mini",
            "temperature": 0.0,
        },
        "dspy_params": {
            "optimizer": None,
            "state": {
                "predict": {
                    "signature": {
                        "instructions": "Given messages, produce response.",
                        "fields": [
                            {"name": "messages", "json_schema_extra": {"__dspy_field_type": "input"}},
                            {"name": "response", "json_schema_extra": {"__dspy_field_type": "output"}},
                        ]
                    }
                }
            },
        },
    }
    client.compile_and_save_agent(payload)

    saved_agent = mock_save_agent.call_args[0][0]
    mock_get_agent.return_value = saved_agent
    mock_resp_get_agent.return_value = saved_agent

    mock_lm_instance = MagicMock()
    mock_lm_instance.return_value = ['{"name": "John Doe", "age": 28}']
    mock_lm.return_value = mock_lm_instance

    with patch("sift.modules.agents.service.AgentModule.forward") as mock_forward:
        mock_forward.return_value = dspy.Prediction(response='{"name": "John Doe", "age": 28}')
        # 2. Predict response with structured output format
        messages = [{"role": "user", "content": "Extract details: John Doe is 28 years old."}]
        response = client.predict_response(
            agent_id=agent_name,
            input=messages,
            text={"format": {"type": "json_object"}}
        )

    assert response is not None
    assert response.model == agent_name

    # Verify the model returned output
    assert len(response.output) > 0
    out_dict = response.output[0]
    if hasattr(out_dict, "model_dump"):
        out_dict = out_dict.model_dump()
    elif hasattr(out_dict, "dict"):
        out_dict = out_dict.dict()
    assert isinstance(out_dict, dict)
    text_content = ""
    if "content" in out_dict and isinstance(out_dict["content"], list):
        text_content = out_dict["content"][0].get("text", "")
    elif "message" in out_dict and isinstance(out_dict["message"], dict):
        text_content = out_dict["message"].get("content", "")
    else:
        text_content = out_dict.get("text", "")
    
    # Try parsing to make sure it's valid JSON
    parsed = json.loads(text_content)
    assert isinstance(parsed, dict)
