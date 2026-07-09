import os
import uuid
import pytest
from dotenv import load_dotenv

from sift.use_cases.agents.service import main

load_dotenv()


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_full_configuration():
    agent_name = "vcr_test_agent_full_config"
    response = main(
        agent_name=agent_name,
        agent_card_params={},
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"},
        dspy_params={
            "optimizer": "BootstrapFewShot",
            "state": {
                "predict": {
                    "signature": {
                        "instructions": "You are a helpful assistant.",
                        "fields": [
                            {"name": "messages", "description": "Input messages"},
                            {"name": "response", "description": "Output response"}
                        ]
                    },
                    "train": [
                        {"messages": "Hello", "response": "Hi there!"},
                        {"messages": "How are you?", "response": "I'm doing well, thanks!"}
                    ]
                }
            }
        }
    )
    assert response.success is True
    assert response.agent_name == agent_name


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_zero_config_auto_inference():
    agent_name = "vcr_test_agent_zero_config"
    response = main(
        agent_name=agent_name,
        agent_card_params={},
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"},
        dspy_params={
            "state": {
                "predict": {
                    "signature": {"instructions": "", "fields": []},
                    "train": [
                        {"messages": "What is 2+2?", "response": "4"},
                        {"messages": "What is 3+3?", "response": "6"}
                    ]
                }
            }
        }
    )
    assert response.success is True
    assert response.agent_name == agent_name


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_multimodal_vision_training():
    agent_name = "vcr_test_agent_multimodal"
    response = main(
        agent_name=agent_name,
        agent_card_params={},
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"},
        dspy_params={
            "state": {
                "predict": {
                    "signature": {"instructions": "", "fields": []},
                    "train": [
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": "Describe this image."},
                                        {"type": "image_url", "image_url": "https://raw.githubusercontent.com/aurumorinc/sift/main/README.md"} # Using a dummy URL for test
                                    ]
                                }
                            ],
                            "response": "This is a document."
                        }
                    ]
                }
            }
        }
    )
    assert response.success is True


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_update_agent_deep_merge():
    agent_name = "vcr_test_agent_deep_merge"
    # Create
    main(
        agent_name=agent_name,
        agent_card_params={},
        dspy_params={"state": {}},
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"}
    )
    
    # Update
    response = main(
        agent_name=agent_name,
        dspy_params={
            "state": {
                "predict": {
                    "signature": {"instructions": "", "fields": []},
                    "train": [
                        {"messages": "Update test", "response": "Passed"}
                    ]
                }
            }
        }
    )
    assert response.success is True
    assert response.litellm_params.get("model") == "gemini/gemini-3.1-flash-lite"
    assert "predict" in response.dspy_params.state


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_async_compilation_with_webhook():
    agent_name = "vcr_test_agent_async_webhook"
    response = main(
        agent_name=agent_name,
        agent_card_params={},
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"},
        dspy_params={"state": {}},
        webhook={
            "url": "https://httpbin.org/post",
            "token": "dummy_token"
        }
    )
    # The webhook logic triggers and suppresses exceptions normally if they fail,
    # but the compilation should succeed.
    assert response.success is True
