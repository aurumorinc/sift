import os
import uuid
import pytest
from dotenv import load_dotenv

from sift.use_cases.responses.service import main
from sift.use_cases.agents.service import main as agents_main

load_dotenv()


@pytest.fixture(scope="module")
def setup_test_agent():
    agent_name = "vcr_test_resp_agent"
    agents_main(
        agent_name=agent_name,
        agent_card_params={},
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"},
        dspy_params={
            "state": {
                "predict": {
                    "signature": {"instructions": "", "fields": []},
                    "train": [
                        {"messages": "What is 2+2?", "response": "4"}
                    ]
                }
            }
        }
    )
    return agent_name


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_simple_text_input(setup_test_agent):
    response = main(
        model=setup_test_agent,
        input="What is 2+2?"
    )
    assert response.success is True
    assert response.response is not None


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_conversational_messages_array_input(setup_test_agent):
    response = main(
        model=setup_test_agent,
        input=[
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi! How can I help you?"},
            {"role": "user", "content": "What is 3+3?"}
        ]
    )
    assert response.success is True
    assert response.response is not None


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_multimodal_vision_input(setup_test_agent):
    response = main(
        model=setup_test_agent,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image."},
                    {"type": "image_url", "image_url": "https://raw.githubusercontent.com/aurumorinc/sift/main/README.md"}
                ]
            }
        ]
    )
    assert response.success is True


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_structured_json_schema_output(setup_test_agent):
    response = main(
        model=setup_test_agent,
        input="Give me a random user profile.",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "UserProfile",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    },
                    "required": ["name", "age"]
                }
            }
        }
    )
    assert response.success is True
    # The output should theoretically be a JSON string or dict depending on the exact implementation


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_async_background_request(setup_test_agent):
    response = main(
        model=setup_test_agent,
        input="Hello",
        background=True,
        webhook={
            "url": "https://httpbin.org/post",
            "token": "dummy"
        }
    )
    assert response.success is True
