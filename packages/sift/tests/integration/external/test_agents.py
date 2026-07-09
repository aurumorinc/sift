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


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_windmill_sparse_payload_compilation():
    """Reproduces the Windmill bug where missing required fields caused Pydantic to crash."""
    agent_name = "vcr_test_agent_sparse"
    response = main(
        agent_name=agent_name,
        litellm_params={"model": "gemini/gemini-3.1-flash-lite"},
        dspy_params={
            "state": {
                "predict": {
                    "train": [
                        {"messages": "What is 2+2?", "response": "4"}
                    ]
                }
            }
        }
    )
    # The fix ensures Pydantic validation passes and defaults are set correctly.
    assert response.success is True
    assert isinstance(response.agent_card_params, dict)
    assert response.dspy_params.state["predict"].signature is not None


def test_completely_empty_payload():
    """Tests that main() works with completely empty parameters, using schema defaults."""
    response = main()
    assert response.success is True
    assert response.agent_name is not None
    assert isinstance(response.dspy_params.state["predict"].signature.fields, list)


def test_explicit_null_overrides():
    """Tests that passing explicit null to dict fields is caught correctly as an error, rather than crashing."""
    response = main(
        agent_name="vcr_test_agent_null",
        litellm_params=None,  # We allow None as an optional kwargs on main
        # But wait, main() handles Optional by skipping it.
        # If the user somehow forces an invalid payload via dict bypassing:
    )
    # If it's valid to pass None to main(), it skips it and uses default.
    assert response.success is True
    
    from pydantic import ValidationError
    # Let's force an invalid type that deep merge will accept but Pydantic will reject
    with pytest.raises(ValidationError) as exc_info:
        main(
            litellm_params=["invalid", "list"] # type: ignore
        )
    # Should raise the ValidationError back to the caller
    assert "Input should be a valid dictionary" in str(exc_info.value)


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_multiple_custom_predictor_states():
    """Tests defaulting logic for completely custom states."""
    agent_name = "vcr_test_agent_multi_state"
    response = main(
        agent_name=agent_name,
        dspy_params={
            "state": {
                "classify": {"train": [{"messages": "text", "response": "class"}]},
                "generate": {"train": [{"messages": "topic", "response": "story"}]}
            }
        }
    )
    assert response.success is True
    assert "classify" in response.dspy_params.state
    assert "generate" in response.dspy_params.state
    assert response.dspy_params.state["classify"].signature.instructions == ""
    assert response.dspy_params.state["generate"].signature.instructions == ""


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_partial_nested_missing_fields():
    """Tests passing partial nested objects (like signature with fields but no instructions)."""
    agent_name = "vcr_test_agent_partial_nested"
    response = main(
        agent_name=agent_name,
        dspy_params={
            "state": {
                "predict": {
                    "signature": {"fields": [{"name": "input"}]}
                }
            }
        }
    )
    assert response.success is True
    assert response.dspy_params.state["predict"].signature.instructions == ""
    assert len(response.dspy_params.state["predict"].signature.fields) == 1


@pytest.mark.vcr(match_on=['method', 'scheme', 'host', 'port', 'path', 'query'])
def test_non_destructive_partial_updates():
    """Tests that deep merge doesn't overwrite an existing signature with defaults."""
    agent_name = "vcr_test_agent_non_destructive"
    # Create with a custom signature
    main(
        agent_name=agent_name,
        dspy_params={
            "state": {
                "predict": {
                    "signature": {"instructions": "DO NOT OVERWRITE", "fields": []}
                }
            }
        }
    )
    
    # Update with only a train array
    response = main(
        agent_name=agent_name,
        dspy_params={
            "state": {
                "predict": {
                    "train": [{"messages": "Hi", "response": "Hello"}]
                }
            }
        }
    )
    
    assert response.success is True
    # Ensure the signature from Langfuse was preserved
    assert response.dspy_params.state["predict"].signature.instructions == "DO NOT OVERWRITE"
